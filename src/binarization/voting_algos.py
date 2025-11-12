################################
## Code to generate the voting table 
## Function - binVoting, voting mechanism based on Lluberes and Seguel paper. 
## Function - binarizationVoting, voting mechanism created by  
## Function - election_strings, voting mechanism based on Lluberes thesis (made by )
###############################

import math
import numpy as np
#from binarization.normalize import geneNorm
import pandas as pd
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

#'s algorithm (i made it myself based on the table!!!)

def binarizationVoting(gene, threshold, displacement):

    #2d array that stores algorithm results
    #x axis is gene
    #y axis is algorithm

    alg = len(threshold)
    n = len(gene)

    algos = np.zeros([alg, n], dtype=int)

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
    majority = np.zeros(n, dtype=int)
       
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

def majority(N, U, E, thr):
    """
        majority - verifies which state have a majority of tie 

        N: 
        U:
        E:
        thr: thr values 
    """

    tie = False

    U_true = U.count(True)
    N_true = N.count(True)
    E_true = E.count(True)

    U_false = U.count(False) 
    N_false = N.count(False) 
    E_false = E.count(False) 

    if U_true == U_false:

        tie = True

    if N_true == N_false:

        tie = True
    
    if E_true == E_false:

        tie = True

    if U_true >= U_false:

        U = True
    
    else:

        U = False

    if N_true >= N_false:

        N = True

    else:

        N = False

    if E_true >= E_false:

        E = True
    
    else:

        E = False

    return U, N, E, tie
    

def election_strings(G, thr, disp):
    """
        election_strings - makes election strings and binarizes genes

        G: gene expression
        thr: threshold values
        disp: displacement of gene 
    """

    # to stpre elecred string
    Z_e = []

    # to save each thr binarization 
    collective = [[] for _ in range(len(thr))]

    U = []
    N = []
    E = []

    # iterates over gene expression
    for j in range(len(G)):
        # iterate over selected thr methods 
        for i in range(len(thr)):

            uvar = ((G[j] + disp[i]) < thr[i]) and (abs(thr[i] - G[j]) > disp[i])

            nvar = abs(thr[i] - G[j]) <= disp[i]
        
            evar = not(uvar or nvar)

            U.append(uvar)
            N.append(nvar)
            E.append(evar)

            # assigns to thr method undecided state
            if (evar != (not(uvar or nvar))) or nvar == True:
                collective[i].append('?')

            # assigns 1s 
            elif evar == True:
                collective[i].append(1)

            # assigns 0s 
            else:
                collective[i].append(0)

        # verifies that there is a tie or majority 
        U, N, E, tie = majority(N, U, E, thr)

        # assigns undecided to elected
        if (E != (not(U or N))) or N == True:
            
            Z_e.append("?")

        # assigns 1s to elected string
        elif E == True:

            Z_e.append(1)

        # assigns 0s to elected string
        else:

            Z_e.append(0)

        U = []
        N = []
        E = []
    
    return collective, Z_e

"""
if __name__ == "__main__":
    
    areg = [0.177247, 0.21085, 0.32051, 0.113363, 0.0185885]
    kifia = [0.19709, 0.325998, 0.155108, 0.0736089, 0.073398]
    hlx = [0.130286, 0.0785806, 0.65799, 0.693175, 0.308899]
    
    genes = [areg, kifia, hlx]
    
    thrs = [[0.113363, 0.1453050000, 0.1510890417, 0.15108904166666667], [0.155108, 0.114358, 0.225400, 0.225400], [0.3088990000, 0.4834345000, 0.4240805167, 0.4240805167]]
    
    #print((np.ceil((max(areg)-min(areg))*10) / 10))
    #print((np.ceil((max(kifia)-min(kifia))*10) / 10))
    #print((np.ceil((max(hlx)-min(hlx))*10) / 10))
    
    #print(np.ceil((max(areg)*10))/10)
    #print(np.ceil((max(kifia)*10))/10)
    #print(np.ceil((max(hlx)*10))/10)
    
    disp = [[0.0845, 0.0785, 0.0480, 0.0307], [0.0699, 0.0580, 0.0508, 0.0252], [0.1435, 0.1107, 0.0796, 0.0502]]
    
    #disp2 = [[0.0845, 0.0785, 0.0480, 0.0307], [0.0845, 0.0785, 0.0480, 0.0307], [0.1435, 0.1107, 0.0796, 0.0502]]
    
    for i in range(3):
        
        elected = election_strings(genes[i], thrs[i], disp[i])
        
        print(binVoting(genes[i], [thrs[i][0]], [disp[i][0]]))
        print('shulevich', elected[0][0])
        
        print('\n')
        
        print(binVoting(genes[i], [thrs[i][1]], [disp[i][1]]))
        print('basc', elected[0][1])
        
        print('\n')
        
        print(binVoting(genes[i], [thrs[i][2]], [disp[i][2]]))
        print('onestep', elected[0][2])
        
        print('\n')
        
        print(binVoting(genes[i], [thrs[i][3]], [disp[i][3]]))
        print('kmeans', elected[0][3])
        
        print('\n')
        
        print(binVoting(genes[i], thrs[i], disp[i]))
        print('elected', elected[1])
        print('\n')
"""

'''
if __name__ == "__main__":

    G = [{0:13618.98725, 1:12113.79308, 2:13882.42529, 3:12037.27047, 4:12924.9502, 5:11795.57956}]

    G = pd.DataFrame(G)

    G  = geneNorm(G).iloc[0].values

    #print(G)

    disp = [0.00490, 0.00366, 0.00292, 0.00188]

    thr = [0.124, 0.126, 0.129, 0.127]

    labels = ['Algo A', 'Algo B', 'Algo C', 'Algo D']
    
    #for i in range(len(thr)):

        #print(labels[i], ":", election_strings(G, [thr[i]], [disp[i]]), "mine")

        #print(labels[i], ":", binVoting(G, [thr[i]], [disp[i]]), "andrea")

    #    print("\n")

    
    #print(election_strings(G, thr, disp), "mine")

    #print(binVoting(G, thr, disp), "andrea")

    #print(binarizationVoting(G, thr, disp))

    G = [0. ,0.16966817, 0.19426017, 0.21037017, 0.20068433, 0.1847105,0.16538533,0.14316133, 0.11713267, 0.09497817] 
    t = [0.0858161158554813, 0.14958133789442618, 0.11163803490458082, 0.018275213120431785] 
    d = [0.0368999999999999, 0.0053999999999999, 0.0186, 0.1296]

    #for i in range(len(thr)):

        #print(labels[i], ":", election_strings(G, [thr[i]], [disp[i]]), "mine")

        #rint(labels[i], ":", binVoting(G, [t[i]], [d[i]]), "andrea")

        #print("\n")

    #print(binVoting(G, t, d))

    print(election_strings(G, t, d), "mine \n")

    #print(binVoting(G, t, d), "andrea \n")

    print(binarizationVoting(G, t, d))'''