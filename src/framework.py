"""

 Script to automatically run framework (this file can be run individualy or the tool can be used)
 To run this file follow the next instructions 
 the file needs to be run with the next arguments:
 
    data: Datasets of gene expression to use. If multiple use ",".
          Make sure to include the folder they are located in.
          Folders should be in datasets directory. 
          Example with two datasets: data=P53-MDM2/data.csv,ecoli_data/Exp4.csv

    rules: Boolean functions files for each system. If multiple use ",".
           Make sure to include the folder they are located in.
           Folders should be in datasets directory. 
           Example with two datasets: rules=P53-MDM2/rules.csv,ecoli_data/rules.csv 
           
    inf: Selected inferece methods. Here you can specify which inference methods to use.
         The ones offered are: Besfit, MIBNI, LogicGep.
         Example to run: inf=Bestfit,MIBNI
         
    bin: Selected threshold methods. Here you can specify which threshold methods to use.
         The ones offered are: BASCA, K-Means, Onestep.
         Example to run: bin=BASCA,K-Means,Onestep
         
    impu: Selected imputation strategies per dataset. Here you can specify which imputation strategies to use per dataset.
          If multiple datasets use "," to specify which imputation to which dataset
         The ones offered are: 1: probabilistic and missforest, and only missforest, 2: only missforest 
         Example to run: impu=1,2
    
    To run this code using an example use the following command:
     
        python framework.py data=P53-MDM2/data.csv,yeast_cell/yeast_data_elu.csv,ecoli_data/Exp4.csv rules=P53-MDM2/rules.csv,yeast_cell/rules.csv,ecoli_data/rules.csv inf=MIBNI,LogicGep,Bestfit bin=BASCA,K-Means,Onestep impu=1,1,1
"""

# libraries import 
import pandas as pd
import numpy as np
import sys, os
import math
from bitarray import bitarray

# import gene normalization function
from binarization.normalize import geneNorm
# import interpolation function
from binarization.interpolation import interpolation
# import functions that call C code of threshold algorithms
from threshold_methods.methods import call_C_BASC, call_C_kmeans, call_C_Stepminer, call_C_shmulevich, K_Means #### VERIFICAR COMMENTS

# import functions that create network (of binarizations) and elected methodology
from networks.networks import create_boolean_network, create_boolean_network_votes

# import MissForest imputation
from imputation.imputation_ml import imputate_missforest
# import function to extract displacement from displacement table
from displacements.displacementMatrixes import getDisplacement   #### VERIFICAR COMMENTS
# import function to call probabilistic C code
from statistics_methods.stringProbabilistic import run as run_stats

# import functions to run Bestfit inference
from inference_methods.BooleanModeling2post.BinInfer import run
# import functions to run Logicgep inference
from inference_methods.logicgep import LogicGep
# import functions to run MIBNI inference
from inference_methods.mibni.Mibni import Mibni

# import function to create BN from boolean functions
from networks.network_rule import createNetwork
# import function to extract path from BN based on initial state
from networks.hamming import extract_path

# import functions to calculate Metrics, and dynamic accuracy
from networks.metrics import Metrics, dynamic_accuracy

# read displacement table
displacements = pd.read_csv("./displacements/Displacements.csv")


def get_threshold(data, selected_methods):
    """
        get_threshold - computes the threshold of data based on selected thr methods

        data: gene expression data
        selected_methods: threshold methods to use
    """
    
    # remove labels of genes
    df1 = data.loc[:, data.columns!='Gene ID']

    # dictionaries for each threshold method
    thr_k = {}
    thr_b = {}
    thr_o = {}
    thr_s = {}

    # dictionary for spline of genes
    splineDict = {}

    # sort selected genes
    selected_rows = [i for i in range(len(df1))]

    # iterate each selected gene and interpolate
    for row in selected_rows:
        
        # get gene from dataset
        selected = df1.iloc[row]

        # extract values
        gene = selected.values

        # interpolate gene 2^k(n-1)+1
        splineGene = interpolation(gene)

        # save gene spline
        splineDict[row] = splineGene

    #print(splineDict)

    # iterate selected methods
    for method in selected_methods:

        # iterate each selected gene
        for row in selected_rows:

            # extract spline of gene
            splineGene = splineDict[row]

            # get basc threshold 
            if(method == 'BASC A'):

                thr = call_C_BASC(splineGene.copy())

                # save thr in dict
                thr_b[row] = thr

            # get onestep threshold 
            elif(method == 'Onestep'):
                thr = call_C_Stepminer(splineGene)

                # save thr in dict
                thr_o[row] = thr

            # get shmulevich threshold 
            elif(method == 'Shmulevich'):
            
                thr = call_C_shmulevich(splineGene)

                # save thr in dict
                thr_s[row] = thr

            # get kmeans threshold 
            elif(method == 'K-Means'):
            
                thr = K_Means(splineGene)

                # save thr in dict
                thr_k[row] = thr

    # return computed thresholds
    return thr_b, thr_k, thr_o

def statistics(data, gene_binarization, method, thr_methods_selected):
            """
                statistics - computes string with the highest probability and the current probability of a string

                data: gene expression data
                gene_binarization - binarization of gene expression based on framework
                method - threshold method to calculate probability
                thr_methods_selected - thr methods selected
            """
    
            # get labels of genes
            labels = data['Gene ID']

            # remove columns with labels
            data = data.loc[:, data.columns!='Gene ID']
            
            # rows of dataset
            rows = [i for i in range(len(data))]

            # get selected gene expressions
            genes = data.iloc[rows].values.astype(float)

            # organize labels 
            labels = [labels[i] for i in rows]

            # to save highest probability string of each gene expression
            string_dict = {} 


            # iterate selected genes
            for i in range(len(genes)):
                
                # get displacement table of the current thr methdod and gene
                if method != 'Elected':
                    disps = getDisplacement([method], genes[i])
                    

                # compute the probabilistic string using BASC A
                if(method == 'BASC A'):
                    print("basc stats")
                    
                    # read the displacement of basc
                    d = disps['BASC_A'].iloc[0]

                    # turn binarization to dataframe
                    df = pd.DataFrame(gene_binarization)

                    # save original binarization
                    og_binarization = df[labels[i]].values

                    # save original binarization as string
                    binary = "".join(str(x) for x in og_binarization)

                    # compute the highest probability string, highest probability, and probability of original binarization
                    # using BASC A
                    high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'BASC_A', binary) #call_C_statistics(genes[i], d, 'BASC_A', binary)

                    # save highest string
                    highest = high_string

                # compute the probabilistic string using k-means
                elif(method == 'K-Means'):
                    print("kmeans stats")
                    
                    # read the displacement of k-means
                    d = disps['k-means'].iloc[0]

                    # turn binarization to dataframe
                    df = pd.DataFrame(gene_binarization)

                    # save original binarization
                    og_binarization = df[labels[i]].values

                    # save original binarization as string
                    binary = "".join(str(x) for x in og_binarization)

                     # compute the highest probability string, highest probability, and probability of original binarization
                    # using k-means
                    high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'k-means', binary) #call_C_statistics(genes[i], d, 'k-means', binary)

                    # save highest string
                    highest = high_string
            
                # compute the probabilistic string using onestep
                elif(method == 'Onestep'):
                    print("onestep stats")
                    
                    # read the displacement of onestep
                    d = disps['onestep'].iloc[0]

                    # turn binarization to dataframe
                    df = pd.DataFrame(gene_binarization)

                    # save original binarization
                    og_binarization = df[labels[i]].values

                     # save original binarization as string
                    binary = "".join(str(x) for x in og_binarization)

                     # compute the highest probability string, highest probability, and probability of original binarization
                    # using onestep
                    high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'onestep', binary) #call_C_statistics(genes[i], d, 'onestep', binary)

                    # save highest string
                    highest = high_string

                # compute the probabilistic string using elected
                elif method == 'Elected':
                    
                    # to save highest strings and probability of each threshold method
                    high_probs = []
                    strings_probs = []

                    # read gene binarization (elected)
                    df1 = pd.DataFrame(gene_binarization)

                    # save binarization values of gene 
                    og_binarization = df1[labels[i]].values

                    print("doing elected stats")
                    
                    # iterate across selected threshold methods
                    for m in thr_methods_selected:
                        
                        # get the displacement table of thr method and based on gene range
                        disps = getDisplacement([m], genes[i])
                        
                        # if thr method is BASC A
                        if m == 'BASC A':
                            # get the displacement
                            d = disps['BASC_A'].iloc[0]

                            # read gene binarizatinon table 
                            df = pd.DataFrame(gene_binarization)

                            # get original gene binarization values of gene
                            og_bina = df[labels[i]].values
                            
                            # save binarization as string 
                            binary = "".join(str(x) for x in og_bina)

                             # compute the highest probability string, highest probability, and probability of original binarization
                            # using basc
                            high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'BASC_A', binary) #call_C_statistics(genes[i], d, 'BASC_A', binary)

                            # save highest string and probability 
                            high_probs.append(high_p)
                            strings_probs.append(high_string)
                        
                        # if thr method is Onestep
                        elif m == 'Onestep':
                            # get the displacement
                            d = disps['onestep'].iloc[0]

                             # read gene binarizatinon table 
                            df = pd.DataFrame(gene_binarization)

                            # get original gene binarization values of gene
                            og_bina = df[labels[i]].values

                             # save binarization as string 
                            binary = "".join(str(x) for x in og_bina)

                             # compute the highest probability string, highest probability, and probability of original binarization
                            # using onestep
                            high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'onestep', binary) #call_C_statistics(genes[i], d, 'onestep', binary)

                            # save highest string and probability 
                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                        # if thr method is k-means
                        elif m == 'K-Means':
                            # get the displacement
                            d = disps['k-means'].iloc[0]

                             # read gene binarizatinon table 
                            df = pd.DataFrame(gene_binarization)

                            # get original gene binarization values of gene
                            og_bin = df[labels[i]].values

                             # save binarization as string 
                            binary = "".join(str(x) for x in og_bin)

                             # compute the highest probability string, highest probability, and probability of original binarization
                            # using onestep
                            high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'k-means', binary) #call_C_statistics(genes[i], d, 'k-means', binary)

                            # save highest string and probability 
                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                        # if thr method is shmulevich
                        else:
                            # get the displacement
                            d = disps['shmulevich'].iloc[0]

                             # read gene binarizatinon table 
                            df = pd.DataFrame(gene_binarization)

                            # get original gene binarization values of gene
                            og_bin = df[labels[i]].values

                            # save binarization as string 
                            binary = "".join(str(x) for x in og_bin)

                            # compute the highest probability string, highest probability, and probability of original binarization
                            # using shmulevich
                            high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'shmulevich', binary) #call_C_statistics(genes[i], d, 'shmulevich', binary)

                            # save highest string and probability 
                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                    # get the highest probability from the list
                    max_value = max(high_probs)

                    # get the index of that highest prob
                    max_index = high_probs.index(max_value)
                    print("ended elected stats")
                    
                    # save the string of the highest prob
                    highest = strings_probs[max_index]
                
                # compute the probabilistic string using shmulevich 
                else:
                    print("shmulevich stats")
                    
                     # read the displacement of shmulevich
                    d = disps['shmulevich'].iloc[0]

                    # turn binarization to dataframe
                    df = pd.DataFrame(gene_binarization)

                     # get original gene binarization values of gene
                    og_binarization = df[labels[i]].values

                     # save binarization as string 
                    binary = "".join(str(x) for x in og_binarization)

                    # compute the highest probability string, highest probability, and probability of original binarization
                    # using shmulevich
                    high_p, high_string, p = run_stats(genes[i], d, len(genes[i]), 'shmulevich', binary) #call_C_statistics(genes[i], d, 'shmulevich', binary)

                    # save highest string
                    highest = high_string

                # saves the changes in the original binarization using probabilistic string
                array_high_P = []

                # iterate across binarized gene 
                for j in range(len(og_binarization)):
                    
                    # if the current binarization has ? and the highest string has 0 or 1 then append 0 or 1 values
                    if og_binarization[j] == '?' and highest[j] != '?':
                        # appends changes in the binarization
                        array_high_P.append(int(highest[j]))
                    # keep the original state as it is 
                    else:
                        array_high_P.append(og_binarization[j])

        
                # save the imputation to the dictionary
                string_dict[labels[i]] = array_high_P


            # turn the imputation to dataframe
            df = pd.DataFrame(string_dict)
            
            return df


def download_metrics(data, selected_rows, thr_methods, elected, kmeans, shmulevich, basc, onestep, rules_uploaded, inference_methods):
        """
                download_metrics - downloads the metrics of selected inference methods based on binarizations, and datasets

                data - gene expression dataset
                selected_rows - selected genes
                thr_methods = selected threshold methods
                elected - elected binarization
                kmeans - kmeans binarization
                shmulevich - shmulevich binarization
                basc - basc a binarization
                onestep - onestep binarization
                rules_uploaded - Boolean Functions
                inference_methods - selected inferece methods
        """

        # save gene expression dataset
        dict_data = {}

        # read gene exp
        df_data = pd.DataFrame(data)

        # get labels of genes
        labels = df_data['Gene ID']

        # remove labels of genes
        df_data = df_data.loc[:, df_data.columns!='Gene ID']

        # get selected genes from dataset
        for row in selected_rows:
            dict_data[labels[row]] = df_data.iloc[row]

        # dataframe with selected genes
        df_data = pd.DataFrame(dict_data)

        # make sure dataset is numeric
        df_data = df_data.apply(pd.to_numeric)

        # make sure indexes are ints
        df_data.index = df_data.index.astype(int)
        
        # append elected label to selected thr methods
        thr_methods = thr_methods + ['Elected']

        # to save metrics computations 
        metrics_data = []
        
    
        # iterate across selected inferece methods
        for m in inference_methods:

            # iterate across thr methods selected
            for m_thr in thr_methods:

                print(f"runnng {m} on {m_thr}")

                # get the elected binarization
                if m_thr == "Elected":
                    print(m_thr)
                    bin_dict = elected
                    df_binary = pd.DataFrame(elected)

                # get the basca binarization
                elif m_thr == "BASC A":
                    print(m_thr)
                    bin_dict = basc
                    df_binary = pd.DataFrame(basc)

                # get the onestep binarization
                elif m_thr == "Onestep":
                    print(m_thr)
                    bin_dict = onestep
                    df_binary = pd.DataFrame(onestep)

                # get the kmeans binarization
                elif m_thr == "K-Means":
                    print(m_thr)
                    bin_dict = kmeans
                    df_binary = pd.DataFrame(kmeans)

                # get the shmulevich binarization
                else:
                    print(m_thr)
                    bin_dict = shmulevich
                    df_binary = pd.DataFrame(shmulevich)
                
                # make sure binarization selected has no undecided state
                if (df_binary == '?').any().any():
                    string = f"{m_thr} binarization has '?' values cannot download metrics. Either eliminate that binarization or remove '?' values."

                    # return error
                    return string, None, None

                # make sure binarization is numeric and indexes are ints
                df_binary = df_binary.apply(pd.to_numeric)
                df_binary.index = df_binary.index.astype(int)

                # LogicGep inference logic to compute metrics
                if m == "LogicGep":
                    print(m)
                    
                    # run LogicGep inference 
                    df_infer_rules = LogicGep(df_binary, df_data)

                    # create network based on inferred rules
                    net, dict_net = createNetwork(df_infer_rules)

                    # get first state of binarization
                    state = df_binary.iloc[0].values
                    state = ''.join(str(s) for s in state)

                    # extract path from infered BN based on first state
                    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                    print("get dyn and metrics")
                        
                    # comute dynamic accuracy
                    df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)
                        
                    # if dynamic accuracy cannot be calculated save message
                    if df_dyn_acc == None:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                        
                    # save dynamic accuracy in dataframe
                    else:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                    # compute metrics between ground truth and inferred Boolean functions
                    metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)
                       
                    # dict to save metrics file rows 
                    metric_dict = {}

                    # save the inference method
                    metric_dict['Method'] = m

                    # save the binarization method
                    metric_dict['Binarization'] = m_thr

                    # save the dynamic accuracy 
                    metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                            
                    # based on computed metrics (accuracy, recall, etc) save those to dictionary
                    for metr in metrics:
                        # saves accuracy, recall, precision, f1-score to dictionary
                        metric_dict[metr] = metrics[metr][0]

                    # append metrics dictionary to metrics data list to convert later to dataframe
                    metrics_data.append(metric_dict)
                    

                # MIBNI inference logic to compute metrics
                elif m == 'MIBNI':
                    print(m)
                    
                    # infer rules using Mibni
                    mibni = Mibni(10, df_binary, "dynamics.tsv")
                    # run MIBNI object and get inferred functions
                    result = mibni.run()

                    # save infered boolean functions in dataframe
                    rules_infered = {'Gene':[],
                                    'Rule':[]}
                    
                    # save rules in dictionary
                    for r in result:

                        rul = r.split(" = ")
                        rules_infered['Gene'].append(rul[0])
                        rules_infered['Rule'].append(rul[1])

                    # turn rules to dataframe
                    df_infer_rules = pd.DataFrame(rules_infered)
                    
                # BESTFIT inference logic to compute metrics
                else:
                    print(m)
                 
                    # to save binarizations 
                    data = {}
            
                    # iterate binarization dataframe
                    for i in df_binary:
                        
                        # turn gene binarization values to list
                        nums = list(df_binary[i].values)
                        
                        # turn each state to a string
                        nums = [str(int(i)) for i in nums]
                        
                        # join binarization states as a single string 
                        array_nums = "".join(nums)
                        
                        # add binarization string as a bitarray to dictionary
                        data[i] = bitarray(array_nums)
  
                        # infer boolean functions using Bestfit
                    rules = run(data, 100, 0.05)
                        
                    # turn inferred rules to dataframe
                    df_infer_rules = pd.DataFrame(rules)

                    # create network based on inferred rules
                    net, dict_net = createNetwork(df_infer_rules)

                    # get first state of binarization
                    state = df_binary.iloc[0].values
                    state = ''.join(str(s) for s in state)

                    # extract path from infered BN based on first state
                    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                    print("get dyn and metrics")
                        
                    # compute dynamic accuracy
                    df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

                    # if dynamic accuracy cannot be computed save message
                    if df_dyn_acc == None:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                    # save dynamic accuracy computed 
                    else:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                    # compute the accuracy, recall, precision, and f1 based on inferred rules, and groundtruth rules
                    metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)
                      
                    # dict to save new row (csv) metrics data
                    metric_dict = {}

                    # save inferece method
                    metric_dict['Method'] = m

                    # save binarization method
                    metric_dict['Binarization'] = m_thr

                    # save dynamic accuracy 
                    metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                            
                    # iterate across accuracy, recall, precision, and f1 and save scores 
                    for metr in metrics:
                            metric_dict[metr] = metrics[metr][0]

                    # save dictionary to list signifying a new row to csv
                    metrics_data.append(metric_dict)
                    
                
                
                # compute metrics of MIBNI inference
                if m == "MIBNI":
                    
                    # create network based on inferred rules
                    net, dict_net = createNetwork(df_infer_rules)

                    # get first state of binarization
                    state = df_binary.iloc[0].values
                    state = ''.join(str(s) for s in state)

                    # extract path from infered BN based on first state
                    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                    print("get dyn and metrics")
                    
                    # compute dynamic accuracy
                    df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

                    # save dynamic accuracy or a message if not able to be computed 
                    if df_dyn_acc == None:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                    
                    else:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                    # compute metrics of inferred functions and groundtruth
                    metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)

                    # dict for a new row 
                    metric_dict = {}

                    # save inference method
                    metric_dict['Method'] = m

                    # save binarization method
                    metric_dict['Binarization'] = m_thr

                    # save dynamic accuracy
                    metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                        
                    # save accuracy, recall, precision, f1 score 
                    for metr in metrics:
                        metric_dict[metr] = metrics[metr][0]

                    
                    # add new dict (row) to metrics list
                    metrics_data.append(metric_dict)
        
        
        # turn metrics list to dataframe. This represents all the metrics scores computed for all inference methods, binarizations. 
        metrics_df = pd.DataFrame(metrics_data)
        
        return metrics_df


# python run.py data=P53-MDM2/data.csv,ecoli_data/Exp4.csv rules=P53-MDM2/rules.csv,ecoli_data/rules.csv inf=Bestfit,MIBNI bin=BASCA,K-Means,Onestep impu=1,2

if __name__ == "__main__":
    
    # so save input arguments from terminal
    input_arguments = {'data':[], 'rules':[], 'inf':[], 'bin':[], 'impu':[]}
    
    # iterate across arguments from terminal
    for arg in sys.argv:
        #print(arg)
        
        # if argument has no "=" then return error
        if ".py" not in arg and "=" not in arg:
            raise TypeError("Wrong argument "+arg)

        # save argument to dictionary
        if ".py" not in arg:
            # split argument name and the values
            name, value = arg.split("=")
            
            # save arguments to dict 
            if name == "data" or name == "rules" or name == "inf" or name == "bin" or name=="impu":
                # split in case of list 
                input_arguments[name] = value.split(",")
                
    #print(input_arguments)

    # save datasets names and path
    datasets = {}
    
    # iterate across input gene datasets and rules 
    for d, r in zip(input_arguments['data'], input_arguments['rules']):
        
        # get system name 
        name = d.split("/")[0]
        
        # save for each biological system the gene expression and rules files path 
        datasets[name] = ["../datasets/"+d, "../datasets/"+r]
    
    # get thr methods from input 
    thr_methods = input_arguments['bin']
    
    # modify BASCA to BASC A
    for i in range(len(thr_methods)):
        if thr_methods[i] == "BASCA":
            thr_methods[i] = "BASC A"
    
    # get inference methods from input 
    inference_methods = input_arguments['inf']
    
    # iterate across datasets, and corresping imputation to use on dataset
    for data, impu in zip(datasets, input_arguments['impu']):
        
        print(datasets[data][0])
        
        # read gene expression
        gene_expr = pd.read_csv(datasets[data][0], header=None)
        
        # normalize each row of the dataframe 
        gene_normalized = geneNorm(gene_expr.loc[ : , gene_expr.columns!=0].copy())
    
        # insert name of genes as first column
        gene_normalized.insert(0, 'Gene ID', gene_expr[0])
        
        # obtain the thresholds based on gene expression, and thr methods
        basc_thr, kmeans_thr, onestep_thr = get_threshold(gene_normalized, thr_methods)
        
        # save thr to dict 
        basc_thr = {str(k): v for k, v in basc_thr.items()}
        kmeans_thr = {str(k): v for k, v in kmeans_thr.items()}
        onestep_thr = {str(k): v for k, v in onestep_thr.items()}
        
        # get list of rows indexes
        selected_genes = [i for i in range(len(gene_normalized))]
        
        # obtain gene names 
        labels = list(gene_expr[0].values)
        
        # remove labels from normalized data
        gene_norm_noLabels = gene_normalized.loc[:, gene_normalized.columns!='Gene ID']
        
        #print(gene_norm_noLabels)
        
        # initialize each dataframe (to prevent comparing each one later and double counting) this is to verify which binarizations are the same
        basc_miss = pd.DataFrame({'a':[-1]})
        kmeans_miss = pd.DataFrame({'a':[-2]})
        onestep_miss = pd.DataFrame({'a':[-3]})
        elected_miss = pd.DataFrame({'a':[-4]})
        basc_probabilistic_probs_miss = pd.DataFrame({'a':[-5]})
        kmeansprobabilistic_probs_miss = pd.DataFrame({'a':[-6]})
        onestep_probabilistic_probs_miss = pd.DataFrame({'a':[-7]})
        elected_probabilistic_probs_miss = pd.DataFrame({'a':[-8]})
        
        # iterate across thr methods 
        for thr in thr_methods:
            
            # if method is basc imputate 
            if thr == "BASC A":
                
                # create binrization based on basca threshold (based on framework)
                basc_binarizations = create_boolean_network(selected_genes, thr, gene_norm_noLabels, displacements,
                                                            [], [], [], basc_thr, labels)
                
                # imputate undecided values with missforest
                basc_miss = pd.DataFrame(imputate_missforest(basc_binarizations.to_dict(orient='records')).copy()).astype(int)
                
                # if imputation was not set as only MissForest do probabilistic + Missforest
                if impu != '2':
                    # imputate using probabilistics
                    basc_probabilistic = statistics(gene_normalized, basc_binarizations, thr, thr_methods)
                
                    # imputate remaining values using MissForest
                    basc_probabilistic_probs_miss = pd.DataFrame(imputate_missforest(basc_probabilistic.to_dict(orient='records')).copy()).astype(int)
                    
                
            # if method is kmeans imputate  
            elif thr == "K-Means":
                
                # create binrization based on kmeans threshold (based on framework)
                kmeans_binarizations = create_boolean_network(selected_genes, thr, gene_norm_noLabels, displacements,
                                                              kmeans_thr, [], [], [], labels)
                
                 # imputate undecided values with missforest
                kmeans_miss = pd.DataFrame(imputate_missforest(kmeans_binarizations.to_dict(orient='records'))).astype(int)
                
                # if imputation was not set as only MissForest do probabilistic + Missforest
                if impu != '2':
                    # imputate using probabilistics
                    kmeans_probabilistic = statistics(gene_normalized, kmeans_binarizations, thr, thr_methods)
                
                    # imputate remaining values using MissForest
                    kmeansprobabilistic_probs_miss = pd.DataFrame(imputate_missforest(kmeans_probabilistic.to_dict(orient='records'))).astype(int)
                
            # if method is onestep imputate
            elif thr == "Onestep":
                
                 # create binrization based on onestep threshold (based on framework)
                onestep_binarizations = create_boolean_network(selected_genes, thr, gene_norm_noLabels, displacements,
                                                               [], onestep_thr, [], [], labels)
                
                # imputate undecided values with missforest
                onestep_miss = pd.DataFrame(imputate_missforest(onestep_binarizations.to_dict(orient='records'))).astype(int)
                
                # if imputation was not set as only MissForest do probabilistic + Missforest
                if impu != '2':
                    # imputate using probabilistics
                    onestep_probabilistic = statistics(gene_normalized, onestep_binarizations, thr, thr_methods)
                
                    # imputate remaining values using MissForest
                    onestep_probabilistic_probs_miss = pd.DataFrame(imputate_missforest(onestep_probabilistic.to_dict(orient='records'))).astype(int)
                
        
        # create binarization based on elected (based on framework)
        elected_binarizations = create_boolean_network_votes(selected_genes, gene_norm_noLabels, thr_methods, displacements, kmeans_thr, onestep_thr,
                                                             {}, basc_thr, labels)
        
        # imputate undecided values with missforest
        elected_miss = pd.DataFrame(imputate_missforest(elected_binarizations.to_dict(orient='records'))).astype(int)
        
        # if imputation was not set as only MissForest do probabilistic + Missforest
        if impu != '2':
                # imputate using probabilistics
                elected_probabilistic = statistics(gene_normalized, elected_binarizations, "Elected", thr_methods)
                
                # imputate remaining values using MissForest
                elected_probabilistic_probs_miss = pd.DataFrame(imputate_missforest(elected_probabilistic.to_dict(orient='records'))).astype(int)
                
        
        # read selected Boolean functions 
        rules_uploaded = pd.read_csv(datasets[data][1], header=0)
        
        # if a gene has no rule save the rule as empty string
        for index, row in rules_uploaded.iterrows():
            if pd.isna(row['Rule']):
                rules_uploaded.loc[index, 'Rule'] = ''
            elif not row['Rule'].strip():
                rules_uploaded.loc[index, 'Rule'] = ''
        
        # turn rules to dict 
        rules_uploaded.to_dict(orient='records')
        
        # save binarizations for each imputation in list
        compare_dfs = [basc_miss, kmeans_miss, onestep_miss, elected_miss, basc_probabilistic_probs_miss, kmeansprobabilistic_probs_miss,
                       onestep_probabilistic_probs_miss, elected_probabilistic_probs_miss]
        
        # labels of each bnarization and imputation
        compare_labels = ["basc_miss", "kmeans_miss", "onestep_miss", "elected_miss", "basc_probs", "kmeans_probs", "onestep_probs", "elected_probs"]
        
        # dictionary to save wich binarization and imputation are equal 
        compare_dict = {'Same binarization':[], 'Diff binarization':[]}
        
        # iterate binarizations 
        for i in range(len(compare_dfs)):
            
            # iterate labels 
            for j in range(i+1, len(compare_labels)):
                
                # if binarizations are equal save in equal column
                if compare_dfs[i].equals(compare_dfs[j]):   
                    
                    compare_dict['Same binarization'].append(f"{compare_labels[i]}, {compare_labels[j]}")
                    compare_dict['Diff binarization'].append("")
                
                # if binarizations are not equal save in not equal column
                else:
                    
                    compare_dict['Same binarization'].append("")
                    compare_dict['Diff binarization'].append(f"{compare_labels[i]}, {compare_labels[j]}")
        
        # create dataframe with comparison
        df_compare = pd.DataFrame(compare_dict)
        
        # save comparison dataframe as csv
        df_compare.to_csv(f'../metrics/{data}_binarization_comparison.csv', index=True) 
        
        # iterate to calculate and save metrics as csv
        for j in range(2):
            
            # save metrics of binarization imputed with only missforest impuation
            if j == 0:
                
                # get metrics results 
                res = download_metrics(gene_normalized, selected_genes, thr_methods, elected_miss, kmeans_miss, [], basc_miss, onestep_miss, rules_uploaded, inference_methods)
                
                # turn metrics to dataframe
                df_res = pd.DataFrame(res)
                
                # save dataframe as csv
                df_res.to_csv(f'../metrics/{data}_miss.csv', index=True) 
                
                elected_miss.to_csv(f'../metrics/binarization/{data}_elected_binarization_miss.csv', index=False) 
                kmeans_miss.to_csv(f'../metrics/binarization/{data}_kmeans_binarization_miss.csv', index=False) 
                basc_miss.to_csv(f'../metrics/binarization/{data}_basc_binarization_miss.csv', index=False) 
                onestep_miss.to_csv(f'../metrics/binarization/{data}_onestep_binarization_miss.csv', index=False) 
                
            # save metrics of binarization imputed with probablistic + missforest imputation  
            elif j == 1 and impu != '2':
                
                # get metrics results 
                res = download_metrics(gene_normalized, selected_genes, thr_methods, elected_probabilistic_probs_miss, 
                                       kmeansprobabilistic_probs_miss, [], basc_probabilistic_probs_miss, onestep_probabilistic_probs_miss, rules_uploaded, inference_methods)
                
                # turn metrics to dataframe
                df_res = pd.DataFrame(res)
                
                # save dataframe as csv
                df_res.to_csv(f'../metrics/{data}_probs.csv', index=True) 
                
                elected_probabilistic_probs_miss.to_csv(f'../metrics/binarization/{data}_elected_binarization_probs.csv', index=False) 
                kmeansprobabilistic_probs_miss.to_csv(f'../metrics/binarization/{data}_kmeans_binarization_probs.csv', index=False) 
                basc_probabilistic_probs_miss.to_csv(f'../metrics/binarization/{data}_basc_binarization_probs.csv', index=False) 
                onestep_probabilistic_probs_miss.to_csv(f'../metrics/binarization/{data}_onestep_binarization_probs.csv', index=False) 
                
                    
