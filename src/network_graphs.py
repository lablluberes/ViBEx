################################
## Code to draw the networks graphs.
## Function - create_boolean_network_graph, draws the network of individual methods 
## Function - create_boolean_network_graph_votes, draws the network based on final collective vote. 

###############################


import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep
from networks import create_boolean_network, create_boolean_network_votes
import gravis as gv
from dash import html
from pyvis.network import Network

# created a plot that is a directional network with the binarization states
# here the graph of each network per algoritm is created 
# arguments: selected - rows to create network, methods - method to create network, data - dataset, tolerance - number of iterations
def create_boolean_network_graph(data):

    # create a figure
    #fig = plt.figure()

    net = Network(width="500px", height="500px", directed=True)
    
    # color for different algorithms networks
    #colors_node = ['skyblue','lightgreen','salmon','gold']
    
    # index
    #ind = 0

    # create new Directional graph
    #G = nx.DiGraph()
    
    # get the network (dataframe of the genes with the final vote)
    network = data


    states = []

        # iterate the new dataframe by row
    for index, row in network.iterrows():

            # add the concat of the first row 
            states.append(''.join(map(str, row)))


    # to save the numbers of self loops by each state
    self_loop = {}

    for i in range(len(states)-1):

            if states[i] == states[i+1]:
                if states[i] in self_loop:
                    self_loop[states[i]] += 1
                else:
                    self_loop[states[i]] = 1

            #G.add_edge(states[i], states[i+1])
        

    # now go through the list of states and add an edge        
    for i in range(len(states)-1):
            
            if states[i] == states[i+1]:
                if states[i] in self_loop:
                    #G.add_edge(states[i], states[i+1], label=self_loop[states[i]])
                    
                    # add curr state node to graph
                    net.add_node(states[i], label=states[i], shape='circle')
                    # add end state node to graph
                    net.add_node(states[i+1], label=states[i+1], shape='circle')
                    # add edge from curr to end state to graph
                    net.add_edge(states[i], states[i+1], label=str(self_loop[states[i]]))

            else:
                #G.add_edge(states[i], states[i+1])
                
                # add curr state node to graph
                net.add_node(states[i], label=states[i], shape='circle')
                # add end state node to graph
                net.add_node(states[i+1], label=states[i+1], shape='circle')
                # add edge from curr to end state to graph
                net.add_edge(states[i], states[i+1])
                        

    # plot the network
    #pos = nx.spring_layout(G)

    # draw and style 
    #nx.draw(G, pos, with_labels=True, node_color=colors_node[ind], font_weight="bold", arrows=True, node_size=115, font_size=10)
    #edge_labels = nx.get_edge_attributes(G, "label")
    #nx.draw_networkx_edge_labels(G, pos, edge_labels)

    #ind += 1

    #print(edge_labels.values())
    #fig = gv.d3(G, edge_curvature=0.8, edge_label_data_source='label', show_edge_label=True, 
                    #node_size_factor=2, node_label_size_factor = 2, edge_label_size_factor = 2)


    #plot = fig.to_html()
       

    return net, network




# created a plot that is a directional network with the binarization final collective vote 
# graph of final vote 
# arguments: selected - rows to create network, methods - method to create network, data - dataset, tolerance - number of iterations
def create_boolean_network_graph_votes(data):
    
    # get the dataframe of the network based on the final vote of all algorithms 
    final = pd.DataFrame(data)
    
    # create directed graph
    #G = nx.DiGraph()
    net = Network(width="500px", height="500px", directed=True)
    
    # create plot
    #fig = plt.figure()
    
    states = []
    
    # go through each row of the dataframe
    for index, row in final.iterrows():

        # concat columns together and save to state array
        states.append(''.join(map(str, row)))

    # to save the numbers of self loops by each state
    self_loop = {}

    for i in range(len(states)-1):

            if states[i] == states[i+1]:
                if states[i] in self_loop:
                    self_loop[states[i]] += 1
                else:
                    self_loop[states[i]] = 1

            #G.add_edge(states[i], states[i+1])
    
    dict_network = {}
    
    # go through each state
    for i in range(len(states)-1):
        
        if states[i] == states[i+1]:
            if states[i] in self_loop:
                #G.add_edge(states[i], states[i+1], label=self_loop[states[i]])
                
                # add curr state node to graph
                net.add_node(states[i], label=states[i], shape='circle')
                # add end state node to graph
                net.add_node(states[i+1], label=states[i+1], shape='circle')
                # add edge from curr to end state to graph
                net.add_edge(states[i], states[i+1], label=str(self_loop[states[i]]))
        else:
            #G.add_edge(states[i], states[i+1])

            # add curr state node to graph
            net.add_node(states[i], label=states[i], shape='circle')
            # add end state node to graph
            net.add_node(states[i+1], label=states[i+1], shape='circle')
            # add edge from curr to end state to graph
            net.add_edge(states[i], states[i+1])
        
        dict_network[states[i]] = states[i+1]

    #print(dict_network)
    #pos = nx.spring_layout(G)
  
    # draw and styling
    #nx.draw(G, pos, with_labels=True,node_color="skyblue",font_weight="bold", arrows=True, node_size=115, font_size=10)
    #edge_labels = nx.get_edge_attributes(G, "label")
    #nx.draw_networkx_edge_labels(G, pos, edge_labels)

    #fig = gv.d3(G, edge_curvature=0.8, edge_label_data_source='label', show_edge_label=True, 
    #                node_size_factor=2, node_label_size_factor = 2, edge_label_size_factor = 2)
    
    # return figure and final dataframe network
    return  net, final


def rules_graph(selected, method, data, rules, thr_b, thr_k, thr_s, thr_o, displacement):
     
    final = network_rules2(selected, method, data, rules, thr_b, thr_k, thr_s, thr_o, displacement)

    # create directed graph
    G = nx.DiGraph()
    
    # create plot
    fig = plt.figure()
    
    states = []
    
    # go through each row of the dataframe
    for index, row in final.iterrows():

        # concat columns together and save to state array
        states.append(''.join(map(str, row)))

    # to save the numbers of self loops by each state
    self_loop = {}

    for i in range(len(states)-1):

            if states[i] == states[i+1]:
                if states[i] in self_loop:
                    self_loop[states[i]] += 1
                else:
                    self_loop[states[i]] = 1

            #G.add_edge(states[i], states[i+1])
     
    
    # go through each state
    for i in range(len(states)-1):
        
        if states[i] == states[i+1]:
            if states[i] in self_loop:
                G.add_edge(states[i], states[i+1], label=self_loop[states[i]])
        else:
            G.add_edge(states[i], states[i+1])

    
    pos = nx.spring_layout(G)
  
    # draw and styling
    nx.draw(G, pos, with_labels=True,node_color="skyblue",font_weight="bold", arrows=True, node_size=115, font_size=10)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    fig = gv.d3(G, edge_curvature=0.8, edge_label_data_source='label', show_edge_label=True, 
                    node_size_factor=2, node_label_size_factor = 2, edge_label_size_factor = 2)
    
    # return figure and final dataframe network
    return  fig.to_html(), final

    '''# create directed graph
    G = nx.DiGraph()
    
    # create plot
    fig = plt.figure()
    
    
    size = len(final.columns)

    for index, row in final.iterrows():
        curr_state = ''.join(map(str, row[:size//2]))
        next_state = ''.join(map(str, row[size//2:]))

        G.add_edge(curr_state, next_state)
        
        #print(curr_state, next_state)

    
    pos = nx.spring_layout(G)
  
    # draw and styling
    nx.draw(G, pos, with_labels=True,node_color="skyblue",font_weight="bold", arrows=True, node_size=115, font_size=10)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    fig = gv.d3(G, graph_height=200, edge_curvature=0.8, edge_label_data_source='label', show_edge_label=True, 
                    node_size_factor=2, node_label_size_factor = 2, edge_label_size_factor = 2)
    
    # return figure and final dataframe network
    return  fig.to_html(), final'''


def rules_graph_vote(selected, method, data, rules, thr_b, thr_k, thr_s, thr_o, displacement):
     
    final = network_rules_vote2(selected, method, data, rules, thr_b, thr_k, thr_s, thr_o, displacement)

    # create directed graph
    G = nx.DiGraph()
    
    # create plot
    fig = plt.figure()
    
    states = []
    
    # go through each row of the dataframe
    for index, row in final.iterrows():

        # concat columns together and save to state array
        states.append(''.join(map(str, row)))

    # to save the numbers of self loops by each state
    self_loop = {}

    for i in range(len(states)-1):

            if states[i] == states[i+1]:
                if states[i] in self_loop:
                    self_loop[states[i]] += 1
                else:
                    self_loop[states[i]] = 1

            #G.add_edge(states[i], states[i+1])
     
    
    # go through each state
    for i in range(len(states)-1):
        
        if states[i] == states[i+1]:
            if states[i] in self_loop:
                G.add_edge(states[i], states[i+1], label=self_loop[states[i]])
        else:
            G.add_edge(states[i], states[i+1])

    
    pos = nx.spring_layout(G)
  
    # draw and styling
    nx.draw(G, pos, with_labels=True,node_color="skyblue",font_weight="bold", arrows=True, node_size=115, font_size=10)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    fig = gv.d3(G, edge_curvature=0.8, edge_label_data_source='label', show_edge_label=True, 
                    node_size_factor=2, node_label_size_factor = 2, edge_label_size_factor = 2)
    
    # return figure and final dataframe network
    return  fig.to_html(), final

    #print(final)
    # create directed graph
    '''G = nx.DiGraph()
    
    # create plot
    fig = plt.figure()
    
    
    size = len(final.columns)

    for index, row in final.iterrows():
        curr_state = ''.join(map(str, row[:size//2]))
        next_state = ''.join(map(str, row[size//2:]))

        G.add_edge(curr_state, next_state)
        
        #print(curr_state, next_state)

    
    pos = nx.spring_layout(G)
  
    # draw and styling
    nx.draw(G, pos, with_labels=True,node_color="skyblue",font_weight="bold", arrows=True, node_size=115, font_size=10)
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    fig = gv.d3(G, graph_height=200, edge_curvature=0.8, edge_label_data_source='label', show_edge_label=True, 
                    node_size_factor=2, node_label_size_factor = 2, edge_label_size_factor = 2)
    
    # return figure and final dataframe network
    return  fig.to_html(), final'''
   