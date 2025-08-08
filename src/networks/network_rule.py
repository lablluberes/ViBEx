#########################
#
# File contains functions to create a BN of all possible states based on rules
#
#########################
import pandas as pd
import numpy as np
import networkx as nx
import gravis as gv
import matplotlib.pyplot as plt
import igraph as ig
from IPython.core.display import HTML
from pyvis.network import Network
from networks.attractors import attractors

# function that reads the rules of the csv and creates a boolean network of all posible states
# the parameters is the csv file as a dataframe
def createNetwork(rules_df):
    """
        createNetwork - generates BN of all possible states based on rules

        rules_df: Boolean functions
    
    """
    
    # empty dict for the genes, rules, and j
    dict_net = {}
    genes = {}
    rules_dict = {}
    j = {}
    
    
    gene_id = 1

    labels = list(rules_df['Gene'].values)
    
    # read each row of the dataframe 
    for index, row in rules_df.iterrows():
 
        # save the gene to the gene_dict and assign a gene_id (1, 2, ..., n). example: gene = {'x1':1, 'x2': 2}
        genes[row['Gene']] = gene_id
        
        # save rule of that gene to rules_dict. example: rules_dict = {'x1': 'x1 or x2'}
        if row['Rule'] == '':

            rules_dict[row['Gene']] = row['Gene']
        
        else:
            rules_dict[row['Gene']] = row['Rule']
        
        # get gene name
        g = row['Gene']
        
        # save to j (j are the genes that are part of each functions)
        # this is basically initializing j
        j[g] = []
        
        # increase gene id
        gene_id += 1
    
    #print(genes, rules_dict, j)
    
    # go through each rule in rule_dict
    for key in rules_dict:
        
        # go through each gene in gene dict
        for g in genes:
            
            # if that gene is at the the rule then append to j
            if g in rules_dict[key]:
                
                # save gene to j
                j[key].append(genes[g])
                
                #print(g, rules_dict[key])
        
        #print(rules_dict[key])
        
    #print(j)
    
    # total of genes
    size = len(genes)
    
    # number of states 2 ** number of genes
    n = 2**size
    
    # get list of all the possible states 2 ** size
    states = np.arange(n)
    
    # initialize a directed network
    net = Network(width="450px", height="450px", directed=True)
    
    #states_name = []
    
    #net_states = []
    
    #print(initState, states)
    
    # go through each possible state in order 
    for s in states:
        
        # turn the numbers of the list (0, 1, ..., 31) to binary strings
        # use zfill to fill with zeros so that all states have a size of 5 
        curr_state = bin(s)[2:].zfill(size)
        
        #print(curr_state)
        #print("Starting here ", curr_state)
        
        #states_name.append(curr_state)
        
        # empty string where to save the next state
        end_state = ""
        
        for key in j:
        
           if rules_dict[key] == "True":         
                list_curr_state = list(curr_state)
                #print(list_curr_state) 
                list_curr_state[genes[key]-1] = '1'
                        
                curr_state = ''.join(list_curr_state)
                
           elif rules_dict[key] == "False":
                list_curr_state = list(curr_state)
                #print(list_curr_state) 
                list_curr_state[genes[key]-1] = '0'
                        
                curr_state = ''.join(list_curr_state)
               
                #print(curr_state)
            
        # loop through each key in j
        for key in j:
            

                # array to save the genes in a rule
                g_in_rule = []
                
                # array to save tje values of the gene
                gene_val_rule = []
                
                # iterate the genes 
                for g in genes:
                    
                    # if the gene is in the rule append it to the list
                    if g in rules_dict[key]:
                        # append gene to list
                        g_in_rule.append(g)
            
                
                # iterate the arrays of j
                for ind in j[key]:

                    # add the values of those genes based on the current state
                    gene_val_rule.append(int(curr_state[ind-1]))
                
                # dictionary of the values of the genes that are in the rule. example dict_eval = {'x1':1, 'x3':0}
                dict_eval = {}
                
                # iterate the list of genes in the rule
                for k in range(len(g_in_rule)):
                    
                    # add to the dict the gene name as the key (this was saved in g_in_rule)
                    # and the value as the value in the current state (this was saved in gene_val_rule list)
                    dict_eval[g_in_rule[k]] = gene_val_rule[k]
         
                # use eval and apply the dict values to the rule
                # append return value to end state
                end_state += str(int(eval(rules_dict[key], dict_eval)))
                
                
        #print(f"Current state {curr_state}, next state {end_state}")
        
        #net_states.append((int(curr_state, 2), int(end_state, 2)))
        
        # add curr state node to graph
        if curr_state in dict_net:
            continue
        
        dict_net[curr_state] = end_state

        title_label1 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(labels, list(curr_state)))
        title_label2 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(labels, list(end_state)))

        net.add_node(curr_state, label=curr_state, shape='circle', title=title_label1)
        # add end state node to graph
        net.add_node(end_state, label=end_state, shape='circle', title=title_label2)
        # add edge from curr to end state to graph
        net.add_edge(curr_state, end_state)
        
        #print(curr_state, end_state)

    #print(dict_net)
    #print(net.edges)

    Atts_syn, Att_num = attractors(dict_net)

    #print(Atts_syn)

    for nodes in net.nodes:

        if nodes['id'] in Atts_syn:
            nodes['color'] = 'lightgray'

    #print(net.nodes)
        
    # save network as html (open the file to see it)
    return net, dict_net
        
        
        