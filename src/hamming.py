import pandas as pd
import numpy as np

def hamming_state_by_state(network_rules, network, method):
    
    df = pd.DataFrame(columns=[method + 'State', 'Hamming'])
    
    df.loc[len(df.index)] = [network[0], '-'] 
    
    num_state = len(network[0]) * len(network)
    
    count = 0
    
    for i in range(len(network)-1):
        
        s1 = network[i+1]
        
        if network_rules.get(network[i]):
            s2 = network_rules[network[i]]
        
            #print(s1, s2)
            hamming = 0

            for j in range(len(s1)):

                if s1[j] != s2[j]:
                    hamming += 1
                    count += 1
        
        else:
            
            hamming = "Does not exist"
                
        df.loc[len(df.index)] = [s1, hamming] 
    
    #print(f"Score is {count} / {num_state}")
    
    perc = np.around(((count / num_state) * 100), 2)
    
    df.loc[len(df.index)] = ["Score", str(perc)+"%"] 
    
    return df



def hamming_chain(network_rules, elected_network):
    
    df = pd.DataFrame(columns=['Elected States', 'Boolean Function Chain', 'Hamming'])
    
    num_state = len(elected_network[0]) * len(elected_network)
    
    count = 0
    
    does_not_exist = False
    
    s = elected_network[0]
    
    chain_network = [s]
    
    if not network_rules.get(s):

        #"Cannot analyze network because initial state does not exist in Boolean Function Network"
        
        return df, False
    
    for i in range(len(elected_network)-1):
        
        s = network_rules[s]
        
        chain_network.append(s)
        
    
    for i in range(len(chain_network)):
        
        s1 = elected_network[i]
        s2 = chain_network[i]
        
        hamming = 0
        
        for j in range(len(s1)):
            
            if s1[j] != s2[j]:
                hamming += 1
                count += 1
            
            
        df.loc[len(df.index)] = [s1, s2, hamming] 
        
    perc = np.around(((count / num_state) * 100), 2)
    
    df.loc[len(df.index)] = ["Score", "", str(perc)+"%"] 
    
    return df, True
    


def hamming_initial_final(network, network_rules):
    
    num_state = len(network)
    
    count_dif = 0
    
    s = network[0]
    
    chain_network = [s]
    
    initial_same = True
    final_same = True
    
    if not network_rules.get(s):
        
        return [False, s]
    
    for i in range(len(network)-1):
        
        s = network_rules[s]
        
        chain_network.append(s)
        
    if network[0] != chain_network[0]:
        
        initial_same = False
        count_dif += 1
        
    if network[-1] != chain_network[-1]:
        
        final_same = False
        count_dif += 1
        
        
    inter_dif = 0
    
    for i in range(1, len(chain_network)-1):
        
        s1 = network[i]
        s2 = chain_network[i]
        
        
        if s1 != s2:
            count_dif += 1
            inter_dif += 1
              
    perc = np.around(((count_dif / num_state) * 100), 2)
    
    return [initial_same, final_same, inter_dif, perc]
    


def generate_init_final_comparison(data_algos, network_rules):
    
    df = pd.DataFrame(columns=['Threshold Method', 'Initial State', 'Final State', '# Intermediate states', 'Score'])
    
    for column in data_algos:

        columnSeriesObj = data_algos[column]
    
        result = hamming_initial_final(columnSeriesObj.values, network_rules)

        if result[0] == False:
            df.loc[len(df.index)] = [column, f"Cannot analyze network because of undecided state: {result[1]}. Change state undecided values to analyze.", None, None, None]
        
        else:
            df.loc[len(df.index)] = [column, "Same State" if result[0] else "Different State", "Same State" if result[1] else "Different State", result[2], result[3]]
        
    return df

