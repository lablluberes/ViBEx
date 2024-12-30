################################
## Interpolation code.
## Function - interpolationConverge does the interpolation until convergence
## Function - three_interpolation does the interpolation N times

###############################

import numpy as np
from scipy import interpolate
from methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep

# function to interpolate until convergence
# CURRENTLY NOT USED IN THE DASHBOARD 
# arguments: 
#         vect - gene expression
#         method - method to binarize
#         tolerance - tolerance level, by default its 0.1
def interpolationConverge(vect, method, tolerance=0.001):

    thr = []
    converge = False

    # size of gene
    n = (len(vect) - 1)

    # size of the first interpolation
    newSize = len(vect) + (len(vect) - 1)
    
    
    x = np.arange(len(vect))
    bspl = interpolate.CubicSpline(x, vect)
    
    
    gene = vect
    sample = []
    # limit of iteration
    limit = 5000
    conver = 0
    
    # limit of iteration if its basc a
    if method == 'BASC A':
        limit = 500
    
    # while no convergence or not reach limit size keep looking for convergence
    while(~converge and newSize < limit):


        # indices of the gene
        indices = np.linspace(0, len(vect) - 1, len(gene) + n)

        # interpolate gene using linspace
        interpolated_values = bspl(indices)
        
        #print(interpolated_values, "\n")
        
        # new values of gene expression
        gene = interpolated_values
        
        # get threshold based on method
        if(method == 'K-Means'):
            
            thr.append(K_Means(gene))
            
        elif(method == 'BASC A'):
            
            # if the new size of the interpolation is greater than 100 use the OpenMP code to get threshold
            if(newSize > 100):
                t = call_C_BASC(gene)
                print("Size: ", newSize, "Thr HPC: ", t)

            # threshold with python code  
            else:
                t = BASC_A(gene)
                print("Size: ", newSize, "Thr reg: ", t)
            thr.append(t)
            
        elif(method == 'Onestep'):
            
            # if the new size of the interpolation is greater than 100 use the OpenMP code to get threshold
            if(newSize > 100):
                t = call_C_Stepminer(gene)
                print("Size: ", newSize, "Thr HPC: ", t)

            # threshold with python code 
            else:
                t = onestep(gene)
                print("Size: ", newSize, "Thr reg: ", t)
            thr.append(t)
            
        else:
            
            thr.append(shmulevich(gene))
    
        #print(interpolated_values)
        
        n_thr = len(thr)
        
        # verifiy if the convergence has been reached by looking for the difference to be like the tolerance
        for i in range(n_thr):
            for j in range(n_thr):
                if(i != j):
                    difference = abs(thr[i] - thr[j])
                    
                    # difference is less or equal than tolerance then converge happens
                    if(difference <= tolerance):
                        converge = True
                        conver = thr[j]
                        break

        # no convergence then keep looking
        # update values   
        if(~converge):
            n = len(gene) - 1
            
            #newSize = newSize + (newSize-1)
            #vect = interpolated_values
        

    # get min, max thresholds 
    tMin = min(thr)
    tMax = max(thr)
    
    return thr, gene

# function to interpolate only n (iter) number of times
# argumenrs: vect - gene expression, method - method to use, iter - number of iterations
def three_interpolation(vect, method, iter=4):

    thr = []

    # size of gene
    n = (len(vect) - 1)
    
    x = np.arange(len(vect))
    #edit s later if necessary
    bspl = interpolate.CubicSpline(x, vect)

    # size of the first interpolation
    newSize = len(vect) + (len(vect) - 1)

    gene = vect
    sample = []

    # for loop to interpolate iter times and save thresholds 
    for i in range(iter):

        # sample size
        #sample.append(newSize)

        # indices of gene
        indices = np.linspace(0, len(vect) - 1, len(gene) + n)

        # interpolate gene expression with a new size
        
        #pick samples from 
        interpolated_values = bspl(indices)
        
        #print(indices, "\n")
        
        gene = interpolated_values
        
        # get the threshold based on the method
        #if(method == 'K-Means'):
        #    thr.append(K_Means(gene))
        #elif(method == 'BASC A'):
        #    t = BASC_A(gene)
        #    thr.append(t)
        #elif(method == 'Onestep'):
        #    thr.append(onestep(gene))
        #else:
        #    thr.append(shmulevich(gene))
        
        # update variables
        n = len(gene) - 1
        #n = newSize - 1

        # new size of the next interpolation
        #newSize = newSize + (newSize-1)
    
    return thr, gene

