################################
##
## File containing functions about binarizing each gene based on thr methods 
##
###############################

import networkx as nx
from binarization.interpolation import interpolation
import pandas as pd
from binarization.voting_algos import  election_strings
from threshold_methods.methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep
import math

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
    
    # iterate by each gene and find the thresholds based on the number of interpolations
    for gene in genes:

        range_displacement_index = math.ceil((max(gene)-min(gene))*10) - 1

        if(method == "K-Means"):
            
            # append threshold of the original gene
            t.append(thr_k[str(selected[index])])

            # save displacement of that gene 
            d.append(displacement['k-means'].iloc[range_displacement_index])

        elif(method == "Shmulevich"):
        
            # append threshold of the original gene
            t.append(thr_s[str(selected[index])])
            
            # save displacement of that gene 
            d.append(displacement['shmulevich'].iloc[range_displacement_index])
            
        elif(method == "Onestep"):
            
            # append threshold of the original gene
            t.append(thr_o[str(selected[index])])

            # save displacement of that gene 
            d.append(displacement['onestep'].iloc[range_displacement_index])


        else:
           
            # append threshold of the original gene
            t.append(thr_b[str(selected[index])])

            # save displacement of that gene 
            d.append(displacement['BASC_A'].iloc[range_displacement_index])

        # get voting based on the gene expression, thresholds, and displacement
        votes =  election_strings(gene, t, d)
            
        # get the final vote 
        final = votes[1]

        # change -1 of the final vote to ?
        for i in range(len(final)):
            if(final[i] != '?'):
                final[i] = int(final[i])
            
        # save the final vote to a dataframe. 
        df[labels[selected[index]]] = final
        t = []
        d = []
        index += 1
        binarize = []

    
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
    
    # for each gene find the vote by the given methods 
    for gene in genes:
        
        t = []
        d = []

        vote_binary = []

        selected_range = max(gene) - min(gene)
    
        range_displacement_index = math.ceil((max(gene)-min(gene))*10) - 1

        #_, geneSpline = three_interpolation(gene, 'K-Means', 4)

        # go through each method and find thresholds, and displacement
        for method in methods:
            if(method == 'BASC A'):

                # save threshold of original gene
                t.append(thr_b[str(selected[index])])

                # save displacement of that gene 
                d.append(displacement['BASC_A'].iloc[range_displacement_index])

            elif(method == 'K-Means'):

                # save threshold of original gene
                t.append(thr_k[str(selected[index])])

                # save displacement of that gene 
                d.append(displacement['k-means'].iloc[range_displacement_index])
        

            elif(method == 'Onestep'):

                # save threshold of original gene
                t.append(thr_o[str(selected[index])])
                
                # save displacement of that gene 
                d.append(displacement['onestep'].iloc[range_displacement_index])
                

            else:

                # save threshold of original gene
                t.append(thr_s[str(selected[index])])
                
                # save displacement of that gene
                d.append(displacement['shmulevich'].iloc[range_displacement_index])


        # based on the gene and the methods find the voting table 
        # pass the list of thresholds, and displacements
        # each element of the list is of a different algorithm 
        votes = election_strings(gene, t, d)
        
        # get the final vote of the gene 
        final = votes[1]
        
        # change -1 to ?
        for i in range(len(final)):
            if(final[i] != '?'):
                final[i] = int(final[i])
                
        # save gene to a dataframe as a column
        df[labels[selected[index]]] = final
        index += 1
    
    #print(df)

    # return dataframe
    return df
