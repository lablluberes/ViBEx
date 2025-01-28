import pandas as pd
import numpy as np
import networkx as nx
import gravis as gv
import matplotlib.pyplot as plt
import igraph as ig
from IPython.core.display import HTML
from pyvis.network import Network

# function that reads the rules of the csv and creates a boolean network of all posible states
# the parameters is the csv file as a dataframe
def createNetwork(rules_df):
    
    # empty dict for the genes, rules, and j
    dict_net = {}
    genes = {}
    rules_dict = {}
    j = {}
    
    
    gene_id = 1
    
    # read each row of the dataframe 
    for index, row in rules_df.iterrows():
 
        # save the gene to the gene_dict and assign a gene_id (1, 2, ..., n). example: gene = {'x1':1, 'x2': 2}
        genes[row['Gene']] = gene_id
        
        # save rule of that gene to rules_dict. example: rules_dict = {'x1': 'x1 or x2'}
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
    net = Network(width="500px", height="500px", directed=True)
    
    #states_name = []
    
    #net_states = []
    
    #print(initState, states)
    
    # go through each possible state in order 
    for s in states:
        
        # turn the numbers of the list (0, 1, ..., 31) to binary strings
        # use zfill to fill with zeros so that all states have a size of 5 
        curr_state = bin(s)[2:].zfill(size)
        
    
        #print("Starting here ", curr_state)
        
        #states_name.append(curr_state)
        
        # empty string where to save the next state
        end_state = ""
            
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
        dict_net[curr_state] = end_state

        net.add_node(curr_state, label=curr_state, shape='circle')
        # add end state node to graph
        net.add_node(end_state, label=end_state, shape='circle')
        # add edge from curr to end state to graph
        net.add_edge(curr_state, end_state)

    #print(dict_net)
        
    # save network as html (open the file to see it)
    return net, dict_net
        
        