################################
## Code to generate the network as a DataFrame.
## Function - create_boolean_network, creates dataframe of the network individualy by the methods selected
## Function - create_boolean_network_votes, creates dataframe of the network by the final collective vote 

###############################

import networkx as nx
from interpolation import three_interpolation, interpolationConverge
import pandas as pd
from voting_algos import binarizationVoting
from methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep
import math

# function to create dataframe with the binarization of each gene done by algorithm 
# arguments: selected - rows to create network, method - method to create network, data - dataset, tolerance - number of iterations
def create_boolean_network(selected, method, data, displacement, thr_k, thr_o, thr_s, thr_b):
    
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
        votes = binarizationVoting(gene, t, d)
            
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
        df['Gene ' + str(selected[index]+1)] = final
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
def create_boolean_network_votes(selected, data, methods, displacement, thr_k, thr_o, thr_s, thr_b):
    
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
        votes = binarizationVoting(gene, t, d)
        
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
        df['Gene ' + str(selected[index]+1)] = final
        index += 1
    
    #print(df)

    # return dataframe
    return df

'''
def network_rules(selected, method, data, rules, thr_b, thr_k, thr_s, thr_o, displacement):

    rules = pd.DataFrame(rules)

    rules.columns = rules.iloc[0]
    rules = rules [1:]

    
    gene_data = pd.DataFrame(data)
    
    genes = gene_data.iloc[selected].values.astype(float)

    #print(genes)
    
    genes_col = []
    
    for index, row in rules.iterrows():
            genes_col.append(row['Gene'])

    df = pd.DataFrame(columns=genes_col)

    binarize = []

    index = 0

    t = []
    d = []
    
    for gene in genes:

        range_displacement_index = math.ceil((max(gene)-min(gene))*10) - 1

        if(method == "K-Means"):
            #thr = K_Means(gene)
         
            t.append(thr_k[str(selected[index])])
            
            d.append(displacement['k-means'].iloc[range_displacement_index])

        elif(method == "Shmulevich"):
            #thr = shmulevich(gene)
            t.append(thr_s[str(selected[index])])

            d.append(displacement['shmulevich'].iloc[range_displacement_index])

        elif(method == "Onestep"):
            #thr = onestep(gene)
            t.append(thr_o[str(selected[index])])

            d.append(displacement['onestep'].iloc[range_displacement_index])

        else:
            #thr = BASC_A(gene)

            t.append(thr_b[str(selected[index])])

            d.append(displacement['BASC_A'].iloc[range_displacement_index])

        binarize = []

        #for t in gene:
        #    if t < thr:
        #        binarize.append(0)
        #    else:
        #        binarize.append(1)

        #df[genes_col[index]] = binarize

        #index += 1

        # get voting based on the gene expression, thresholds, and displacement
        votes = binarizationVoting(gene, t, d)
            
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
        df[genes_col[index]] = final
        t = []
        d = []
        index += 1
        binarize = []

    

    final_states_df = df.copy()
    
    for indexes, rows in rules.iterrows():

            gene = rows['Gene']
            rule = rows['Rule']

            rule = rule.replace('!', ' not ')

            genes_names = []

            for g in genes_col:
                if g in rule:
                    genes_names.append(g)

            for index, row in df.iterrows():

                values = {}

                for g in genes_names:
                    values[g] = row[g]

                if '?' in values.values():
                    result = '?'
                else:


                    result = int(eval(rule, values))

                final_states_df.at[index, f"{gene}'"] = str(result)
                
    return final_states_df


def network_rules_vote(selected, methods, data, rules, thr_b, thr_k, thr_s, thr_o, displacement):

    rules = pd.DataFrame(rules)

    rules.columns = rules.iloc[0]
    rules = rules [1:]

    
    gene_data = pd.DataFrame(data)
    
    genes = gene_data.iloc[selected].values.astype(float)

    #print(genes)
    
    genes_col = []
    
    for index, row in rules.iterrows():
            genes_col.append(row['Gene'])

    df = pd.DataFrame(columns=genes_col)

    binarize = []

    index = 0
    
    for gene in genes:

        t = []
        d = []

        vote_binary = []

        range_displacement_index = math.ceil((max(gene)-min(gene))*10) - 1

        for method in methods:

            if(method == "K-Means"):
    
                t.append(thr_k[str(selected[index])])
                #thr = K_Means(gene)

                 # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'K-Means', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['k-means'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))




            elif(method == "Shmulevich"):

                t.append(thr_s[str(selected[index])])
                #thr = shmulevich(gene)

                 # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'Shmulevich', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['shmulevich'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))



            elif(method == "Onestep"):

                t.append(thr_o[str(selected[index])])
                #thr = onestep(gene)

                 # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'Onestep', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['onestep'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))



            else:

                # save threshold of original gene
                t.append(thr_b[str(selected[index])])

                # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'BASC A', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['BASC_A'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))


                #thr = BASC_A(gene)

        votes = binarizationVoting(gene, t, d)

        final = votes[1]

        # change -1 to ?
        for i in range(len(final)):
            if(final[i] != '?'):
                final[i] = int(final[i])

        #for t in gene:
        #        if t < thr:
        #            binarize.append(0)
        #        else:
        #            binarize.append(1)

        df[genes_col[index]] = final

        index += 1

    
    final_states_df = df.copy()

    #print(final_states_df)
    
    for indexes, rows in rules.iterrows():

            gene = rows['Gene']
            rule = rows['Rule']

            rule = rule.replace('!', ' not ')

            genes_names = []

            for g in genes_col:
                if g in rule:
                    genes_names.append(g)

            for index, row in df.iterrows():

                values = {}

                for g in genes_names:
                    values[g] = row[g]

                if '?' in values.values():
                    result = '?'
                else:

                    
                    #print(rule, values)
                    result = int(eval(rule, values))

                final_states_df.at[index, f"{gene}'"] = str(result)
                
    return final_states_df



def network_rules2(selected, method, data, rules, thr_b, thr_k, thr_s, thr_o, displacement):

    rules = pd.DataFrame(rules)

    rules.columns = rules.iloc[0]
    rules = rules [1:]

    
    gene_data = pd.DataFrame(data)
    
    genes = gene_data.iloc[selected].values.astype(float)

    #print(genes)
    
    genes_col = []
    
    for index, row in rules.iterrows():
            genes_col.append(row['Gene'])
            

    df = pd.DataFrame(columns=genes_col)

    binarize = []

    index = 0

    t = []
    d = []
    
    gene_size = len(genes[0])
    
    for gene in genes:

        range_displacement_index = math.ceil((max(gene)-min(gene))*10) - 1

        if(method == "K-Means"):
            #thr = K_Means(gene)
         
            t.append(thr_k[str(selected[index])])
            
            d.append(displacement['k-means'].iloc[range_displacement_index])

        elif(method == "Shmulevich"):
            #thr = shmulevich(gene)
            t.append(thr_s[str(selected[index])])

            d.append(displacement['shmulevich'].iloc[range_displacement_index])

        elif(method == "Onestep"):
            #thr = onestep(gene)
            t.append(thr_o[str(selected[index])])

            d.append(displacement['onestep'].iloc[range_displacement_index])

        else:
            #thr = BASC_A(gene)

            t.append(thr_b[str(selected[index])])

            d.append(displacement['BASC_A'].iloc[range_displacement_index])

        binarize = []

        #for t in gene:
        #    if t < thr:
        #        binarize.append(0)
        #    else:
        #        binarize.append(1)

        #df[genes_col[index]] = binarize

        #index += 1

        # get voting based on the gene expression, thresholds, and displacement
        votes = binarizationVoting(gene, t, d)
            
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
        df[genes_col[index]] = final
        t = []
        d = []
        index += 1
        binarize = []


    df2 = pd.DataFrame(columns=df.columns)
    #df2 = df2.append(df.iloc[1], ignore_index=True)
    df2 = pd.concat([df2, df.iloc[[0]]], axis=0, ignore_index=True)
    
    #print(df2)
    
    
    #print(genes_rules)
    
    for t in range(gene_size-1):
        
        row_bin = df2.iloc[t]
        
        #strr = []
        for indexes, rows in rules.iterrows():
            gene = rows['Gene']
            rule = rows['Rule']

            rule = rule.replace('!', ' not ')
            
            dic = row_bin.to_dict()
            
            
            actual_values = {}
            
            for key in dic:
                
                if key in rule:
                    actual_values[key] = dic[key]
            
            #print(actual_values)
            if '?' in actual_values.values():
                
                df2.at[t+1, gene] = '?'
            
            #if '?' == curr_val_gene:
            #        result = '?'
            else:
                result = int(eval(rule, row_bin.to_dict()))
            
                df2.at[t+1, gene] = int(result)
            #strr.append(result)
            
        #print(row_bin.to_dict(), strr)
           
        
            
    return df2


def network_rules_vote2(selected, methods, data, rules, thr_b, thr_k, thr_s, thr_o, displacement):

    rules = pd.DataFrame(rules)

    rules.columns = rules.iloc[0]
    rules = rules [1:]

    
    gene_data = pd.DataFrame(data)
    
    genes = gene_data.iloc[selected].values.astype(float)

    #print(genes)
    
    genes_col = []
    
    for index, row in rules.iterrows():
            genes_col.append(row['Gene'])

    df = pd.DataFrame(columns=genes_col)

    binarize = []

    gene_size = len(genes[0])

    index = 0
    
    for gene in genes:

        t = []
        d = []

        vote_binary = []

        range_displacement_index = math.ceil((max(gene)-min(gene))*10) - 1

        for method in methods:

            if(method == "K-Means"):
    
                t.append(thr_k[str(selected[index])])
                #thr = K_Means(gene)

                 # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'K-Means', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['k-means'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))




            elif(method == "Shmulevich"):

                t.append(thr_s[str(selected[index])])
                #thr = shmulevich(gene)

                 # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'Shmulevich', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['shmulevich'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))



            elif(method == "Onestep"):

                t.append(thr_o[str(selected[index])])
                #thr = onestep(gene)

                 # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'Onestep', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['onestep'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))



            else:

                # save threshold of original gene
                t.append(thr_b[str(selected[index])])

                # find threshold list of the number of interpolations
                #t_b, _ = three_interpolation(gene, 'BASC A', 4)

                #d.append(max(t_b) - min(t_b))

                d.append(displacement['BASC_A'].iloc[range_displacement_index])

                # do vote for this method
                #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))


                #thr = BASC_A(gene)

        votes = binarizationVoting(gene, t, d)

        final = votes[1]

        # change -1 to ?
        for i in range(len(final)):
            if(final[i] != '?'):
                final[i] = int(final[i])

        #for t in gene:
        #        if t < thr:
        #            binarize.append(0)
        #        else:
        #            binarize.append(1)

        df[genes_col[index]] = final

        index += 1

    
    df2 = pd.DataFrame(columns=df.columns)
    #df2 = df2.append(df.iloc[1], ignore_index=True)
    df2 = pd.concat([df2, df.iloc[[0]]], axis=0, ignore_index=True)
    
    #print(df2)
    
    
    #print(genes_rules)
    
    for t in range(gene_size-1):
        
        row_bin = df2.iloc[t]
        
        #strr = []
        for indexes, rows in rules.iterrows():
            gene = rows['Gene']
            rule = rows['Rule']

            rule = rule.replace('!', ' not ')
            
            dic = row_bin.to_dict()
            
            
            actual_values = {}
            
            for key in dic:
                
                if key in rule:
                    actual_values[key] = dic[key]
            
            #print(actual_values)
            if '?' in actual_values.values():
                
                df2.at[t+1, gene] = '?'
            
            #if '?' == curr_val_gene:
            #        result = '?'
            else:
                result = int(eval(rule, row_bin.to_dict()))
            
                df2.at[t+1, gene] = int(result)
            #strr.append(result)
            
        #print(row_bin.to_dict(), strr)
           
        
            
    return df2
           '''
