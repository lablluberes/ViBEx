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
         The ones offered are: 1: probabilistic (complete) and missforest, and only missforest, 2: only missforest, 
                               3: (1) and probabilistic (time) and missforest
         Example to run: impu=1,2
    
    To run this code using an example use the following command:
        
        python script.py data=P53-MDM2/data.csv,yeast_cell/yeast_data_elu.csv,ecoli_data/Exp4.csv rules=P53-MDM2/rules.csv,yeast_cell/rules.csv,ecoli_data/rules.csv inf=MIBNI,LogicGep,Bestfit bin=BASCA,K-Means,Onestep
"""

# libraries import 
import pandas as pd
import numpy as np
import sys, os
import math
from bitarray import bitarray
from itertools import chain, combinations

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

from statistics_methods.probImpute import build_kde_cdf, binarize_and_impute_matrix_with_probs_multi_methods

# read displacement table
displacements = pd.read_csv("./displacements/Displacements.csv")

thrs = pd.read_csv('./statistics_methods/thrs.csv')
    
thrsBasc = list(thrs['basca'].values)
thrsOnestep = list(thrs['onestep'].values)
thrsKmeans = list(thrs['kmeans'].values)
thrsShmulevich = list(thrs['shmulevich'].values)
    
cdfBasc = build_kde_cdf(thrsBasc)
cdfOnestep = build_kde_cdf(thrsOnestep)
cdfKmeans = build_kde_cdf(thrsKmeans)
cdfShmulevich = build_kde_cdf(thrsShmulevich)

cdf_dict = {'BASC A':cdfBasc, 'K-Means':cdfKmeans, 'Onestep': cdfOnestep, 'Shmulevich': cdfShmulevich}

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


###### Added function for elected string alg

def election_strings(gene, thr_list, disp_list):
    """
        election_strings - makes election strings and binarizes genes

        gene: gene expression
        thr_list: list of threshold values
        disp_list: list of displacement of gene
    """

    z_e = []

    for j in range(len(gene)):

      store = []

      for i in range(len(thr_list)):

        U = (gene[j]+disp_list[i] < thr_list[i]) and (abs(thr_list[i] - gene[j]) > disp_list[i])
        N = abs(thr_list[i] - gene[j]) <= disp_list[i]
        E = not(U or N)

        store.append(np.array([N, U, E]))

      store = np.array(store)

      # verify ties for N, U, E
      count1N = list(store[:,0]).count(1)
      count0N = list(store[:,0]).count(0)
      count1U = list(store[:,1]).count(1)
      count0U = list(store[:,1]).count(0)
      count1E = list(store[:,2]).count(1)
      count0E = list(store[:,2]).count(0)


      # get majority for N, U, E
      majN = max(set(store[:,0]), key=list(store[:,0]).count)
      majU = max(set(store[:,1]), key=list(store[:,1]).count)
      majE = max(set(store[:,2]), key=list(store[:,2]).count)

      if majE != (not(majU or majN)) or majN == 1 or (count0N == count1N) or (count1E == count0E) or (count0U == count1U):
        z_e.append(np.nan)
      elif majE == 1:
        z_e.append(1)
      else:
        z_e.append(0)

    return z_e


def dataframeComparison(compare_dfs, compare_labels):
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
        df_compare.to_csv(f'../new_metrics/{data}/binarizations/{data}_bin_comparison.csv', index=False) 
        
        
def getMetrics(data, selected_rows, power_set, inference_methods, binarizations, binarization_labels, rules_uploaded, name, typeImpu):
    
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
    
    metrics_data = []
    
    for m in inference_methods:
        
        for bin, p, label in zip(binarizations, power_set, binarization_labels):
            
            # make sure binarization is numeric and indexes are ints
            df_binary = bin.apply(pd.to_numeric)
            df_binary.index = bin.index.astype(int)
            
            # LogicGep inference logic to compute metrics
            if m == "LogicGep":
                    print(m, label)
                    
                    # run LogicGep inference 
                    df_infer_rules = LogicGep(df_binary, df_data)
                    
                    df_infer_rules.to_csv(f'../new_metrics/{name}/functions/LogicGep_functions_{label}.csv', index=False)

                    # create network based on inferred rules
                    net, dict_net = createNetwork(df_infer_rules)

                    # get first state of binarization
                    state = df_binary.iloc[0].values
                    state = ''.join(str(s) for s in state)

                    # extract path from infered BN based on first state
                    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                    #print("get dyn and metrics")
                        
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
                    metric_dict['Binarization'] = "{" + ", ".join(p) + "}"

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
                    print(m, label)
                    
                    #print(df_binary)
                    
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
                    
                    df_infer_rules.to_csv(f'../new_metrics/{name}/functions/MIBNI_functions_{label}.csv', index=False)
                    
                # BESTFIT inference logic to compute metrics
            else:
                    print(m, label)
                 
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
                    
                    df_infer_rules.to_csv(f'../new_metrics/{name}/functions/bestfit_functions_{label}.csv', index=False)

                    # create network based on inferred rules
                    net, dict_net = createNetwork(df_infer_rules)

                    # get first state of binarization
                    state = df_binary.iloc[0].values
                    state = ''.join(str(s) for s in state)

                    # extract path from infered BN based on first state
                    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                    #print("get dyn and metrics")
                        
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
                    metric_dict['Binarization'] = "{" + ", ".join(p) + "}"

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

                    #print("get dyn and metrics")
                    
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
                    metric_dict['Binarization'] = "{" + ", ".join(p) + "}"

                    # save dynamic accuracy
                    metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                        
                    # save accuracy, recall, precision, f1 score 
                    for metr in metrics:
                        metric_dict[metr] = metrics[metr][0]

                    
                    # add new dict (row) to metrics list
                    metrics_data.append(metric_dict)
        
        
    # turn metrics list to dataframe. This represents all the metrics scores computed for all inference methods, binarizations. 
    metrics_df = pd.DataFrame(metrics_data)
        
    metrics_df.to_csv(f'../new_metrics/{name}/metrics/{name}_{typeImpu}.csv', index=False)
        
     #return metrics_df


# python script.py data=P53-MDM2/data.csv rules=P53-MDM2/rules.csv inf=MIBNI,LogicGep,Bestfit bin=BASCA,K-Means,Onestep

if __name__ == "__main__":
    
    # so save input arguments from terminal
    input_arguments = {'data':[], 'rules':[], 'inf':[], 'bin':[]}
    
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
            if name == "data" or name == "rules" or name == "inf" or name == "bin":
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
    
    # power set of thr methods
    power_set = list(chain.from_iterable(combinations(thr_methods, r) for r in range(len(thr_methods) + 1)))
    
    power_set = [p for p in power_set if len(p) > 0]
    
    #print(power_set)
    
    for i, data in enumerate(datasets):
        
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
        
        thresholds = {'BASC A': basc_thr, 'K-Means': kmeans_thr, 'Onestep': onestep_thr}
        
        # get list of rows indexes
        selected_genes = [i for i in range(len(gene_normalized))]
        
        # obtain gene names 
        labels = list(gene_expr[0].values)
        
        # remove labels from normalized data
        gene_norm_noLabels = gene_normalized.loc[:, gene_normalized.columns!='Gene ID']
        #print(gene_norm_noLabels)
        
        binarizationsMiss = []
        binarization_labelsMiss = []
        
        binarizationsProb = []
        binarization_labelsProb = []
        
        for j, method in enumerate(power_set):
            
            print(method)
            
            #thrs = []
            #disp = []
            
            og_bin = pd.DataFrame(columns=labels)
            prob_bin = pd.DataFrame(columns=labels)
            
            for label, idx in zip(labels, selected_genes):
                g = list(gene_norm_noLabels.loc[idx])
                #print(g)
                thrs = []
                cdfList = []
                
                for m in method:
                    
                    cdfList.append(cdf_dict[m])
                    
                    thrs.append(thresholds[m][str(idx)])
                    
                disp = (list(getDisplacement(method, g).loc[0]))
                
                #print(thrs)
                #print(disp)
                
                og_bin[label] = election_strings(g, thrs, disp)
                
                prob_bin[label] = list(binarize_and_impute_matrix_with_probs_multi_methods([g], cdfList, thrs, disp, 0.5, 3)[0])
            
            df_miss = pd.DataFrame(imputate_missforest(og_bin.copy())).astype(int)
            
            df_miss.to_csv(f'../new_metrics/{data}/binarizations/{data}_{"{" + ", ".join(method) + "}"}_bin_onlyMissForest.csv', index=False)
            
            binarizationsMiss.append(df_miss)
            binarization_labelsMiss.append(f'{data}_{"{" + ", ".join(method) + "}"}_onlyMissforest')
            
            
            #print(prob_bin)
            
            prob_bin = prob_bin.fillna(-1)
            
            #print(prob_bin)
            
            prob_bin = prob_bin.astype(int)
            
            prob_bin = prob_bin.replace(-1, '?')
            
            df_probMiss = pd.DataFrame(imputate_missforest(prob_bin.copy())).astype(int)
            
            df_probMiss.to_csv(f'../new_metrics/{data}/binarizations/{data}_{"{" + ", ".join(method) + "}"}_bin_Prob_and_MissForest.csv', index=False)
            
            binarizationsProb.append(df_probMiss)
            binarization_labelsProb.append(f'{data}_{"{" + ", ".join(method) + "}"}_Prob_and_Missforest')
                
            og_bin.to_csv(f'../new_metrics/{data}/binarizations/{data}_{"{" + ", ".join(method) + "}"}_og_bin.csv', index=False)
            
            #print(len(binarizations))
            
        dataframeComparison(binarizationsMiss+binarizationsProb, binarization_labelsMiss+binarization_labelsProb)
        
        print(datasets[data][1])
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
        
        
        getMetrics(gene_normalized, selected_genes, power_set, inference_methods, binarizationsMiss, binarization_labelsMiss, rules_uploaded, data, "missforestMetrics")
        getMetrics(gene_normalized, selected_genes, power_set, inference_methods, binarizationsProb, binarization_labelsProb, rules_uploaded, data, "probsMetrics")
        
    