


def HammingDistance(votes):

    genes_binarized = votes[0]

    n = len(genes_binarized)

    #print(n)

    distance = 0

    size_vect = len(genes_binarized[0])

    #print(size_vect)

    for i in range(n):
        for j in range(i+1, n):

            #print(genes_binarized[i], genes_binarized[j])

            for k in range(size_vect):
                
                if genes_binarized[i][k] != genes_binarized[j][k]:
                    distance += 1
    
    return distance, size_vect


            
#genes = [[[0,1,0], [1,0,0], [1,1,0]]]
         
#print(HammingDistance(genes))


def process_hamming(network_rule, network):
    #print(network_rule.iloc[0].values, len(network_rule))
    
    n = network_rule.copy()
    
    
    for row in range(len(network_rule)):
        
        net1_row = network_rule.iloc[row].values
        net2_row = network.iloc[row].values
        
        #ham = net1_row - net2_row 

        ham = 0

        for i in range(len(net1_row)):

            if net1_row[i] != net2_row[i]:
                ham += 1
     
        #sum_ham = sum(abs(ham))
        
        n.at[row, 'Hamming'] = ham
        
    #print(n)
        
    return n