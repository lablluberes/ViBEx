##############################################
#
# This file contains functions and code for threshold computation methods 
#
##############################################
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import math
import ctypes
from binarization.normalize import geneNorm
from scipy.stats import f

################################
## K-MEANS

###############################


## Kmeans main function
def K_Means(genes):
    """
        K_Means - uses Kmeans to compute thr

        genes: gene expression
    """

    # reshape data
    data = np.array(genes).reshape(-1, 1)

    # kmeans object two clusters
    kmeans = KMeans(n_clusters=2, n_init=10)
    # fit data
    kmeans.fit(data)
    # extract assigment
    c=kmeans.labels_
    # turn gene to array
    genes = np.array(genes)
    # get expression from first cluster
    groupOne = genes[c==1]
    # get expression from second cluster
    groupZero = genes[c==0]
    
    # get mean
    thr1 = np.mean(groupOne)
    thr2 = np.mean(groupZero)
    
    # get mean of two clusters 
    thr = (thr1 + thr2) / 2

    return thr


def call_C_kmeans(data):
    """
        call_C_kmeans - function calls C code of Kmeans implementation using Openmp

        data: gene expression
    """

    # Load the shared library of kmeans
    kmeans_lib = ctypes.CDLL('./threshold_methods/kmeans.so')

    # Define the argument and return types for the functions
    kmeans_lib.KMeans.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    kmeans_lib.KMeans.restype = ctypes.c_double

    # Define your data
    data = np.asarray(data, dtype=np.float64)

    # compute thr using c code 
    t = kmeans_lib.KMeans(data, len(data))

    return t


################################
## BASC A code in Python and C

###############################


############
## BASC A Code
############

# Mean from a to b
def Y_a_b(genes, a, b):
    """
        Y_a_b - computes mean from a to b

        genes: gene expression
        a - starting point
        b - end point 
    """
    #print("Mean ", np.mean(genes[a:b]), " from a ",a , " to b ", b)
    return np.mean(genes[a:b])

# Cost of jump from a to b
def C_a_b(genes, a, b):
    """
        C_a_b - computes cost from a to b

        genes: gene expression
        a: starting index
        b: end index
    """
    mean = Y_a_b(genes, a, b+1)
    return sum( (np.array(genes[a:b+1]) - mean) ** 2 )

# determine height of the jump
def determine_h(P, i, j, genes):
    """
        determine_h - determines height of jump

        P: matrix indexes
        i: rows
        j: cols
        genes: gene expression
    """
    N = len(genes)

    if (i == 0 and j > 0):
        return Y_a_b(genes, P[i][j], P[i+1][j]) - Y_a_b(genes, 0, P[i][j])
    elif (i == j and j > 0):
        return Y_a_b(genes, P[i][j], N) - Y_a_b(genes, P[i-1][j], P[i][j])
    elif (i == 0 and j == 0):
        return Y_a_b(genes, P[i][j], N) - Y_a_b(genes, 0, P[i][j])
    else:
        return Y_a_b(genes, P[i][j], P[i+1][j]) - Y_a_b(genes, P[i-1][j], P[i][j])

# BASC A main function 
def BASC_A(gene):
    """
        BASC_A - computes thr using BASC A

        gene: gene expression
    """

    # sort gene 
    gene_og = gene
    gene = np.sort(gene)
    N = len(gene)

    cost_matrix = [[0 for _ in range(N - 1)] for _ in range(N)]
    ind_matrix = [[0 for _ in range(N - 2)] for _ in range(N - 1)]
    P = [[0 for _ in range(N - 2)] for _ in range(N - 2)]

    # Step 1: Compute a Series of Step Function

    # initialization C_i_(0) = c_i_N
    # calculate first cost matrix column with no intermidiate break points
    for i in range(N):
        cost_matrix[i][0] = C_a_b(gene, i, N)

    # Algorithm 1: Calculate optimal step functions
    for j in range(N-2):
        for i in range(N-j-1):
            min_value = math.inf
            min_index = math.inf

            for d in range(N-j-1):
                if(i <= d):
                    curr_value = C_a_b(gene, i, d) + cost_matrix[d+1][j]

                if(curr_value < min_value):
                    min_value = curr_value
                    min_index = d

            cost_matrix[i][j+1] = min_value
            ind_matrix[i][j] = min_index + 1

    #  Algorithm 2: Compute the break points of all optimal step functions
    for j in range(N-2):
        z = j
        P[0][j] = ind_matrix[0][z]
        if(j > 0):
            z = z - 1
            for i in range(1, j+1):
                P[i][j] = ind_matrix[P[i-1][j]][z]
                z = z - 1

    # Step 2: Find Strongest Discontinuity in Each Step Function
    v = [0] * (N-2)

    for j in range(N-2):
        max_value = -math.inf
        max_index = j
        for i in range(j+1):
            h = determine_h(P, i, j, gene)
            z = (gene[P[i][j]] + gene[P[i][j]-1]) / 2
            e = sum( (np.array(gene) - z) ** 2 )
            q_score = h / e
            if(q_score > max_value):
                max_value = q_score
                max_index = i

        v[j] = P[max_index][j]

    # Step 3: Estimate Location and Variation of the Strongest Discontinuities
    thr = (gene[round(np.median(v))-1] + gene[round(np.median(v))]) / 2

    return thr


# This code makes python call the OpenMP code of BASC A in C

def call_C_BASC(data):
    """
        call_C_BASC - calls C code of BASC using Openmp

        data: gene expression
    """

    # Load the shared library
    basca_lib = ctypes.CDLL('./threshold_methods/basca.so')

    # Define the argument and return types for the functions
    basca_lib.Y_a_b.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_int]
    basca_lib.Y_a_b.restype = ctypes.c_double

    basca_lib.C_a_b.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_int]
    basca_lib.C_a_b.restype = ctypes.c_double

    basca_lib.quicksort.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_int]
    basca_lib.quicksort.restype = None

    basca_lib.Find_median.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    basca_lib.Find_median.restype = ctypes.c_double

    basca_lib.BASCA.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    basca_lib.BASCA.restype = ctypes.c_double

    # Define your data
    data = np.asarray(data, dtype=np.float64)

    # Call the BASCA function
    t = basca_lib.BASCA(data, len(data))

    return t


##############
## Stepminer code (only onestep) in Python and C
#############

# Main function for Stepminer (onestep) based on Sahoo: https://sites.google.com/view/debashis-sahoo/softwares

def mse(data, start, end):
    """
        mse - calculates mean square error

        data: gene expression
        start: start index
        end: end index
    """

    result = 0

    # get mean
    m = np.mean(data[start:end+1])

    # calculate mean square error
    for i in range(start, end+1):
        result += (data[i] - m) * (data[i] - m)

    return result
    

def find_mean(data, start, end):
    """
        find_mean - finds mean

        data: gene expr
        start: start index
        end: end index
    """

    # return 0 if start index is greater
    if (start > end):
        return 0

    # return 0 if indexes are the same
    if start == end: 
        return 0

    # return mean
    return np.mean(data[start:end+1])

def onestep(data):
    """
        onestep - onestep threshold computation 

        data: gene expression
    """

    # size of gene
    n = len(data)

    # initialize sse array to 0
    sseArray = np.zeros(n)

    # sum of datapoints
    suma = sum(data)

    # mean of expression
    mean = np.mean(data)

    # calculate sstot
    sstot = mse(data, 0, len(data)-1)
    
    # more variables
    sum1 = 0
    count1 = 0
    m1 = 0
    sum2 = suma
    count2 = n
    m2 = (suma/n)
    sum1sq = 0
    sum2sq = sstot
    sse = sum1sq + sum2sq

    # iterate gene expression
    for i in range(len(data)):
        entry = data[i]

        count1 += 1
        count2 -= 1

        if count2 == 0:
            sseArray[i] = sstot
            continue
        tmp = (mean - (entry + sum1)/count1)
        sum1sq = sum1sq + (entry - mean) * (entry - mean) - tmp * tmp * count1 + (count1 - 1) * (mean - m1) * (mean - m1)
        tmp = (mean - (sum2 - entry)/count2)
        sum2sq = sum2sq - (entry - mean) * (entry - mean) - tmp * tmp * count2 + (count2 + 1) * (mean - m2) * (mean - m2)
        sum1 += entry
        sum2 -= entry
        m1 = sum1/count1
        m2 = sum2/count2
        sse = sum1sq + sum2sq
        sseArray[i] = sse

    
    # to find the best sse (minimum)
    bestSse = sseArray[0]
    bestIndex = 0

    # find sse that is smaller 
    for i in range(len(data)):
        index = i

        if sseArray[i] < bestSse:
            bestSse = sseArray[i]
            bestIndex = index

    
    # get means based on sse minimum index
    m1 = find_mean(data, 0, bestIndex)
    m2 = find_mean(data, bestIndex + 1, len(data))

    # compute thr 
    thr = (m1+m2)/2

    return thr



# This code makes python call the OpenMP code of Stepminer in C
def call_C_Stepminer(data):
    """
        call_C_Stepminer - calls C code of stepminer

        data: gene expression
    """
    
    # Load the shared library
    stepminer_lib = ctypes.CDLL('./threshold_methods/stepminer.so')  # Update with the correct path to the compiled library

    # Define argument and return types for the functions
    stepminer_lib.calcSSTOT.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_double]
    stepminer_lib.calcSSTOT.restype = ctypes.c_double

    stepminer_lib.mean.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_int]
    stepminer_lib.mean.restype = ctypes.c_double

    stepminer_lib.stepminer.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    stepminer_lib.stepminer.restype = ctypes.c_double

    # Define your data
    data = np.asarray(data, dtype=np.float64)

    gene = data.copy()

    # sort gene
    gene.sort()
    
    return stepminer_lib.stepminer(gene, len(gene))


# This code makes python call the Onestep in C
def call_C_Onestep(data):
    """
        call_C_Onestep - calls C code of onestep

        data: gene expression
    """
    
    # Load the shared library
    Onestep_lib = ctypes.CDLL('./threshold_methods/onestep.so')  # Update with the correct path to the compiled library

    # Define argument and return types for the functions
    Onestep_lib.mse.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_double]
    Onestep_lib.mse.restype = ctypes.c_double

    Onestep_lib.find_mean.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_int]
    Onestep_lib.find_mean.restype = ctypes.c_double
    
    Onestep_lib.sum.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    Onestep_lib.sum.restype = ctypes.c_double

    Onestep_lib.stepminer.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    Onestep_lib.stepminer.restype = ctypes.c_double

    # Define your data
    data = np.asarray(data, dtype=np.float64)

    gene = data.copy()

    # sort gene
    gene.sort()
    
    return Onestep_lib.stepminer(gene, len(gene))

#################
## Shumelich Code
#################

## Main function for Shmulevich
def shmulevich(G):
    """
        shmulevich - computes threshold using shmulevich method

        G: gene expression
    """

    # sort gene
    S = np.sort(G)

    # length of gene
    k = len(S)
    D = []

    # calculate D
    for j in range(k-1):
        D.append(S[j+1] - S[j])
    
    t = (S[k-1]-S[0]) / (k-1)
    
    m = []
    for j in range(len(D)):
        if D[j] > t:
            m.append(j)
    
    m = min(m)

    return S[m+1]


# This code makes python call the OpenMP code of BASC A in C

def call_C_shmulevich(data):
    """
        call_C_shmulevich - calls C code of shmulevich

        data: gene expression
    """

    # Load the shared library
    shmulevich_lib = ctypes.CDLL('./threshold_methods/shmulevich.so')

    # Define the argument and return types for the functions
    shmulevich_lib.min.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    shmulevich_lib.min.restype = ctypes.c_int

    shmulevich_lib.shmulevich.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    shmulevich_lib.shmulevich.restype = ctypes.c_double

    # Define your data
    data = np.asarray(data, dtype=np.float64)

    gene = data.copy()

    # sort gene
    gene.sort()

    #print(gene)

    # call c code
    t = shmulevich_lib.shmulevich(gene, len(data))

    return t


def binaryreturn(thr, data):
    """
        binaryreturn - binarizes gene expression

        thr - list of threshold
        data - list of gene expr
    """
    binary = []

    # iterate gene expr
    for i in range(len(data)):
        s = thr[i]
        b = []
        g = data[i]

        # binarize 
        for e in g:
            if e > s:
                b.append(1)
            else:
                b.append(0)
        
        # append binarization
        binary.append(b)

    return binary


def thr_and_binary(data, method):
    """
        thr_and_binary - computes thrs and binarizations

        data: gene exprs
        method: selected methods
    """
    thr_arr = []

    # iterage genes 
    for d in data:
        # compute thrs
        if method == 'basc':
            thr_arr.append(BASC_A(np.array(d)))
        elif method == 'kmeans':
            thr_arr.append(K_Means(np.array(d)))
        elif method == 'onestep':
            thr_arr.append(onestep(np.array(d)))
        else:
            thr_arr.append(shmulevich(np.array(d)))
    
    # get binarizations 
    binary = binaryreturn(thr_arr, data)

    return thr_arr, binary

"""if __name__ == '__main__':

    '''data = {'lexA':[0,738.5883333,1726.663333,2161.133333,1921.125,1619.07,1190.89,849.2483333,655.355,494.62,439.2416667,368.7466667,382.2266667,337.565,257.7633333,292.9166667,287.015,227.6633333,216.045,238.9266667,210.1783333,183.9533333,165.0283333,182.38,188.3966667,182.615,169.57,163.6133333,164.42,141.8766667,89.80833333,101.6083333,133.7833333,123.6283333,125.5916667,169.635,164.885,159.155,131.76,117.5366667,112.975,103.38,102.4816667,91.635,71.67,68.645,94.6,89.63666667,88.53666667,121.2633333],
    'uvrD':[0,242.8116667,341.765,268.555,144.0233333,103.525,83.96333333,92.25166667,96.46833333,117.2366667,118.905,91.12666667,88.77,90.12333333,116.5716667,109.3816667,98.50166667,73.28166667,50.03666667,45.985,40.07333333,58.32666667,58.50666667,46.93666667,31.90666667,22.41666667,19.25666667,13.20333333,17.96166667,28.90166667,50.495,44.505,70.2,86.82,78.06333333,69.30666667,67.20166667,41.18666667,26.82833333,23.735,20.33833333,18.385,22.30833333,20.58166667,25.29666667,38.22,50.435,65.70333333,66.76333333,65.20833333],
    'recA':[0,1696.681667,1942.601667,2103.701667,2006.843333,1847.105,1653.853333,1431.613333,1171.326667,949.7816667,793.28,688.285,634.6983333,566.6983333,494.675,472.4083333,464.7233333,394.5216667,383.9116667,432.2333333,395.7133333,373.94,371.1266667,386.2716667,367.355,320.6033333,310.9766667,313.8333333,253.6516667,248.74,263.0316667,261.735,232.7783333,228.0216667,259.8566667,282.47,269.2133333,244.2366667,169.6133333,131.7,103.1366667,57.17166667,85.11666667,137.2083333,175.0866667,172.6233333,194.7683333,196.7383333,169.2433333,140.6466667],
    'uvrA':[0,1252.276667,1407.586667,1456.77,1409.568333,1260.02,1043.75,841.59,571.8833333,352.265,244.055,231.9516667,206.785,207.63,227.3216667,229.7683333,210.7533333,185.435,165.2483333,153.7933333,143.5933333,143.9816667,134.0816667,107.805,81.03,86.47833333,85.68333333,95.20333333,105.0616667,99.65333333,78.34166667,67.54333333,77.24166667,69.655,62.51666667,70.92166667,74.12166667,61.16166667,56.93833333,67.68833333,79.195,85.94166667,87.62,94.49666667,89.79333333,77.405,77.615,84.17166667,80.62833333,67.99],
    'polB':[0,43.59833333,53.46833333,57.52166667,71.92333333,60.95666667,56.86166667,35.03833333,19.44166667,19.72666667,28.03166667,34.80333333,40.76333333,51.62833333,31.74666667,20.59666667,28.23333333,29.58666667,23.58166667,35.15,40.93333333,36.06166667,45.14833333,47.04833333,50.55166667,47.62333333,48.43333333,43.76333333,37.295,29.25166667,26.50333333,25.75666667,26.72833333,35.58333333,30.035,28.83666667,25.315,27.44,20.24833333,21.02333333,20.54333333,5.63,1.328333333,0.308333333,1.743333333,0,5.205,4.098333333,2.885,0],
    'umuD':[0,0,0,70.48333333,142.0983333,151.3683333,157.99,178.5266667,156.8716667,156.1766667,142.3916667,122.7116667,86.77666667,70.50833333,47.23,30.78166667,48.43333333,57.375,34.17166667,36.34,29.68666667,15.01333333,19.79666667,32.57666667,52.92833333,57.57333333,66.395,60.95166667,39.37,34.28,29.41833333,27.76,31.875,38.45166667,38.07333333,40.925,39.91333333,34.09833333,25.42,15.16833333,7.128333333,8.178333333,21.05833333,16.67,17.51833333,23.065,18.46166667,18.1,21.25666667,23.46]}
     '''

    areg = [1772.47, 2108.5, 3205.1, 1133.63, 185.885]

    df = pd.DataFrame({'0':[134], '1':[75], '2':[75], 
                       '3':[91], '4':[100], '5':[52], '6':[79], '7':[112], 
                       '8':[102], '9':[125], '10':[103], '11':[109], '12':[103],
                         '13':[60], '14':[94], '15':[63], '16':[91]})
    
    data = [[273, 214, 190, 208, 353, 210, 337, 324, 271, 391, 250, 244, 306, 265, 304, 253, 231],
        [2020, 1284, 2191, 1651, 2696, 1069, 2084, 1779, 1261, 5887, 2676, 2411, 1523, 2277, 2915, 2426, 2863],
        [134, 75, 75, 91, 100, 52, 79, 112, 102, 125, 103, 109, 103, 60, 94, 63, 91],
        [112, 155, 142, 150, 137, 135, 150, 159, 153, 147, 131, 111, 153, 117, 139, 160, 113]]

    #df = pd.DataFrame(data)

    df.columns = [f"Col{i+1}" for i in range(df.shape[1])]

    data  = geneNorm(df).values

    print(onestep(data[0]))

    #cdc = df

    #areg  = geneNorm(cdc).iloc[0].values

    #print(areg)

    #thr_s = shmulevich(areg)
    #thr_b = BASC_A(areg)
    #thr_o = onestep(areg)
    #thr_k = K_Means(areg)

    #print(f"\nshmulevich: {thr_s}, basc: {thr_b}, onestep: {thr_o}, kmeans: {thr_k}\n")



"""