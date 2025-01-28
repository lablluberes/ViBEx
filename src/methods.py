from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import math
import ctypes

############
## KMeans Code
############

## Kmeans main function
def K_Means(genes):
    data = np.array(genes).reshape(-1, 1)
    kmeans = KMeans(n_clusters=2, n_init=10)
    kmeans.fit(data)
    c=kmeans.labels_
    genes = np.array(genes)
    groupOne = genes[c==1]
    groupZero = genes[c==0]
    
    thr1 = np.mean(groupOne)
    thr2 = np.mean(groupZero)
    
    thr = (thr1 + thr2) / 2

    return thr


################################
## BASC A code in Python and C

###############################


############
## BASC A Code
############

# Mean from a to b
def Y_a_b(genes, a, b):
    #print("Mean ", np.mean(genes[a:b]), " from a ",a , " to b ", b)
    return np.mean(genes[a:b])

# Cost of jump from a to b
def C_a_b(genes, a, b):
    mean = Y_a_b(genes, a, b+1)
    return sum( (np.array(genes[a:b+1]) - mean) ** 2 )

# determine height of the jump
def determine_h(P, i, j, genes):
    N = len(genes)

    if (i == 0 and j > 0):
        return Y_a_b(genes, P[i][j], P[i+1][j]) - Y_a_b(genes, 0, P[i][j]);
    elif (i == j and j > 0):
        return Y_a_b(genes, P[i][j], N) - Y_a_b(genes, P[i-1][j], P[i][j]);
    elif (i == 0 and j == 0):
        return Y_a_b(genes, P[i][j], N) - Y_a_b(genes, 0, P[i][j]);
    else:
        return Y_a_b(genes, P[i][j], P[i+1][j]) - Y_a_b(genes, P[i-1][j], P[i][j]);

# BASC A main function 
def BASC_A(gene):
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

    # Load the shared library
    basca_lib = ctypes.CDLL('./basca.so')

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

# Main function of Stepminer (onestep)
def onestep(x):
    
    n = len(x)
    #step = 0
    xmean = np.mean(x)
    SSTOT = getSSTOT(x, n, xmean)
    
    SSEmin = SSTOT
    
    for i in range(n-1):
        leftMean = np.mean(x[0:i+1])
    
        rightMean = np.mean(x[i+1:n])
        
        SSE = 0
        
        for j in range(n):
            if j < i+1:
                SSE = SSE + (x[j] - leftMean)**2
            else:
                SSE = SSE + (x[j] - rightMean)**2
                    
        
        if SSEmin > SSE:
            SSEmin = SSE
            #print("1:",SSEmin1)
                
            t = (leftMean + rightMean)/2
        
    
    return t

#function returns the SSTOT
def getSSTOT(x, n, xmean):
    m = 0
    for i in range(n):
        m = m + (x[i] - xmean)**2
    return m


# This code makes python call the OpenMP code of Stepminer in C
def call_C_Stepminer(data):
    
    # Load the shared library
    stepminer_lib = ctypes.CDLL('./stepminer.so')  # Update with the correct path to the compiled library

    # Define argument and return types for the functions
    stepminer_lib.calcSSTOT.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_double]
    stepminer_lib.calcSSTOT.restype = ctypes.c_double

    stepminer_lib.mean.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int, ctypes.c_int]
    stepminer_lib.mean.restype = ctypes.c_double

    stepminer_lib.stepminer.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64), ctypes.c_int]
    stepminer_lib.stepminer.restype = ctypes.c_double

    data = np.asarray(data, dtype=np.float64)
    return stepminer_lib.stepminer(data, len(data))

#################
## Shumelich Code
#################

## Main function for Shmulevich
def shmulevich(x):
    
    n = len(x)
    s = np.sort(x)
    d = np.empty(n)
    
    for i in range(n-2):
        d[i] = s[i+1] - s[i]
    
    t = (s[n-1] - s[0])/(n-1)
    
    mn = s[n-1]
    index = 0
    
    for i in range(n-1):
        if d[i] > t and d[i] < mn:
            mn = d[i]
            index = i
            
    z = s[index + 1]
   
    
    return z