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
import ast
from itertools import product
from networks.booleanParser import runBooleanParser

# function that reads the rules of the csv and creates a boolean network of all posible states
# the parameters is the csv file as a dataframe
def createNetwork(rules_df):
    """
        createNetwork - generates BN of all possible states based on rules

        rules_df: Boolean functions
    
    """

    # lexicography of each BN states
    lexi = [True, False]
    
    # gene names
    names = list(rules_df['Gene'].values)

    # generate all 2^N states 
    states = product(lexi, repeat=len(names))
    
    # to sabe rules and genes that are fixed values
    rules_dict = {}
    fixed_rules = {}
    
    # read each row of the dataframe 
    for index, row in rules_df.iterrows():
 
        # save rule of that gene to rules_dict. example: rules_dict = {'x1': 'x1 or x2'}
        # if rule is empty make the state stay the same 
        if row['Rule'] == '':
            # gene has no rule then keep state as the same 
            rules_dict[row['Gene']] = row['Gene']
        
        else:
            rules_dict[row['Gene']] = row['Rule']
        
        # verifies if boolean function is a fixed value "True" or "False"
        try:
            # verift rule is just a True or False (no variables)
            boolValue = ast.literal_eval(row['Rule'])
            # save the gene that is fixed value 
            fixed_rules[row['Gene']] = boolValue
        except Exception as e:
            pass
    
    # save BN state transitions
    dict_net = {}
    
    #print(rules_dict)
    
    #print(fixed_rules)
    
    # to exit current loop iteration when a state has a value that contradicts fixed value 
    condition = False
    
    # BN plot 
    net = Network(width="450px", height="450px", directed=True)
    
    # iterate all 2^N states 
    for s in states:

        # convert current state and names of genes to a dictionary. For example: (False, True), ['A', 'B'] -> {'A': False, 'B': True}
        curr_state_dict = dict(zip(names,s))
        
        # convert current state to a string 
        curr_state_string = [str(int(e)) for e in s]
        curr_state_string = ''.join(curr_state_string)
        
        # to save the next state after applying rules
        next_state_string = ''
        
        # verify that state exists when some genes are fixed values
        for r in fixed_rules:
            # if a gene if fixed based on rules and the current state is not that fixed 
            # value then skip applying rule to state and skip iteration
            if curr_state_dict[r] != fixed_rules[r]:
                condition = True
                continue
        
        # skip iteration
        if condition:
            condition = False
            continue
        
        # iterate across Boolean functions to apply to each bin state
        for r in rules_dict:
            # calls the parser to apply dictionary of gene values to boolean function
            result = runBooleanParser(curr_state_dict, rules_dict[r])
            # append the rule result to the next state string
            next_state_string += str(int(result))
           
        # if the current state already exist in the BN dictionary skip iteration 
        if curr_state_string in dict_net:
            continue
        
        # label for toolip of plot. For both current state and next state 
        title_label1 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(names, list(curr_state_string)))
        title_label2 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(names, list(next_state_string)))

        # adds current state as node with toolip
        net.add_node(curr_state_string, label=curr_state_string, shape='circle', title=title_label1)
        
        
        # verifies if next state does not exist as key in BN dictionary
        if next_state_string not in dict_net.keys():
            # add next state as a node with toolip
            net.add_node(next_state_string, label=next_state_string, shape='circle', title=title_label2)
        
        # adds an edge from current state to next state node
        net.add_edge(curr_state_string, next_state_string)
        
        # add transition to dictionary
        dict_net[curr_state_string] = next_state_string
        
        #print(curr_state_dict)
    
    # find attractors of BN 
    Atts_syn, Att_num = attractors(dict_net)
    
    # iterate nodes and color attractors 
    for nodes in net.nodes:
        # if node is an attractor color as lightgray
        if nodes['id'] in Atts_syn:
            nodes['color'] = 'lightgray'

    
    #net.save_graph("plot.html")
    
    return net, dict_net

"""
if __name__ == "__main__":
    
    rules = {'Gene':['ATM', 'p53', 'WIP1', 'MDM2'],  
             'Rule':['(not WIP1) and (ATM or True)', '(not MDM2) and (ATM or WIP1)', 'p53', '(not ATM) and (p53 or WIP1)']}
    
    rules2 = {'Gene':['lexA', 'uvrD', 'recA', 'uvrA', 'polB', 'umuD'],
             'Rule':['not recA', 'not lexA', 'True', 'not lexA', 'not lexA', 'not lexA']}
    df = pd.DataFrame(rules)
    
    createNetwork(df)"""
    
    
########## OLD FUNCTION WITHOUT PARSING. USES ONLY EVAL
# function that reads the rules of the csv and creates a boolean network of all posible states
# the parameters is the csv file as a dataframe
def createNetwork2(rules_df):
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
        # if rule is empty make the state stay the same 
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
        
        
        