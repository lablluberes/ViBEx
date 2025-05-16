import numpy as np
import pandas as pd
import math
import ctypes
from scipy.stats import f
from itertools import product
from methods import K_Means, onestep, shmulevich, BASC_A

def probabilistic(G, S, disp):
    
    N = len(G)
    
    store_prob = {}

    for x in S:
        
        random_genes = [np.random.uniform(0, 1, 10) for _ in range(1000)]
        
        #print(random_genes)
        
        if x == 'K-Means':
            T = np.array([K_Means(g) for g in random_genes])
        elif x == 'Shmulevich':
            T = np.array([shmulevich(g) for g in random_genes])
        elif x == 'BASC A':
            T = np.array([BASC_A(g) for g in random_genes])
        else:
            T = np.array([onestep(g) for g in random_genes])
            
        store_prob[x] = [[], [], []]
        
        #print(T)

        for j in range(len(G)):
            
            P_0 = np.mean(T > G[j] + disp)
            P_1 = np.mean(T < G[j] - disp)
            P_undecided = 1 - (P_0 + P_1)
            
            store_prob[x][0].append(P_0)
            store_prob[x][1].append(P_1)
            store_prob[x][2].append(P_undecided)
    
    omega =  [np.array(store_prob[x]) for x in S]
    omega_avg = np.mean(omega, axis=0)

    
    #print(omega_avg)
    
    lexicograph = ['0', '1', '?']
    
    z_k = [''.join(p) for p in list(product(lexicograph, repeat=N))]
    
    Z = {}
    #P = {}
    
    for k in range(3**N):
        
        #print(z_k[k])
        
        perm_string = z_k[k]
        
        P_k = 1
        
        for j in range(N):
            
            lex = perm_string[j]
            
            if lex == '0':
                
                P_k *= omega_avg[0][j]
                
            elif lex == '1':
                
                P_k *= omega_avg[1][j]
            
            else: 
                
                P_k *= omega_avg[2][j]
            
        
        Z[perm_string] = P_k
        
    
    #counts, bin_edges = np.histogram(Z.values, bins=h, range=(0,1))
    
    return Z


# string_high_P = max(Z, key=Z.get)
# high_P = Z[string_high_P]