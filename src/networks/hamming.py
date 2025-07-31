##############################################
#
# This file contains function that create Hamming analysis
#
##############################################
import pandas as pd
import numpy as np

def hamming_state_by_state(network_rules, network, method):
    """
        hamming_state_by_state - makes Hamming analysis state by state

        network_rules: BN based on rules
        network: binary path based on a binarization
        method: binarization method used
    """
    
    # create dataframe 
    df = pd.DataFrame(columns=[method + ' State', 'Hamming'])
    
    # dont compare first state
    df.loc[len(df.index)] = [network[0], '-'] 
    
    # number of binary states 
    num_state = len(network[0]) * len(network)
    
    count = 0
    
    # iterate binarization states
    for i in range(len(network)-1):
        
        # get next state based on binarization 
        s1 = network[i+1]
        
        # verify parent state exists in rules network
        if network_rules.get(network[i]):
            # get transition based on rules 
            s2 = network_rules[network[i]]
        
            #print(s1, s2)

            # hamming counter
            hamming = 0

            # counts hamming difference between states
            for j in range(len(s1)):

                if s1[j] != s2[j]:
                    hamming += 1
                    count += 1
        
        # if state has undecided it does not exist in rules network
        else:
            
            hamming = "Does not exist"

        # had row to table      
        df.loc[len(df.index)] = [s1, hamming] 
    
    #print(f"Score is {count} / {num_state}")
    
    # calculate score of percentage of hamming diff
    perc = np.around(((count / num_state) * 100), 2)
    
    # add row with score
    df.loc[len(df.index)] = ["Score", str(perc)+"%"] 
    
    return df



def hamming_chain(network_rules, elected_network):
    """
        hamming_chain - creates Hamming chain analysis (compares elected states to path generated from rules)

        network_rules: network based on rules
        elected_network: elected binarization
    """
    
    # create dataframe with columns
    df = pd.DataFrame(columns=['Elected States', 'Boolean Function Chain', 'Hamming'])
    
    # total number of binary states
    num_state = len(elected_network[0]) * len(elected_network)
    
    count = 0
    
    does_not_exist = False
    
    # get first state of elected network
    s = elected_network[0]
    
    chain_network = [s]
    
    # if state has undecided value then does not exist in rules BN
    if not network_rules.get(s):

        #"Cannot analyze network because initial state does not exist in Boolean Function Network"
        
        return df, False
    
    # extract a path of size of elected network from rules based on first state from elected
    for i in range(len(elected_network)-1):
        
        s = network_rules[s]
        
        chain_network.append(s)
        
    # iterate over chain extracted 
    for i in range(len(chain_network)):
        
        # state from elected and rules BN
        s1 = elected_network[i]
        s2 = chain_network[i]
        
        hamming = 0
        
        # compare both states using hamming
        for j in range(len(s1)):
            
            if s1[j] != s2[j]:
                hamming += 1
                count += 1
            

        # add hamming and states as a row   
        df.loc[len(df.index)] = [s1, s2, hamming] 
    
    # score for hamming 
    perc = np.around(((count / num_state) * 100), 2)
    
    # add score as row 
    df.loc[len(df.index)] = ["Score", "", str(perc)+"%"] 
    
    return df, True
    


def hamming_initial_final(network, network_rules):
    """
        hamming_initial_final - makes initial and final state Hamming analysis

        network: takes binarization 
        network_rules: network from rules
    
    """
    
    # number of states in binarized genes 
    num_state = len(network)
    
    count_dif = 0
    
    # first state of binarized genes
    s = network[0]
    
    # the first state of the extracted path of rules (same as first state of binarizations)
    chain_network = [s]
    
    initial_same = True
    final_same = True
    
    # if first state has undecided values dont do analysis
    if not network_rules.get(s):
        
        return [False, s]
    
    # extract path from rules based on first state of binarization
    for i in range(len(network)-1):
        
        s = network_rules[s]
        
        chain_network.append(s)
    
    # verifies first state are equal
    if network[0] != chain_network[0]:
        
        initial_same = False
        count_dif += 1
    
    # verifies final state are equal
    if network[-1] != chain_network[-1]:
        
        final_same = False
        count_dif += 1
        
        
    inter_dif = 0
    
    # does Hamming for intermediate states 
    for i in range(1, len(chain_network)-1):
        
        s1 = network[i]
        s2 = chain_network[i]
        
        
        if s1 != s2:
            count_dif += 1
            inter_dif += 1

    # creates score    
    perc = np.around(((count_dif / num_state) * 100), 2)
    
    # returns information 
    return [initial_same, final_same, inter_dif, perc]


def hamming_score_chain(network, network_rules):
    """
        hamming_score_chain - returns transition match and similarity scores

        network: binarized genes
        network_rules: BN from rules
    """
    
    # number of states of binarized genes
    num_state = len(network)
    
    count_dif = 0
    perc_dif = 0
    
    # first state of binarized genes
    s = network[0]
    
    # add first state to extracted chain
    chain_network = [s]
    
    # return false if it has undecided value 
    if not network_rules.get(s):
        
        return False
    
    # extract chain from rules
    for i in range(len(network)-1):
        
        s = network_rules[s]
        
        chain_network.append(s)
        
    # iterate over extracted chain
    for i in range(0, len(chain_network)):
        
        s1 = network[i]
        s2 = chain_network[i]
        
        # count states that are different
        for j in range(len(s1)):
            if s1[j] != s2[j]:
                count_dif += 1
        
        # verify if next states are the same 
        if i > 0 and i < num_state-1:
            if network[i+1] == chain_network[i+1]:
                perc_dif += 1
                
        
    # total number of binary states  
    total_states = len(network[0]) * num_state

    # calculate similarity and transition match
    similarity = np.round(((total_states - count_dif)/total_states) * 100, 2)
    transition = np.round((perc_dif/num_state) * 100, 2)
    
    return [similarity, transition]

def generate_init_final_comparison(data_algos, network_rules):
    """
        generate_init_final_comparison - generate table init final comparison for selected methods

        data_algos: binarization of all methods
        network_rules: BN from rules
    """
    
    # create dataframe with column names
    df = pd.DataFrame(columns=['Threshold Method', 'Initial State', 'Final State', '# Intermediate states different', 'Silimarity (%)', 'Transition Match (%)'])
    
    # for each binarization do the analysis
    for column in data_algos:

        # extract binarization 
        columnSeriesObj = data_algos[column]

        # get hamming analysis
        result = hamming_initial_final(columnSeriesObj.values, network_rules)

        # get similarity and transmatch score 
        similarity = hamming_score_chain(columnSeriesObj.values, network_rules)

        # error for when a state has an undecided state
        if result[0] == False:
            df.loc[len(df.index)] = [column, f"Cannot analyze network because of undecided state: {result[1]}. Change state undecided values to analyze.", None, None, None, None]
        
        # add row on table 
        else:
            df.loc[len(df.index)] = [column, "Same State" if result[0] else "Different State", "Same State" if result[1] else "Different State", result[2], similarity[0], similarity[1]]
        
    return df



def extract_path(state, net_dict, n, labels, net):
    """
        extract_path - paints path from Boolean network rules

        state: first state of path
        net_dict: network as dictionary
        n: length of path
        labels: gene labels
        net: 
    """

    data = []

    # extracts n length path
    for i in range(n):
        
        # get nodes from network
        for node in net.nodes:
            
            # if the node is the current path state paint it 
            if node['label'] == state:
                
                # paint node if its not attractor
                if node['color'] != 'lightgray':
                    node['color']= 'lightgreen'

        # turn state to list
        state_split = list(state)

        # append state and labels as dictionary
        data.append(dict(zip(labels, state_split)))

        # get next state from path
        state = net_dict[state]

    return data, net

'''if __name__ == "__main__":

    n = 10

    state = '000000'

    labels = ['orx', 'val', 'polb']

    net_dict = {'000000': '000000', '000001': '000010', '000010': '000010', '000011': '000010', '000100': '000010', '000101': '000010', '000110': '000010', '000111': '000010', '001000': '000010', '001001': '000010', '001010': '000010', '001011': '000010', '001100': '000010', '001101': '000010', '001110': '000010', '001111': '000010', '010000': '000010', '010001': '000010', '010010': '000010', '010011': '000010', '010100': '000010', '010101': '000010', '010110': '000010', '010111': '000010', '011000': '000010', '011001': '000010', '011010': '000010', '011011': '000010', '011100': '000010', '011101': '000010', '011110': '010010', '011111': '000010', '100000': '000010', '100001': '000010', '100010': '000010', '100011': '000010', '100100': '000010', '100101': '000010', '100110': '000010', '100111': '000010', '101000': '000010', '101001': '000010', '101010': '000010', '101011': '000010', '101100': '000010', '101101': '000010', '101110': '000010', '101111': '001111', '110000': '000010', '110001': '000010', '110010': '000010', '110011': '000010', '110100': '000010', '110101': '000010', '110110': '000010', '110111': '000010', '111000': '000010', '111001': '000010', '111010': '000010', '111011': '000010', '111100': '000010', '111101': '000010', '111110': '100010', '111111': '000010'}

    print(extract_path(state, net_dict, n, labels))'''