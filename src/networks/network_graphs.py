################################
# File contains the functions to create network graph for each binarization
###############################


import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from threshold_methods.methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep
from networks.networks import create_boolean_network, create_boolean_network_votes
import gravis as gv
from dash import html
from pyvis.network import Network
import string

# created a plot that is a directional network with the binarization states
# here the graph of each network per algoritm is created 
def create_boolean_network_graph(data):
    """
        create_boolean_network_graph -  create network of binarization 

        data: binarized dataset
    """


    # initialize network as directed
    net = Network(width="500px", height="500px", directed=True)
    
    # get the network 
    network = data
    states = []

    # iterate the new dataframe by row
    for index, row in network.iterrows():

            # add concadenate columns as a single string (state)
            states.append(''.join(map(str, row)))


    # labels of network (edges)
    labels_network = {}
    # name of genes 
    data_columns = data.columns

    first_node = ""
    string_legend = f"Gene by Position:\n"

    first_node = ""

    for i in range(len(data_columns)):
        first_node += f"{i+1} "
        string_legend += f"{i+1} = {data_columns[i]}\n"

    #net.add_node("node_legend", label=first_node, color='yellow', shape='circle') # x=0, y=-370, physics=False, fixed=True)

    net.add_node("legend", label=string_legend, #x=0, y=-250,
             shape='box', physics=True, fixed=False, color='lightgray')
    
    #net.add_edge("node_legend", "legend")

    # now go through the list of states and add an edge        
    for i in range(len(states)-1):
            
            # if state was not added add a single number to edge 
            if states[i] not in labels_network:
        
                labels_network[states[i]] = {states[i+1]:[i+1]}
            
            # append new iteration for edge
            else:
                # if next state is in label add iteration 
                if states[i+1] in labels_network[states[i]]:
                    labels_network[states[i]][states[i+1]].append(i+1)
            
                # initialize iteration edge number
                else:
                    labels_network[states[i]][states[i+1]] = [i+1]

            # the title (toolip) for each state node. Assigns gene names and the binary value in curr state
            title_label1 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(data_columns, states[i]))
            
            # the title (toolip) for each state node. Assigns gene names and the binary value in next state
            title_label2 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(data_columns, states[i+1]))
            
            # if its the last state then color as an attractor 
            if states[i] == states[-1]:
                # add curr state node to graph
                net.add_node(states[i], label=states[i], shape='circle', title=title_label1, color='lightgray')

            # add curr state node to graph
            else:
                net.add_node(states[i], label=states[i], shape='circle', title=title_label1)

            # add end state node to graph color as attractor if its the last
            if states[i+1] == states[-1]:
                net.add_node(states[i+1], label=states[i+1], shape='circle', title=title_label2, color='lightgray')

            # add node 
            else:
                net.add_node(states[i+1], label=states[i+1], shape='circle', title=title_label2)
                
            
            # verifies if edge connection already exists
            if {'from':states[i], 'to':states[i+1], 'arrows': 'to', 'color': '#97c2fc'} in net.edges:
                continue

            # add edge 
            else:
                net.add_edge(states[i], states[i+1], color = '#97c2fc')


    # to add labels to edges (iterations)
    legend_edges = {}
    letters1 = list(string.ascii_lowercase)
    letters = list(string.ascii_lowercase)
    index = 0
    index_lett = 0

    #print("index:", len(letters))

    # iterate edges
    for edge in net.edges:
        
        # edge starting and arrival nodes
        f = edge['from']
        t = edge['to']

        # if the iteration of edge is greater than 2 add legend (letter) and toolip
        if len(labels_network[f][t]) > 2:
            
            # resets index to have more letters 
            if index == len(letters):
                index = 0
                
                # creates more letters 
                letters = [letters[i] + letters1[index_lett] for i in range(len(letters))]
                index_lett += 1
            
            # get a letter 
            let = letters[index]

            # if the letter in not in edges add it 
            if let not in legend_edges:
                # adds letter to edge
                edge['label'] = let

                # adds toolip
                edge['title'] = f"{let}={labels_network[f][t]}"

                # assign letter and values in dict
                legend_edges[let] = str(labels_network[f][t])
                index += 1

        # 2 or 1 iterations then add numbers directly in edge (instead of letter)
        else:
        
            edge['label'] = ", ".join(map(str, labels_network[f][t]))
       

    return net, network, legend_edges




# created a plot that is a directional network with the binarization final collective vote 
# graph of final vote 
def create_boolean_network_graph_votes(data):
    """
        create_boolean_network_graph_votes -  create network of elected binarization

        data: elected binarization
    """
    
    # get the dataframe of the network based on the final vote of all algorithms 
    final = pd.DataFrame(data)
    
    # create directed graph
    net = Network(width="500px", height="500px", directed=True)
    
    states = []
    
    # go through each row of the dataframe
    for index, row in final.iterrows():

        # concat columns together and save to state array
        states.append(''.join(map(str, row)))

    
    dict_network = {}
    labels_network = {}
    data_columns = final.columns

    first_node = ""
    string_legend = f"Gene by Position:\n"

    first_node = ""

    for i in range(len(data_columns)):
        first_node += f"{i+1} "
        string_legend += f"{i+1} = {data_columns[i]}\n"

    #net.add_node("node_legend", label=first_node, color='yellow', shape='circle') # x=0, y=-370, physics=False, fixed=True)

    net.add_node("legend", label=string_legend, #x=0, y=-250,
             shape='box', physics=True, fixed=False, color='lightgray')
    
    # go through each state
    for i in range(len(states)-1):
        
        # adds iteration number of edge 
        if states[i] not in labels_network:
        
            labels_network[states[i]] = {states[i+1]:[i+1]}
        
        else:
            # keeps appending numbers to edges repeated 
            if states[i+1] in labels_network[states[i]]:
                labels_network[states[i]][states[i+1]].append(i+1)
           
            else:
                labels_network[states[i]][states[i+1]] = [i+1]

        # nodes toolip showing values of each gene
        title_label1 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(data_columns, states[i]))
        
        title_label2 = "\n".join(f"{gene}: {bin}" for gene, bin in zip(data_columns, states[i+1]))
        
        # adds last node as an attractor
        if states[i] == states[-1]:
            net.add_node(states[i], label=states[i], shape='circle', title=title_label1, color='lightgray')

        # add curr state node to graph
        else:
            net.add_node(states[i], label=states[i], shape='circle', title=title_label1)

        # adds last node as an attractor
        if states[i+1] == states[-1]:
            net.add_node(states[i+1], label=states[i+1], shape='circle', title=title_label2, color='lightgray')

        # add curr state node to graph
        else:
            net.add_node(states[i+1], label=states[i+1], shape='circle', title=title_label2)
        
        # verifies if edge does not already exist
        if {'from':states[i], 'to':states[i+1], 'arrows': 'to', 'color': '#97c2fc'} in net.edges:
            continue

        # adds edge to network
        else:
            net.add_edge(states[i], states[i+1], color = '#97c2fc')


        # network as dictionary
        dict_network[states[i]] = states[i+1]


    # for edges labels 
    legend_edges = {}
    letters1 = list(string.ascii_lowercase)
    letters = list(string.ascii_lowercase)
    index = 0
    index_lett = 0

    # iterates edges 
    for edge in net.edges:
        
        f = edge['from']
        t = edge['to']

        # verifies if edge has more than 2 iterations
        if len(labels_network[f][t]) > 2:

            # resets letters once reached maximum 
            if index == len(letters):
                index = 0
                
                letters = [letters[i] + letters1[index_lett] for i in range(len(letters))]
                index_lett += 1
            
            let = letters[index]

            # adds letter to edge
            if let not in legend_edges:
                # add letter to edge
                edge['label'] = let

                # add toolip to edge
                edge['title'] = f"{let}={labels_network[f][t]}"

                # save letter and iterations
                legend_edges[let] = str(labels_network[f][t])
                index += 1

        # adds numbers directly to edges if only 1 or 2 iterations occur
        else:
        
            edge['label'] = ", ".join(map(str, labels_network[f][t]))
        
    
    return  net, final, legend_edges



def create_GRN_plot(df):
    
    genes = list(df['Gene'].values)
    rules = list(df['Rule'].values)
    
    net = Network(width="450px", height="450px", directed=True)
    #net.toggle_physics(False)

    string_legend = f"Legend:\n - Node: Genes\n - Green Arrow: Activation\n - Red Arrow: Inhibition\n"

    net.add_node("legend", label=string_legend, #x=0, y=-250,
                shape='box', physics=True, fixed=False, color='lightgray')

    for i in genes:
        net.add_node(i, label=i, shape="ellipse", color="#e0cd95")

    for i in range(len(rules)):
        
        r = rules[i].replace(" ", "")
        
        if "True" in r:
            net.add_node('1', label='1', shape="ellipse", color="#e0cd95")
            net.add_edge('1', genes[i], color="green")
        
        if "False" in r:
            net.add_node('0', label='0', shape="ellipse", color="#e0cd95")
            net.add_edge('0', genes[i], color="green")
        
        for j in genes:
            
            #r = r.replace("not", "not ")
            
            #print(r, len(r))
            
            #if f"not {j}" in r and j in r:
            #    net.add_edge(j, genes[i], color="black")
                
            if f"not{j}" in r:
                #print("swi")
                net.add_edge(j, genes[i], color="red")
                
            elif j in r:
                #print(f"from {j} to {genes[i]}")
                net.add_edge(j, genes[i], color="green")
            else:
                continue
                

    
    return net
            
