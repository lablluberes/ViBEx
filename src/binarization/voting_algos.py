################################
## Code to generate the voting table 
## Function - election_strings, voting mechanism based on Lluberes thesis (made by Michael)
###############################

import math
import numpy as np
#from binarization.normalize import geneNorm
import pandas as pd
#threshold/displacement indexes are vectors with values in them
#for different algorithms


###### Added function for elected string alg

def election_strings(gene, thr_list, disp_list):
    """
        election_strings - makes election strings and binarizes genes

        gene: gene expression
        thr_list: list of threshold values
        disp_list: list of displacement of gene
    """

    z_e = []

    for j in range(len(gene)):

      store = []

      for i in range(len(thr_list)):

        U = (gene[j]+disp_list[i] < thr_list[i]) and (abs(thr_list[i] - gene[j]) > disp_list[i])
        N = abs(thr_list[i] - gene[j]) <= disp_list[i]
        E = not(U or N)

        store.append(np.array([N, U, E]))

      store = np.array(store)

      # verify ties for N, U, E
      count1N = list(store[:,0]).count(1)
      count0N = list(store[:,0]).count(0)
      count1U = list(store[:,1]).count(1)
      count0U = list(store[:,1]).count(0)
      count1E = list(store[:,2]).count(1)
      count0E = list(store[:,2]).count(0)


      # get majority for N, U, E
      majN = max(set(store[:,0]), key=list(store[:,0]).count)
      majU = max(set(store[:,1]), key=list(store[:,1]).count)
      majE = max(set(store[:,2]), key=list(store[:,2]).count)

      if majE != (not(majU or majN)) or majN == 1 or (count0N == count1N) or (count1E == count0E) or (count0U == count1U):
        z_e.append(np.nan)
      elif majE == 1:
        z_e.append(1)
      else:
        z_e.append(0)

    return z_e

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