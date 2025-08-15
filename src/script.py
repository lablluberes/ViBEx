#########################################################
#
# Script to automatically run experiments (this file can be run individualy or the tool can be used)
# Also, experiments can be done using the tool
# Upload data, select thr methods, imputate values
# Press button run script and it will download metrics 
#
########################################################

import pandas as pd
import numpy as np
import math
from bitarray import bitarray

from binarization.normalize import geneNorm
from binarization.interpolation import interpolation
from threshold_methods.methods import call_C_BASC, call_C_kmeans, call_C_Stepminer, call_C_shmulevich

from networks.networks import create_boolean_network, create_boolean_network_votes

from imputation.imputation_ml import imputate_missforest

from displacements.displacementMatrixes import getDisplacement

from statistics_methods.stringProbabilistic import call_C_statistics

from inference_methods.BooleanModeling2post.BinInfer import run
from inference_methods.logicgep import LogicGep
from inference_methods.mibni.Mibni import Mibni

from networks.network_rule import createNetwork
from networks.hamming import extract_path

from networks.metrics import Metrics, dynamic_accuracy

displacements = pd.read_csv("./displacements/Displacements.csv")

def get_threshold(data, selected_methods):
    
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

        # interpolate gene 
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
                #thr = shmulevich(splineGene)
                thr = call_C_shmulevich(splineGene)

                # save thr in dict
                thr_s[row] = thr

            # get kmeans threshold 
            elif(method == 'K-Means'):
                #thr = K_Means(splineGene)
                thr = call_C_kmeans(splineGene)

                # save thr in dict
                thr_k[row] = thr

    
    return thr_b, thr_k, thr_o

def statistics(data, gene_binarization, method, thr_methods_selected):
    
            # get labels of genes
            labels = data['Gene ID']

            data = data.loc[:, data.columns!='Gene ID']
            
            rows = [i for i in range(len(data))]

            # get selected gene expressions
            genes = data.iloc[rows].values.astype(float)

            # organize labels 
            labels = [labels[i] for i in rows]

            string_dict = {} 


            # iterate selected genes
            for i in range(len(genes)):
                
                # displacement table
                if method != 'Elected':
                    disps = getDisplacement([method], genes[i])
                rangeIndex = math.ceil((max(genes[i])-min(genes[i]))*10) - 1

                #get PDF for gene
                #probden = pd.read_csv("./statistics_methods/cdf_"+str(rangeIndex+1)+".csv")

                # extracts displacement based on selected method
                if(method == 'BASC A'):
                    print("basc stats")
                    d = disps['BASC_A'].iloc[0]

                    df = pd.DataFrame(gene_binarization)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'BASC_A', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string
        
                elif(method == 'K-Means'):
                    print("kmeans stats")
                    d = disps['k-means'].iloc[0]

                    df = pd.DataFrame(gene_binarization)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'k-means', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string
            
                elif(method == 'Onestep'):
                    print("onestep stats")
                    d = disps['onestep'].iloc[0]

                    df = pd.DataFrame(gene_binarization)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'onestep', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string

                elif method == 'Elected':
                    
                    high_probs = []
                    strings_probs = []

                    df1 = pd.DataFrame(gene_binarization)

                    og_binarization = df1[labels[i]].values

                    print("doing elected stats")
                    for m in thr_methods_selected:
                        disps = getDisplacement([m], genes[i])
                        if m == 'BASC A':
                            d = disps['BASC_A'].iloc[0]

                            df = pd.DataFrame(gene_binarization)

                            og_bina = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bina)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'BASC_A', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)
                        
                        elif m == 'Onestep':

                            d = disps['onestep'].iloc[0]

                            df = pd.DataFrame(gene_binarization)

                            og_bina = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bina)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'onestep', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                        elif m == 'K-Means':

                            d = disps['k-means'].iloc[0]

                            df = pd.DataFrame(gene_binarization)

                            og_bin = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bin)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'k-means', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                        else:
                            d = disps['shmulevich'].iloc[0]

                            df = pd.DataFrame(gene_binarization)

                            og_bin = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bin)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'shmulevich', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                    max_value = max(high_probs)

                    max_index = high_probs.index(max_value)
                    print("ended elected stats")
                    highest = strings_probs[max_index]
                    
                else:
                    print("shmulevich stats")
                    d = disps['shmulevich'].iloc[0]

                    df = pd.DataFrame(gene_binarization)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'shmulevich', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string

                array_high_P = []

                for j in range(len(og_binarization)):

                    if og_binarization[j] == '?' and highest[j] != '?':
                        array_high_P.append(int(highest[j]))
                    #elif str(og_binarization[j]) != highest[j]:
                    #    array_high_P.append('?')
                    else:
                        array_high_P.append(og_binarization[j])

                # get probability of strings 
                #Z = probabilistic(np.array(genes[i]), [method], d)

                # highest string probability 
                #string_high_P = max(Z, key=Z.get)
                
                # save string key to array
                #array_high_P = [e for e in string_high_P]

                # save highest prob string to each gene 
                string_dict[labels[i]] = array_high_P

            #print(string_dict)

            # turn to imputation to dataframe
            df = pd.DataFrame(string_dict)
            
            return df


def download_metrics(data, selected_rows, thr_methods, elected, kmeans, shmulevich, basc, onestep, rules_uploaded):

        dict_data = {}

        # read gene exp
        df_data = pd.DataFrame(data)

        # get labels of genes
        labels = df_data['Gene ID']

        df_data = df_data.loc[:, df_data.columns!='Gene ID']

        # get selected genes from dataset
        for row in selected_rows:
            dict_data[labels[row]] = df_data.iloc[row]

        df_data = pd.DataFrame(dict_data)

        #print(df_data)
        #print(df_binary)

        # make sure dataset is numeric
        df_data = df_data.apply(pd.to_numeric)

        # make sure indexes are ints
        df_data.index = df_data.index.astype(int)
        
        thr_methods = thr_methods + ['Elected']

        metrics_data = []
        
        inference_methods = ['MIBNI', 'LogicGep', 'Bestfit']
        #= {
        #    'MIBNI':[], 'LogicGep':[], 'Bestfit':[]
        #}

        for m in inference_methods:

            for m_thr in thr_methods:

                print(f"runnng {m} on {m_thr}")

                # get a dataframe based on the selected binarization used to inference 
                if m_thr == "Elected":
                    print(m_thr)
                    bin_dict = elected
                    df_binary = pd.DataFrame(elected)

                elif m_thr == "BASC A":
                    print(m_thr)
                    bin_dict = basc
                    df_binary = pd.DataFrame(basc)

                elif m_thr == "Onestep":
                    print(m_thr)
                    bin_dict = onestep
                    df_binary = pd.DataFrame(onestep)

                elif m_thr == "K-Means":
                    print(m_thr)
                    bin_dict = kmeans
                    df_binary = pd.DataFrame(kmeans)

                else:
                    print(m_thr)
                    bin_dict = shmulevich
                    df_binary = pd.DataFrame(shmulevich)
                
                # make sure binarization selected has no undecided state
                if (df_binary == '?').any().any():
                    string = f"{m_thr} binarization has '?' values cannot download metrics. Either eliminate that binarization or remove '?' values."

                    return string, None, None

                df_binary = df_binary.apply(pd.to_numeric)
                df_binary.index = df_binary.index.astype(int)

                # logic for selected inference method
                if m == "LogicGep":
                    print(m)
                    # infer rules using LogicGep

                    dyn_arr = []
                    acc_arr = []
                    pre_arr = []
                    re_arr = []
                    fscore_arr = []

                    for i in range(15):
                        df_infer_rules = LogicGep(df_binary, df_data)
                        
                        print("LOGICGEP", i)

                        # create network based on inferred rules
                        net, dict_net = createNetwork(df_infer_rules)

                        # get first state of binarization
                        state = df_binary.iloc[0].values
                        state = ''.join(str(s) for s in state)

                        # extract path from infered BN based on first state
                        path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                        print("get dyn and metrics")
                        df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

                        if df_dyn_acc == None:
                            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                        
                        else:
                            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                        metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)
                        #metrics_dir = Metrics_directed(pd.DataFrame(rules_uploaded), df_infer_rules)

                        metric_dict = {}

                        metric_dict['Method'] = m

                        metric_dict['Binarization'] = m_thr

                        metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                            

                        for metr in metrics:
                            metric_dict[metr] = metrics[metr][0]

                        #for metr in metrics_dir:
                        #    metric_dict[metr+'(Directed Matrix)'] = metrics_dir[metr][0]

                        if metric_dict['Dynamic Accuracy'] != 'Cannot be calculated':
                      
                            dyn_arr.append(metric_dict['Dynamic Accuracy'])

                        acc_arr.append(metric_dict['Accuracy'])
                        pre_arr.append(metric_dict['Precision'])
                        re_arr.append(metric_dict['Recall'])
                        fscore_arr.append(metric_dict['F1-Score'])

                        metrics_data.append(metric_dict)
                    
                    mean_dyn = np.mean(dyn_arr)
                    mean_acc = np.mean(acc_arr)
                    mean_pre = np.mean(pre_arr)
                    mean_re = np.mean(re_arr)
                    mean_f= np.mean(fscore_arr)

                    std_dyn = np.std(dyn_arr, ddof=1)
                    std_acc = np.std(acc_arr, ddof=1)
                    std_pre = np.std(pre_arr, ddof=1)
                    std_re = np.std(re_arr, ddof=1)
                    std_f= np.std(fscore_arr, ddof=1)

                    se_dyn = std_dyn / np.sqrt(len(dyn_arr))
                    se_acc = std_acc / np.sqrt(len(acc_arr))
                    se_pre = std_pre / np.sqrt(len(pre_arr))
                    se_re = std_re / np.sqrt(len(re_arr))
                    se_f= std_f / np.sqrt(len(fscore_arr))

                    mean_row = {'Method': m, 'Binarization':m_thr, 
                                'Dynamic Accuracy': f"Mean: {mean_dyn} STD: {std_dyn} SE: {se_dyn}",
                                'Accuracy': f"Mean: {mean_acc} STD: {std_acc} SE: {se_acc}",
                                'Precision': f"Mean: {mean_pre} STD: {std_pre} SE: {se_pre}",
                                'Recall': f"Mean: {mean_re} STD: {std_re} SE: {se_re}",
                                'F1-Score': f"Mean: {mean_f} STD: {std_f} SE: {se_f}"} 
                    metrics_data.append(mean_row)


                elif m == 'MIBNI':
                    print(m)
                    # infer rules using Mibni
                    mibni = Mibni(10, df_binary, "dynamics.tsv")
                    result = mibni.run()

                    # save infered boolean functions in dataframe
                    rules_infered = {'Gene':[],
                                    'Rule':[]}
                    for r in result:

                        rul = r.split(" = ")
                        rules_infered['Gene'].append(rul[0])
                        rules_infered['Rule'].append(rul[1])

                    df_infer_rules = pd.DataFrame(rules_infered)
                    
                else:
                    print(m)
                    # infer rules using Bestfit
                    
                    data = {}
            
                    for i in df_binary:
                        nums = list(df_binary[i].values)
                        
                        nums = [str(int(i)) for i in nums]
                        
                        array_nums = "".join(nums)
                        
                        data[i] = bitarray(array_nums)

                    dyn_arr = []
                    acc_arr = []
                    pre_arr = []
                    re_arr = []
                    fscore_arr = []

                    for i in range(15):
                        
                        rules = run(data, 100, 0.05)
                        
                        df_infer_rules = pd.DataFrame(rules)
                        
                        print(i, rules, "BESTFIT")

                        # create network based on inferred rules
                        net, dict_net = createNetwork(df_infer_rules)

                        # get first state of binarization
                        state = df_binary.iloc[0].values
                        state = ''.join(str(s) for s in state)

                        # extract path from infered BN based on first state
                        path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                        print("get dyn and metrics")
                        df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

                        if df_dyn_acc == None:
                            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                        
                        else:
                            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                        metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)
                        #metrics_dir = Metrics_directed(pd.DataFrame(rules_uploaded), df_infer_rules)

                        metric_dict = {}

                        metric_dict['Method'] = m

                        metric_dict['Binarization'] = m_thr

                        metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                            

                        for metr in metrics:
                            metric_dict[metr] = metrics[metr][0]

                        #for metr in metrics_dir:
                        #    metric_dict[metr+'(Directed Matrix)'] = metrics_dir[metr][0]

                        if metric_dict['Dynamic Accuracy'] != 'Cannot be calculated':
                      
                            dyn_arr.append(metric_dict['Dynamic Accuracy'])

                        acc_arr.append(metric_dict['Accuracy'])
                        pre_arr.append(metric_dict['Precision'])
                        re_arr.append(metric_dict['Recall'])
                        fscore_arr.append(metric_dict['F1-Score'])

                        metrics_data.append(metric_dict)
                    
                    mean_dyn = np.mean(dyn_arr)
                    mean_acc = np.mean(acc_arr)
                    mean_pre = np.mean(pre_arr)
                    mean_re = np.mean(re_arr)
                    mean_f= np.mean(fscore_arr)

                    std_dyn = np.std(dyn_arr, ddof=1)
                    std_acc = np.std(acc_arr, ddof=1)
                    std_pre = np.std(pre_arr, ddof=1)
                    std_re = np.std(re_arr, ddof=1)
                    std_f= np.std(fscore_arr, ddof=1)

                    se_dyn = std_dyn / np.sqrt(len(dyn_arr))
                    se_acc = std_acc / np.sqrt(len(acc_arr))
                    se_pre = std_pre / np.sqrt(len(pre_arr))
                    se_re = std_re / np.sqrt(len(re_arr))
                    se_f= std_f / np.sqrt(len(fscore_arr))

                    mean_row = {'Method': m, 'Binarization':m_thr, 
                                'Dynamic Accuracy': f"Mean: {mean_dyn} STD: {std_dyn} SE: {se_dyn}",
                                'Accuracy': f"Mean: {mean_acc} STD: {std_acc} SE: {se_acc}",
                                'Precision': f"Mean: {mean_pre} STD: {std_pre} SE: {se_pre}",
                                'Recall': f"Mean: {mean_re} STD: {std_re} SE: {se_re}",
                                'F1-Score': f"Mean: {mean_f} STD: {std_f} SE: {se_f}"} 
                    metrics_data.append(mean_row)
                
                if m == "MIBNI":
                    # create network based on inferred rules
                    net, dict_net = createNetwork(df_infer_rules)

                    # get first state of binarization
                    state = df_binary.iloc[0].values
                    state = ''.join(str(s) for s in state)

                    # extract path from infered BN based on first state
                    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                    print("get dyn and metrics")
                    df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

                    if df_dyn_acc == None:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                    
                    else:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                    metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)
                    #metrics_dir = Metrics_directed(pd.DataFrame(rules_uploaded), df_infer_rules)

                    metric_dict = {}

                    metric_dict['Method'] = m

                    metric_dict['Binarization'] = m_thr

                    metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                        

                    for metr in metrics:
                        metric_dict[metr] = metrics[metr][0]

                    #for metr in metrics_dir:
                    #    metric_dict[metr+'(Directed Matrix)'] = metrics_dir[metr][0]


                    metrics_data.append(metric_dict)
        
        
        #return None
        #print(metrics_data)
        metrics_df = pd.DataFrame(metrics_data)
        
        return metrics_df


if __name__ == "__main__":
    
    datasets = { 
                #'yeast':['../datasets/yeast_cell/yeast_data_elu.csv', '../datasets/yeast_cell/rules.csv'], 
                'p53':['../datasets/P53-MDM2/data.csv', '../datasets/P53-MDM2/rules.csv'],
                'yeast':['../datasets/yeast_cell/yeast_data_elu.csv', '../datasets/yeast_cell/rules.csv'], 
                'ecoli':['../datasets/ecoli_data/Exp4.csv', '../datasets/ecoli_data/rules.csv'], 
                }
    thr_methods = ['BASC A', 'K-Means', 'Onestep']
    
    
    for data in datasets:
        
        print(datasets[data][0])
        
        gene_expr = pd.read_csv(datasets[data][0], header=None)
        
         # normalize each row of the dataframe 
        gene_normalized = geneNorm(gene_expr.loc[ : , gene_expr.columns!=0].copy())
    
        # insert name of genes as first column
        gene_normalized.insert(0, 'Gene ID', gene_expr[0])
        
        #print(gene_expr)
        #print(gene_normalized)
        
        basc_thr, kmeans_thr, onestep_thr = get_threshold(gene_normalized, thr_methods)
        
        basc_thr = {str(k): v for k, v in basc_thr.items()}
        kmeans_thr = {str(k): v for k, v in kmeans_thr.items()}
        onestep_thr = {str(k): v for k, v in onestep_thr.items()}
        
        #print(basc_thr, kmeans_thr, onestep_thr)
        
        selected_genes = [i for i in range(len(gene_normalized))]
        
        labels = list(gene_expr[0].values)
        
        
        gene_norm_noLabels = gene_normalized.loc[:, gene_normalized.columns!='Gene ID']
        
        #print(gene_norm_noLabels)
        
        for thr in thr_methods:
            
            if thr == "BASC A":
                basc_binarizations = create_boolean_network(selected_genes, thr, gene_norm_noLabels, displacements,
                                                            [], [], [], basc_thr, labels)
                
                basc_miss = pd.DataFrame(imputate_missforest(basc_binarizations.to_dict(orient='records')).copy()).astype(int)
                
                if data != 'ecoli':
                    basc_probabilistic = statistics(gene_normalized, basc_binarizations, thr, thr_methods)
                
                    basc_probabilistic_probs_miss = pd.DataFrame(imputate_missforest(basc_probabilistic.to_dict(orient='records')).copy()).astype(int)
                    
                #print(basc_probabilistic_probs_miss)
                
                #print(basc_miss)
                
                
            elif thr == "K-Means":
                kmeans_binarizations = create_boolean_network(selected_genes, thr, gene_norm_noLabels, displacements,
                                                              kmeans_thr, [], [], [], labels)
                kmeans_miss = pd.DataFrame(imputate_missforest(kmeans_binarizations.to_dict(orient='records'))).astype(int)
                
                
                if data != 'ecoli':
                    kmeans_probabilistic = statistics(gene_normalized, kmeans_binarizations, thr, thr_methods)
                
                    kmeansprobabilistic_probs_miss = pd.DataFrame(imputate_missforest(kmeans_probabilistic.to_dict(orient='records'))).astype(int)
                
                
            elif thr == "Onestep":
                onestep_binarizations = create_boolean_network(selected_genes, thr, gene_norm_noLabels, displacements,
                                                               [], onestep_thr, [], [], labels)
                
                onestep_miss = pd.DataFrame(imputate_missforest(onestep_binarizations.to_dict(orient='records'))).astype(int)
                
                if data != 'ecoli':
                    onestep_probabilistic = statistics(gene_normalized, onestep_binarizations, thr, thr_methods)
                
                    onestep_probabilistic_probs_miss = pd.DataFrame(imputate_missforest(onestep_probabilistic.to_dict(orient='records'))).astype(int)
                
                
                #print("og bin:", pd.DataFrame(onestep_binarizations))
                #print("prob bin:",onestep_probabilistic)
                #print("prob and miss:",pd.DataFrame(onestep_probabilistic_probs_miss))
                #print("miss:", pd.DataFrame(onestep_miss))
        
        elected_binarizations = create_boolean_network_votes(selected_genes, gene_norm_noLabels, thr_methods, displacements, kmeans_thr, onestep_thr,
                                                             {}, basc_thr, labels)
        elected_miss = pd.DataFrame(imputate_missforest(elected_binarizations.to_dict(orient='records'))).astype(int)
        
        if data != 'ecoli':
                elected_probabilistic = statistics(gene_normalized, elected_binarizations, "Elected", thr_methods)
                
                elected_probabilistic_probs_miss = pd.DataFrame(imputate_missforest(elected_probabilistic.to_dict(orient='records'))).astype(int)
                
        
        #print(datasets[data][1])
        rules_uploaded = pd.read_csv(datasets[data][1], header=0)
        
        for index, row in rules_uploaded.iterrows():
            if pd.isna(row['Rule']):
                rules_uploaded.loc[index, 'Rule'] = ''
            elif not row['Rule'].strip():
                rules_uploaded.loc[index, 'Rule'] = ''
        
        rules_uploaded.to_dict(orient='records')
        #print(rules_uploaded)
        
        #print(rules_uploaded)
        
        compare_dfs = [basc_miss, kmeans_miss, onestep_miss, elected_miss, basc_probabilistic_probs_miss, kmeansprobabilistic_probs_miss,
                       onestep_probabilistic_probs_miss, elected_probabilistic_probs_miss]
        
        compare_labels = ["basc_miss", "kmeans_miss", "onestep_miss", "elected_miss", "basc_probs", "kmeans_probs", "onestep_probs", "elected_probs"]
        
        compare_dict = {'Same binarization':[], 'Diff binarization':[]}
        
        for i in range(len(compare_dfs)):
            
            for j in range(i+1, len(compare_labels)):
                
                if compare_dfs[i].equals(compare_dfs[j]):   
                    
                    #print(compare_labels[i], compare_labels[j])
                    
                    compare_dict['Same binarization'].append(f"{compare_labels[i]}, {compare_labels[j]}")
                    compare_dict['Diff binarization'].append("")
                
                else:
                    
                    compare_dict['Same binarization'].append("")
                    compare_dict['Diff binarization'].append(f"{compare_labels[i]}, {compare_labels[j]}")
        
        
        df_compare = pd.DataFrame(compare_dict)
        
        df_compare.to_csv(f'../metrics_results/{data}_binarization_comparison.csv', index=True) 
        
        for j in range(2):
            
            if j == 0:
                #print(basc_miss)
                res = download_metrics(gene_normalized, selected_genes, thr_methods, elected_miss, kmeans_miss, [], basc_miss, onestep_miss, rules_uploaded)
                
                df_res = pd.DataFrame(res)
                
                #print(df_res)
                
                df_res.to_csv(f'../metrics_results/{data}_miss.csv', index=True) 
                
                
            elif j == 1 and data != 'ecoli':
                
                res = download_metrics(gene_normalized, selected_genes, thr_methods, elected_probabilistic_probs_miss, 
                                       kmeansprobabilistic_probs_miss, [], basc_probabilistic_probs_miss, onestep_probabilistic_probs_miss, rules_uploaded)
                
                #print(res)
                
                df_res = pd.DataFrame(res)
                
                df_res.to_csv(f'../metrics_results/{data}_probs.csv', index=True) 
                
    
    