import numpy as np
import pandas as pd
import math
import ctypes
from scipy.stats import f
from itertools import product
from threshold_methods.methods import K_Means, shmulevich, BASC_A
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


import numpy as np
import pandas as pd
import math
from bisect import bisect_right, bisect_left



def probability(gene, d, n, alg, my_string, CDF):

    probs = CDF
    v = gene - math.floor(min(gene)*10)/10


    my_prob = 1
    high_prob = 1
    high_string = ""

    for i in range(n, 0, -1): 
        #print(i)
        #prob(gene, d, probs_alg, probs_val, i, sizeGene, p0_list, p1_list, pq_list, sizeGene-i);

        t = (v[-i]-d)
        idx = bisect_right(probs['val'], t)
        if idx < 1: idx = 0
        if idx > 99: idx = 99
        p1 = probs[alg].iloc[idx]
        t = (v[-i]+d)
        idx = bisect_left(probs['val'], t)
        if idx > 99: idx = 99
        if idx < 1: idx = 0
        p0 = 1 - probs[alg].iloc[idx]
        pq = 1 - (p1 + p0)

        prb = [p0, p1, pq]

        #print(f"inter {n-i}, prob0: {p0}, prob1: {p1}, prob?: {pq}")

        if my_string[n-i] == '0':
            my_prob *= p0
        elif my_string[n-i] == '1':
            my_prob *= p1
        else:
            my_prob *= pq

        #print(my_string[n-i])

        maxProb = max(prb)

        index = prb.index(maxProb)

        if index == 0:
            high_prob *= prb[0]
            high_string += '0'
        elif index == 1:
            high_prob *= prb[1]
            high_string += '1'
        else:
            high_prob *= prb[2]
            high_string += '?'

    #print(f"high string: {high_string}, prob: {high_prob}, my prob: {my_prob}")
        
    return high_string, high_prob, my_prob

def run(gene, d, size, alg, my_string):

    rangeIndex = math.ceil((max(gene)-min(gene))*10) - 1

    probden = pd.read_csv("./statistics_methods/cdf_"+str(rangeIndex+1)+".csv")

    high_string, high_prob, my_prob = probability(gene, d, size, alg, my_string, probden)

    return high_prob, high_string, my_prob

"""
if __name__ == "__main__":

    gene10 = [0.104088,  0.0456529, 0.0899751, 0.182464,  0.0397391, 0.0932, 0.0851, 0.1019, 0.0894, 0.0970]

    gene17 = np.array([0.104088  , 0.0456529 , 0.0899751 , 0.182464  , 0.0397391 ,   0.182464  , 0.07210751, 0.0397391 , 0.13845988, 0.13340002,   0.14899839, 0.09482894, 0.08228803, 0.0397391 , 0.04502217, 0.104088  , 0.0456529])
    
    gene50 = [0.104088  , 0.0456529 , 0.0899751 , 0.182464  , 0.0397391 ,   0.182464  , 0.07210751, 0.0397391 , 0.13845988, 0.13340002,   0.14899839, 0.09482894, 0.08228803, 0.0397391 , 0.04502217,   0.182464  , 0.11878976, 0.04595516, 0.11877186, 0.14492543,   0.12920543, 0.10077983, 0.12206538, 0.05716041, 0.11400026,   0.10608877, 0.12505076, 0.1153136 , 0.06699311, 0.182464  ,   0.0397391 , 0.04965236, 0.06459848, 0.05807794, 0.07369502,   0.11049246, 0.09580436, 0.0397391 , 0.08706011, 0.12915618,   0.09906689, 0.0397391 , 0.08134486, 0.13013362, 0.182464  ,   0.05471957, 0.10810489, 0.0664399 , 0.0397391 , 0.14370657]

    alg = "k-means"
    d = 0.0032

    run(np.array(gene10), d, len(gene10), alg, "10?1000100")

    run(gene17, d, len(gene17), alg, "10110100111000110")

    run(np.array(gene50), d, len(gene50), alg, "1001?100111000011011111011110100000100010001101001")"""

"""
if __name__ == "__init__":

    S = ['K-Means']
    disp = 0.005399999999999999
    G = [0., 0.07385883, 0.17266633, 0.21611333, 0.1921125,  0.161907, 0.119089, 0.08492483, 0.0655355,  0.049462]

    probabilistic(G, S, disp)"""