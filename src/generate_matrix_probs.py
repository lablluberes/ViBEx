import numpy as np
import pandas as pd
import scipy

######################################
#                                    #
# Generate matrix,thresholds & probs #
#                                    #
######################################


from methods import K_Means, BASC_A, onestep, shmulevich

#algos -> list of algorithms
#n -> size of gene
def PDF(algos, rangeIndex):

    #generate random matrix
    m = np.random.rand(1000,n)
    #list of algorithms
    methods = []
    #list of lists of thresholds
    thresholds = []
    #list of col names
    cols = []
    for a in algos:
        if a == "K-Means":
            methods.append(K_Means)
            thresholds.append([])
            cols.append('k-means')
        if a == "Onestep":
            methods.append(onestep)
            thresholds.append([])
            cols.append('onestep')
        if a == "BASC A":
            methods.append(BASC_A)
            thresholds.append([])
            cols.append('BASC_A')
        if a == "Shmulevich":
            methods.append(shmulevich)
            thresholds.append([])
            cols.append('shmulevich')

    #Generate thresholds and store
    for i in range(1000):
    
        x = m[i]
        for a in range(len(methods)):
    
            thr = methods[a](x)
            thresholds[a].append(thr)

    #dataframe with probabilities
    prob = []

    #create PDF
    for i in range(len(cols)):
        col = thresholds[i]
        r = scipy.stats.rv_histogram(np.histogram(col, bins=100))
        probs = r.cdf(np.linspace(0.1,1,100))
        prob.append(probs) 

    pdf_df = pd.DataFrame(prob).transpose()
    pdf_df.columns = cols
    return pdf_df
    