#################################
## This is the code for normalizing the data

## Change name variable to the filename to normalize
#################################

import numpy as np
import pandas as pd
import csv
import math

# Normalize function takes the name of the file and normalizes it
# based on formula x' = (x - min) / (max - min)
def normalize(name):

    # read file
    df = pd.read_csv(name, header=None)

    # iterate each row
    for i in range(len(df)):
            
            # get values of row
            vect = df.iloc[i].values

            # normalize vect based on formula
            norm = (vect - min(vect))/ (max(vect)-min(vect))

            # round and save it 
            df.iloc[i] = norm.round(decimals=4)

    # create dataframe
    df = pd.DataFrame(df)

    # save to new file 
    df.to_csv('norm.csv', index=False, header=False)

# geneNorm function takes the name of the file to normalize
# it then moves the decimal point based on the maximum value of each row
# checks if it is a 10^n
def geneNorm(G):

    #G = pd.read_csv(name, header=None)

    arr = np.shape(G)

    #print(arr[1])

    G_norm = np.zeros([arr[0],arr[1]])

    for i in range(arr[0]):

        m = max(G.iloc[i].values)

        if m == 1:

            G_norm[i] = G.iloc[i].values

        else:

            expo = math.log10(m)

            if expo % 1 == 0:

                maxV = m

            else:

                n = len(str(math.ceil(m)))

                maxV = 10 ** n

                
            G_norm[i] = np.array(G.iloc[i].values) / maxV
        

    
    #print(G_norm)
            
    G = pd.DataFrame(G_norm)

    return G
    #G.to_csv('norm.csv', index=False, header=False)

                

    
# change to read another file 
#name = "HIV.csv"


#normalize(name)

#geneNorm(name)

