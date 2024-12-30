################################
## Code to generate the voting table 
## Function - binVoting, voting mechanism based on Lluberes and Seguel paper. 
## Function - binarizationVoting, voting mechanism created by Andrea 

###############################

import math
import numpy as np
#threshold/displacement indexes are vectors with values in them
#for different algorithms


#Algorithm in Lluberes paper

def binVoting(gene, threshold, displacement):
    
    alg = len(threshold)
    x = len(gene)
    #NULL STRING TO STORE RESULT BIN STRING
    z = []
    #NULL 2D ARRAY TO STORE VOTING RESULTS 
    res = np.empty([alg,3])
    
    for j in range(x):
        for i in range(alg):
        #CALCULATE RESULTS
            U = (gene[j] + displacement[i] < threshold[i]) and (abs(threshold[i] - gene[j]) > displacement[i])
            N = abs(threshold[i] - gene[j]) <= displacement[i]
            E = not (U or N)
            
            res[i][0] = U
            res[i][1] = N
            res[i][2] = E
        #COMPUTE MAJORITY VOTE 
        
        E = sum(res[:,2]) > alg/2
        N = sum(res[:,1]) > alg/2
        U = sum(res[:,0]) > alg/2
        
        if ((E != (not(U or N))) or (N)):
            z.append('?')
        elif E:
            z.append(1)
        else:
            z.append(0)
       
    return z

#Andrea's algorithm (i made it myself based on the table!!!)

def binarizationVoting(gene, threshold, displacement):

    #2d array that stores algorithm results
    #x axis is gene
    #y axis is algorithm

    alg = len(threshold)
    n = len(gene)

    algos = np.zeros([alg, n])

    #get results for every algorithm
    for i in range(alg): 
        for j in range(n):
            # if this is true the expression is not expressed
            if (gene[j] + displacement[i] < threshold[i]) and (abs(threshold[i] - gene[j]) > displacement[i]):
                #algos[i][j] = 1
                algos[i][j] = 0
            # if true the expression is undecided
            elif(abs(threshold[i] - gene[j]) <= displacement[i]):
                #algos[i][j] = 2
                algos[i][j] = -1
            # else the expression is expressed
            else:
                #algos[i][j] = 3
                algos[i][j] = 1

    #id 
    # 1 -> U
    # 2 -> N
    # 3 -> E
    
    # new ids
    # unexpresed -> 0
    # expresed -> 1
    # undefined -> nan

    # start counting votes
    majority = np.zeros(n)
       
    for i in range(n):

        #array of tally votes
        results = algos[:,i]
        #U = np.count_nonzero(results == 1)
        #N = np.count_nonzero(results == 2)
        #E = np.count_nonzero(results == 3)
        
        U = np.count_nonzero(results == 0)
        N = np.count_nonzero(results == -1)
        E = np.count_nonzero(results == 1)

        #binarize tally votes
        tally = [U,N,E]
        for j in range(3):
            #if algorithms is an even number this will be half, else itll be a
            #number rounded up from half ex. 3 -> 1.5 becomes 2
            if tally[j] >= math.ceil(alg/2):
                tally[j] = 1
            else:
                tally[j] = 0

        #first check if final tally contradicts itself
        if sum(tally) != 1:
            majority[i] = -1
        #then check other cases
        else:
            if tally[0] == 1:
                majority[i] = 0
            elif tally[1] == 1:
                majority[i] = -1
            else:
                majority[i] = 1

    algo = []
    majority = list(majority)
    
    for row in algos:
        line = list(row)
        for i in range(len(line)):
            if line[i] == -1:
                line[i] = '?'
        
        algo.append(line)
    
    for i in range(len(majority)):
        if majority[i] == -1:
            majority[i] = '?'

     #return 2d array of votes + final votes
    return algo, majority