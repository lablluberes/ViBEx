##############################################
#
# This file contains functions for metrics performance
#
##############################################
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def getAdjMatrix(rule_net):
    """
        getAdjMatrix - return undirected adj matrix based on Boolean functions 

        rule_net: boolean functions dataframe
    """
    
    # get gene names
    gene_names = rule_net['Gene'].values
    
    gene_dict = {}
    
    # name genes as numbers 
    for i in range(len(gene_names)):
        
        gene_dict[gene_names[i]] = i
        

    # adj matrix 
    adj_matrix = np.zeros((len(rule_net), len(rule_net)))   

    # iterate rules and add edges 
    for index, row in rule_net.iterrows():
        rule = row['Rule']
        gene = row['Gene']
        
        # verify if genes are in rule
        for g in gene_names:
            
            # adds undirected edge example: (1, 2)
            if g in rule:

                to = gene_dict[gene]
                from_ = gene_dict[g]
                
                adj_matrix[to, from_] = 1
                adj_matrix[from_, to] = 1   
        
    return adj_matrix

def Metrics(ground_truth, inferred):
    """
        Metrics - does metrics evaluation of inferred rules and uploaded rules

        ground_truth: uploaded Boolean functions
        inferred: inferred Boolean functions
    """
    
    # get size of network
    sizeNet = len(ground_truth)
    
    # get adj matrix undirected 
    adj_ground = getAdjMatrix(ground_truth)
    adj_inferred = getAdjMatrix(inferred) 

    # for metrics  
    y_true = adj_ground[np.triu_indices(sizeNet)]           
    y_pred = adj_inferred[np.triu_indices(sizeNet)]  
    
    #print(adj_ground, adj_inferred)
    
    #print(y_true, y_pred)
    
    # gets metrics 
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    metrics_dict = {'Accuracy': [accuracy], 'Precision':[precision], 'Recall':[recall], 'F1-Score':[f1]}
    
    return metrics_dict

def dynamic_accuracy(df, df1):
    """
        dynamic_accuracy - calculate dynamic accuracy 

        df - extracted path from inferred BN
        df1 - path from binarization  
    """
    
    # save names of genes 
    columns_names = list(df.columns)

    #print(columns_names)

    # if the length between paths are not the same return none
    if len(df) != len(df1):
        return None

    # save the hamming/t of gene states 
    C = []
    
    # iterate genes
    for c in columns_names:

        # calculate hamming after the first state 
        x = list(df[c].values[1:])
        x1 = list(df1[c].values[1:])
    
        #print(x, x1)

        # hamming count
        s = 0
        
        # total states of gene
        t = len(x)

        # save hamming distance of each state
        for xi, xip in zip(x, x1):
            s += abs(int(xi) - int(xip))

        # save the hamming/length states 
        C.append(s/t)

    #print(C)

    # calculate dynamic accuracy 
    dyn_acc = 1 - (sum(C)/len(columns_names))

    return dyn_acc


def getAdjMatrix_directed(rule_net):
    """
        getAdjMatrix_directed - return directed adj matrix based on Boolean functions 

        rule_net: boolean functions dataframe
    """
    
    # get gene names
    gene_names = rule_net['Gene'].values
    
    gene_dict = {}
    
    # name genes as numbers 
    for i in range(len(gene_names)):
        
        gene_dict[gene_names[i]] = i
        

    # adj matrix 
    adj_matrix = np.zeros((len(rule_net), len(rule_net)))   

    # iterate rules and add edges 
    for index, row in rule_net.iterrows():
        rule = row['Rule']
        gene = row['Gene']
        
        # verify if genes are in rule
        for g in gene_names:
            
            # adds directed edge example: (1, 2)
            if g in rule:

                to = gene_dict[gene]
                from_ = gene_dict[g]
                
                adj_matrix[to, from_] = 1
                #adj_matrix[from_, to] = 1   
    
    #print(rule_net)
    #print(adj_matrix)

    return adj_matrix

def Metrics_directed(ground_truth, inferred):
    """
        Metrics_directed - does metrics evaluation of inferred rules and uploaded rules

        ground_truth: uploaded Boolean functions
        inferred: inferred Boolean functions
    """
    
    # get size of network
    sizeNet = len(ground_truth)
    
    # get adj matrix directed 
    adj_ground = getAdjMatrix_directed(ground_truth)
    adj_inferred = getAdjMatrix_directed(inferred) 

    #print(adj_ground)
    #print(adj_inferred)

    # for metrics  
    y_true = adj_ground.flatten()         
    y_pred = adj_inferred.flatten()
    
    #print(adj_ground, adj_inferred)
    
    #print(y_true, y_pred)
    
    # gets metrics 
    accuracy = round(accuracy_score(y_true, y_pred), 2)
    precision = round(precision_score(y_true, y_pred), 2)
    recall = round(recall_score(y_true, y_pred), 2)
    f1 = round(f1_score(y_true, y_pred), 2)
    
    metrics_dict = {'Accuracy': [accuracy], 'Precision':[precision], 'Recall':[recall], 'F1-Score':[f1]}
    
    return metrics_dict