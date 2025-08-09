import numpy as np
import pandas as pd
import math
import ctypes
from scipy.stats import f
from itertools import product
from threshold_methods.methods import K_Means, onestep, shmulevich, BASC_A
from ctypes import CDLL, c_int, byref, c_char, c_double, c_char_p

def call_C_statistics(gene, d, alg, binary):

    #print("me llaman")

    # to compile use gcc -O3 -fPIC -shared -o statistics.so statistics.c

    my_lib = CDLL('./statistics_methods/statistics.so') 

    my_lib.get_string.argtypes = []
    my_lib.get_string.restype = c_char_p

    my_lib.get_p.argtypes = []
    my_lib.get_p.restype = c_double

    my_lib.get_high_p.argtypes = []
    my_lib.get_high_p.restype = c_double

    my_lib.run.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), c_double, c_int, c_char_p, c_char_p]
    my_lib.run.restype = None

    my_lib.probBin.argtypes = [c_double, c_double, c_int, c_double, c_double, c_double, c_char]
    my_lib.probBin.restype = None

    my_lib.probPerm.argtypes = [c_double, c_double, c_int, c_int, c_char, c_double, c_double, c_double, c_char]
    my_lib.probPerm.restype = None

    my_lib.prob.argtypes = [c_double, c_double, c_double, c_double, c_int, c_int, c_double]
    my_lib.prob.restype = None

    my_lib.bisect_left.argtypes = [c_double, c_double]
    my_lib.bisect_left.restype = c_int

    my_lib.bisect_right.argtypes = [c_double, c_double]
    my_lib.bisect_right.restype = c_int

    my_lib.readFile.argtypes = [c_double, c_double, c_int, c_int]
    my_lib.readFile.restype = None

    sizeGene = len(gene)

    #print("aqui", binary, alg, d, gene)

    #print(gene, d, sizeGene, alg, binary)

    gene2 = gene.copy()

    my_lib.run(gene2, d, sizeGene, alg.encode('utf-8'), binary.encode('utf-8'))

    #print("despues de run")

    high_p = my_lib.get_high_p()
    high_string = my_lib.get_string()
    p = my_lib.get_p()

    #print((high_p, high_string), p)

    prob_dict = {'label':[alg],'string':[binary],'prob':[p],'mean':[],'sd':[],'res':[],'highest':[high_string.decode('utf-8')],'highestprob':[high_p]}

    #print(prob_dict, d)

    return high_p, high_string.decode('utf-8'), p


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

"""
if __name__ == "__init__":

    S = ['K-Means']
    disp = 0.005399999999999999
    G = [0., 0.07385883, 0.17266633, 0.21611333, 0.1921125,  0.161907, 0.119089, 0.08492483, 0.0655355,  0.049462]

    probabilistic(G, S, disp)"""