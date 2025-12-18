################################
##
## File containing functions about binarizing each gene based on thr methods 
##
###############################

import networkx as nx
from binarization.interpolation import interpolation
import pandas as pd
from binarization.voting_algos import  election_strings
from threshold_methods.methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer
import math
import numpy as np
from displacements.displacementMatrixes import getDisplacement

# function to create dataframe with the binarization of each gene done by algorithm 
# arguments: selected - rows to create network, method - method to create network, data - dataset, tolerance - number of iterations
def create_boolean_network(selected, method, data, displacement, thr_k, thr_o, thr_s, thr_b, labels):
    """
        create_boolean_network - function to create dataframe with the binarization of each gene done by algorithm 

        selected: selected genes
        methods: selected thr methods
        data: gene expr dataset
        displacement: displacement table
        thr_k: thr of kmeans
        thr_o: thr of onestep
        thr_s: thr of shmulevich
        thr_b: thr of basca
        labels: gene labels
    """
    
    # get the dataset
    gene_data = pd.DataFrame(data)
    
    # get the selected genes
    genes = gene_data.iloc[selected].values.astype(float)
    
    df = pd.DataFrame()
    
    binarize = []
    
    index = 0

    # save thresholds of genes and displacement 
    t = []
    d = []

    vote_binary = []
    
    method_labels = {'BASC A': ['BASC_A', thr_b], 'Onestep': ['onestep', thr_o], 'K-Means':['k-means', thr_k], 'Shmulevich':['shmulevich', thr_s]}
    
    # iterate by each gene and find the thresholds based on the number of interpolations
    for row, gene in enumerate(genes):
        
        # extract displacement based on gene range
        disps = getDisplacement([method],gene)

        #print(disps)
        
        t = []
        d = []
        #votes = [[]]
        
        # extract thr, and disp of each method of the gene
            
        thr = method_labels[method][1][str(selected[row])]
        dis = disps[method_labels[method][0]].iloc[0]
        t.append(thr)
            
        d.append(dis)
                
        el = election_strings(gene, [thr], [dis])
                
        el = ['?' if np.isnan(e) else int(e) for e in el]
        #votes[0].append(el)
                
        df[labels[selected[row]]] = el
        
        #print(gene, t, d)
        # generate voting (elected string) of the gene based on thr, and displacements
        #print(gene, t, d, selected_method)

    
    #print(df)

    # return created dataframe of the final vote of each gene
    
    return df

# function to create dataframe with the binarization of elected 
# done by the final vote of the collective algorithms 
# arguments: selected - rows to create network, methods - method to create network, data - dataset, tolerance - number of iterations
def create_boolean_network_votes(selected, data, methods, displacement, thr_k, thr_o, thr_s, thr_b, labels):
    """
        create_boolean_network_votes - function to create dataframe with the binarization of final vote 

        selected: selected genes
        methods: selected thr methods
        data: gene expr dataset
        displacement: displacement table
        thr_k: thr of kmeans
        thr_o: thr of onestep
        thr_s: thr of shmulevich
        thr_b: thr of basca
        labels: gene labels
    """
    
    # get dataset
    gene_data = pd.DataFrame(data)
    
    # extract the genes from data set
    genes = gene_data.iloc[selected].values.astype(float)
    
    df = pd.DataFrame()
    
    index = 0
    
    method_labels = {'BASC A': ['BASC_A', thr_b], 'Onestep': ['onestep', thr_o], 'K-Means':['k-means', thr_k], 'Shmulevich':['shmulevich', thr_s]}
    
    # for each gene find the vote by the given methods 
    for row, gene in enumerate(genes):
        
        # extract displacement based on gene range

        #print(disps)
        
        t = []
        d = []
        #votes = [[]]
        
        # go through each method and extract the thr, and disp
       
        for method in methods:
            
            #print(gene)
            #print("MMEEEETTOOOOODOOOOOO", method)
            disps = getDisplacement([method],gene)
           

            # extract thr, and disp of each method of the gene
            
            thr = method_labels[method][1][str(selected[row])]
            
            #print("aqui")
            dis = disps[method_labels[method][0]].iloc[0]
            
       
            t.append(thr)
      
            d.append(dis)
                   
        #print(gene, t, d)
        # generate voting (elected string) of the gene based on thr, and displacements
        #print(gene, t, d, selected_method)
        
        el = election_strings(gene, t, d)
                
        el = ['?' if np.isnan(e) else int(e) for e in el]
        
        df[labels[selected[row]]] = el
    
    #print(df)

    # return dataframe
    return df
