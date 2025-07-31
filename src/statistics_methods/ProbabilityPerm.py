import pandas as pd
import numpy as np
import math
from bisect import bisect_right, bisect_left

#calculate prob
#vec is threshold
#d is displacement
#alg is algorithm id
def prob(vec, d, alg, probs,n):

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

    return [p0,p1,pq]

#vec is threshold
#d is displacement
#n is number of elements in gene vector
#a is algorithm to calculate prob for
#x is empty list, left default for function call
#xx is list of tuples of list and prob, left default for function call
#pp is running probability, left default for function call
def probPerm(vec, d, n, alg, x, p, xx, probs):
    #base case
    if n == 0:
        #return xx.append((x, p))
        xx['string'].append(x)
        xx['prob'].append(p)
        return
    else:
        #calculate probs
        prb = prob(vec,d,alg,probs,n)
        
        #append values
        x0 = x + '0'
        p0 = p * prb[0]
        probPerm(vec,d,n-1,alg,x0,p0,xx,probs)
        
        x1 = x + '1'
        p1 = p * prb[1]
        probPerm(vec,d,n-1,alg,x1,p1,xx,probs)
        
        xq = x + '?'
        pq = p * prb[2]
        probPerm(vec,d,n-1,alg,xq,pq,xx,probs)

    return xx

#PDF is a dataframe with the PDF of the selected algorithms
#vec is vector of gene
#alg is algorithm (string)
#d is displacement
#n is size of gene
def probBin(vec,d,n,alg,CDF):
    
    probs = CDF
    v = vec - math.floor(min(vec)*10)/10
    res = probPerm(v,d,n,alg,"",1,{'string':[], 'prob':[]},probs)
    #dct = {'string':[],'prob':[]}
    #for t in res:
    #    dct['string'].append(t[0])
    #    dct['prob'].append(t[1])
    
    df = pd.DataFrame.from_dict(res)
    return df
