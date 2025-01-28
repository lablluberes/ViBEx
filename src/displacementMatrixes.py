#####################################
#                                   #
# Generate matrix and displacements #
#                                   #
#####################################

import numpy as np
#import scipy
#from methods import K_Means, BASC_A, onestep, shmulevich

import pandas as pd

#Pass gene and calculate displacement
#Pass list of algorithms to get disp of
def getDisplacement(algos, gene):

    mxx = max(gene)
    mnn = min(gene)
    Range = int(np.ceil((mxx-mnn) * 10) - 1)
    disps = pd.read_csv("Displacements.csv")
    
    
    
    #n = len(gene)
    #matrixes = np.random.rand(100,n)
    #matrixes = (matrixes*Range)+mnn
    
    #list of algorithms
    #methods = []
    #list of lists of thresholds
    displacements = []
    #list of col names
    cols = []
    for a in algos:
        if a == "K-Means":
            #methods.append(K_Means)
            displacements.append(disps['k-means'].iloc[Range])
            cols.append('k-means')
        if a == "Onestep":
            #methods.append(onestep)
            displacements.append(disps['onestep'].iloc[Range])
            cols.append('onestep')
        if a == "BASC A":
            #methods.append(BASC_A)
            displacements.append(disps['BASC_A'].iloc[Range])
            cols.append('BASC_A')
        if a == "Shmulevich":
            #methods.append(shmulevich)
            displacements.append(disps['shmulevich'].iloc[Range])
            cols.append('shmulevich')

    # #get displacements of each over 100 vectors
    # for i in range(100):
        # #select vector
        # v = matrixes[i]
        # xx = np.arange(n)
        # #obtain spline
        # sp = scipy.interpolate.CubicSpline(xx,v)
        # #create min and max trackers
        # for a in range(len(methods)):
            # mn = 1
            # mx = 0
            # nn = xx
            # #4 interpolations
            # for k in range(4):
                # yy = sp(nn)
                # thr = methods[a](yy)
                # #update maxmin
                # if thr > mx:
                    # mx = thr
                # if thr < mn:
                    # mn = thr
                # #update x's, nn
                # nn = np.linspace(0, n-1, len(nn)*2 - 1)
            # displacements[a].append(mx-mn)

    # #do histogram to get average displacement
    # #bins = 10
    # binS = np.linspace(mnn,mxx,11)
    # finalE = []
    # for a in range(len(methods)):
        # hist = np.histogram(displacements[a],bins=binS)
        # E = sum(binS[0:10] * (hist[0]/100))
        # finalE.append(E)

    df = pd.DataFrame(displacements).transpose()
    df.columns = cols
    return df
        
