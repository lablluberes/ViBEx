################################
## Code to generate the network as a DataFrame.
## Function - create_boolean_network, creates dataframe of the network individualy by the methods selected
## Function - create_boolean_network_votes, creates dataframe of the network by the final collective vote 

###############################

import networkx as nx
from interpolation import interpolation
import pandas as pd
from voting_algos import  election_strings
from methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep
import math

# function to create dataframe with the binarization of each gene done by algorithm 
# arguments: selected - rows to create network, method - method to create network, data - dataset, tolerance - number of iterations
def create_boolean_network(selected, method, data, displacement, thr_k, thr_o, thr_s, thr_b, labels):
    
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

        #_, geneSpline = three_interpolation(gene, 'K-Means', 4)

        if(method == "K-Means"):
            #thr = K_Means(gene)

            # append threshold of the original gene
            t.append(thr_k[str(selected[index])])
            #t.append(K_Means(geneSpline))

            # find threshold list of the number of interpolations
            #t_k, _ = three_interpolation(gene, 'K-Means', 4)

            #t.append(t_k[-1])

            # save displacement of that gene 
            d.append(displacement['k-means'].iloc[range_displacement_index])

            #d.append(max(t_k) - min(t_k))

            # get vote and save 
            #vote_binary.append(binVoting(gene, [K_Means(gene)], [max(t_k) - min(t_k)]))

        elif(method == "Shmulevich"):
            #thr = shmulevich(gene)

            # append threshold of the original gene
            t.append(thr_s[str(selected[index])])
            #t.append(shmulevich(geneSpline))

             # find threshold list of the number of interpolations
            #t_s, _ = three_interpolation(gene, 'Shmulevich', 4)

            #t.append(t_s[-1])

            # save displacement of that gene 
            d.append(displacement['shmulevich'].iloc[range_displacement_index])

            #d.append(max(t_s) - min(t_s))

            # get vote and save 
            #vote_binary.append(binVoting(gene, [shmulevich(gene)], [max(t_s) - min(t_s)]))
            
        elif(method == "Onestep"):
            #thr = onestep(gene)

            # append threshold of the original gene
            t.append(thr_o[str(selected[index])])
            #t.append(onestep(geneSpline))

            # find threshold list of the number of interpolations
            #t_o, _ = three_interpolation(gene, 'Onestep', 4)

            #t.append(t_o[-1])

            # save displacement of that gene 
            d.append(displacement['onestep'].iloc[range_displacement_index])

            #d.append(max(t_o) - min(t_o))

            # get vote and save 
            #vote_binary.append(binVoting(gene, [onestep(gene)], [max(t_o) - min(t_o)]))

        else:
            #thr = BASC_A(gene)

            # append threshold of the original gene
            t.append(thr_b[str(selected[index])])
            #t.append(BASC_A(geneSpline))

            # find threshold list of the number of interpolations
            #t_b, _ = three_interpolation(gene, 'BASC A', 4)

            #t.append(t_b[-1])

            # save displacement of that gene 
            d.append(displacement['BASC_A'].iloc[range_displacement_index])

            #d.append(max(t_b) - min(t_b))

            # get vote and save 
            #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))
            
        #for exp in gene:
        #    if(exp <= thr):
        #        binarize.append(0)
        #    else:
        #        binarize.append(1)

        # get voting based on the gene expression, thresholds, and displacement
        votes =  election_strings(gene, t, d)
            
        # saved previous votes of genes
        #votes = [vote_binary]
        
        # do a final vote 
        #votes.append(binVoting(gene, t, d))

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

# function to create dataframe with the binarization of each gene
# done by the final vote of the collective algorithms 
# arguments: selected - rows to create network, methods - method to create network, data - dataset, tolerance - number of iterations
def create_boolean_network_votes(selected, data, methods, displacement, thr_k, thr_o, thr_s, thr_b, labels):
    
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
                #t.append(BASC_A(geneSpline))

                # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'BASC A', 4)

                #t.append(t_b[-1])

                # save displacement of that gene 
                d.append(displacement['BASC_A'].iloc[range_displacement_index])

                #d.append(max(t_b) - min(t_b))

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))

            elif(method == 'K-Means'):

                # save threshold of original gene
                t.append(thr_k[str(selected[index])])
                #t.append(K_Means(geneSpline))

                # find threshold list of the number of interpolations
                #t_k, _ = three_interpolation(gene, 'K-Means', 4)

                #t.append(t_k[-1])

                # save displacement of that gene 
                d.append(displacement['k-means'].iloc[range_displacement_index])
                
                #d.append(max(t_k) - min(t_k))

                # do vote for this method
                #vote_binary.append(binVoting(gene, [K_Means(gene)], [max(t_k) - min(t_k)]))


            elif(method == 'Onestep'):

                # save threshold of original gene
                t.append(thr_o[str(selected[index])])
                #t.append(onestep(geneSpline))

                # find threshold list of the number of interpolations
                #t_o, _ = three_interpolation(gene, 'Onestep', 4)

                #t.append(t_o[-1])

                # save displacement of that gene 
                d.append(displacement['onestep'].iloc[range_displacement_index])
                
                #d.append(max(t_o) - min(t_o))

                # do vote for this method
                #vote_binary.append(binVoting(gene, [onestep(gene)], [max(t_o) - min(t_o)]))

            else:

                # save threshold of original gene
                t.append(thr_s[str(selected[index])])
                #t.append(shmulevich(geneSpline))

                # find threshold list of the number of interpolations
                #t_s, _ = three_interpolation(gene, 'Shmulevich', 4)

                #t.append(t_s[-1])
                
                # save displacement of that gene
                d.append(displacement['shmulevich'].iloc[range_displacement_index])

                #d.append(max(t_s) - min(t_s))

                # do vote for this method
                #vote_binary.append(binVoting(gene, [shmulevich(gene)], [max(t_s) - min(t_s)]))

        # based on the gene and the methods find the voting table 
        # pass the list of thresholds, and displacements
        # each element of the list is of a different algorithm 
        votes = election_strings(gene, t, d)
        
        # saved the votes
        #votes = [vote_binary]

        # do vote with all algos to get final
        #votes.append(binVoting(gene, t, d))
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
