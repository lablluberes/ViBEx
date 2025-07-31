import pandas as pd
import numpy as np
import math
from bisect import bisect_right, bisect_left
import time 
from itertools import product

#calculate prob
#vec is threshold
#d is displacement
#alg is algorithm id
def prob_a(vec, d, alg, probs,n, binary_string):
    
    if binary_string == '1':
        
        t = (vec[-n]-d)
        idx = bisect_right(probs['val'], t)
        if idx < 1: idx = 0
        if idx > 99: idx = 99
        p1 = probs[alg].iloc[idx]
        
        return p1

    elif binary_string == '0':
        
        t = (vec[-n]+d)
        idx = bisect_left(probs['val'], t)
        if idx > 99: idx = 99
        if idx < 1: idx = 0
        p0 = 1 - probs[alg].iloc[idx]
        
        return p0
        
    else:
        
        t = (vec[-n]-d)
        idx = bisect_right(probs['val'], t)
        if idx < 1: idx = 0
        if idx > 99: idx = 99
        p1 = probs[alg].iloc[idx]

        t = (vec[-n]+d)
        idx = bisect_left(probs['val'], t)
        if idx > 99: idx = 99
        if idx < 1: idx = 0
        p0 = 1 - probs[alg].iloc[idx]
        pq = 1 - (p1 + p0)
        
        return pq

def probability_strings(gene, d, n, alg, probs):
    '''
        probability_strings: returns a dictionary with all possible strings and their probabilities

        gene: gene expression
        d: displacement
        n: size of gene
        alg: binarization method
        probs: probability dataframe
    '''
    
    # generates all posible strings 
    lexicograph = ['0', '1', '?']
    
    z_k = [''.join(p) for p in list(product(lexicograph, repeat=n))]
    
    # to save probabilities of strings
    prob_z = {}
    
    # iterate all possible strings
    for z in z_k:
        
        # probability of current string
        curr_prob = 1
        
        # iterate string 
        for i in range(n):
            
            # once it reached 0 exit loop
            if n-i == 0:
                break

            # gets probability of current state (either 0, 1, or ?)
            prb = prob_a(gene, d, alg, probs, n-i, z[i])
            
            # accumulate prob
            curr_prob *= prb
        
        # saves prob 
        prob_z[z] = curr_prob
    
    # return probs 
    return prob_z

#PDF is a dataframe with the PDF of the selected algorithms
#vec is vector of gene
#alg is algorithm (string)
#d is displacement
#n is size of gene
def probBin(vec,d,n,alg,CDF):
    
    probs = CDF
    v = vec - math.floor(min(vec)*10)/10
  
    res = probability_strings(v, d, n, alg, probs)
    
    #print(res)
    
    dct = {'string':[],'prob':[]}
    for t in res:
        dct['string'].append(t)
        dct['prob'].append(res[t])
        #print(t)
    
    df = pd.DataFrame.from_dict(dct)
    return df

'''
if __name__ == "__main__":

    standard_dev = pd.read_csv("standard_dev.csv")
    gene = np.array([0.104088,  0.0456529, 0.0899751, 0.182464,  0.0397391])
    thr_k = {'0': 0.11303083005859375}
    selected_gene = 0
    d = 0.0032
    sizeGene = len(gene)

    rangeIndex = math.ceil((max(gene)-min(gene))*10) - 1
    probden = pd.read_csv("cdf_"+str(rangeIndex+1)+".csv")

    res = probBin(gene,d,sizeGene,'k-means',probden)

    print(res)
'''