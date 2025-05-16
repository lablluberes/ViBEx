################################
## Interpolation code.
## Function - three_interpolation does the interpolation N times

###############################

import numpy as np
from scipy import interpolate
from methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep


# function to interpolate only n (iter) number of times
# argumenrs: vect - gene expression, method - method to use, iter - number of iterations
'''def three_interpolation(vect, method, iter=4):

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
    
    return thr, gene'''

# function to interpolate only n (iter) number of times
# argumenrs: vect - gene expression, iter - number of iterations
def interpolation(vect, iter=4):
    
    x = np.arange(len(vect))

    #edit s later if necessary
    bspl = interpolate.CubicSpline(x, vect)

    # size of the first interpolation
    newSize = len(vect) + (len(vect) - 1)

    #print(newSize)

    gene = vect

    # for loop to interpolate iter times and save thresholds 
    for i in range(iter):

        # indices of gene
        indices = np.linspace(0, len(vect)-1, newSize)

        #print(len(indices))

        # interpolate gene expression with a new size
        
        #pick samples from 
        interpolated_values = bspl(indices)
        
        #print(indices, "\n")
        
        gene = interpolated_values
        

        # update variables
        newSize = len(gene) + (len(gene) - 1)
        
    return gene

'''if __name__ == "__main__":

    arr = [16.966817, 19.426017, 21.037017]
 
    a = interpolation(arr)

    print(a)'''