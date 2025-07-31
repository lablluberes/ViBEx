#################################
## 
## File contains code for gene normalization 
## 
#################################

import numpy as np
import pandas as pd
import csv
import math

# geneNorm function takes the name of the file to normalize
# it then moves the decimal point based on the maximum value of each row
# checks if it is a 10^n
def geneNorm(G):
    """
        geneNorm - normalized gene expression matrix

        G: gene expression matrix
    """


    # shape of matrix
    arr = np.shape(G)

    #print(arr[1])

    # create matrix to store normalized genes
    G_norm = np.zeros([arr[0],arr[1]])
    
    # iterate matrix
    for i in range(arr[0]):
        
        # max value of curr gene expr
        m = max(G.iloc[i].values)

        # if its 1 then leave gene expr as it is
        if m == 1:

            G_norm[i] = G.iloc[i].values

        # moves the decimal point based on the maximum value of each row
        else:
            
            # log10 of highest expr 
            expo = math.log10(m)
            
            if expo % 1 == 0:

                maxV = m
            
            else:

                n = len(str(math.ceil(m)))

                maxV = 10 ** n

            # divide gene expr 
            G_norm[i] = np.array(G.iloc[i].values) / maxV
        

    
    # returns dataframe     
    G = pd.DataFrame(G_norm)

    return G


