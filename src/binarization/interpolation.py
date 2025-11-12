##############################################
#
# This file contains function that interpolates gene 
#
##############################################
import numpy as np
from scipy import interpolate

def interpolation(vect, iter=4):
    """
        interpolation - function to interpolate only n (iter) number of times

        vect: gene expression
        iter: number of iterations
    """
    
    # get x from 0 n-1
    indices = np.arange(len(vect))

    #cubic spline 
    #bspl = interpolate.CubicSpline(x, vect)

    # size of the first interpolation
    newSize = len(vect) + (len(vect) - 1)

    # gene expr
    gene = vect

    # for loop to interpolate iter times
    for i in range(iter):

        bspl = interpolate.CubicSpline(indices, gene)

        # indices of spline gene
        indices = np.linspace(0, len(vect)-1, newSize)

        # interpolate gene expression with a new size
        interpolated_values = bspl(indices)

        # save new gene spline
        gene = interpolated_values

        # get gene size for new interpolation
        newSize = len(gene) + (len(gene) - 1)

    # return spline gene  
    gene[gene < 0] = 0
    gene[gene > 1] = 1
    return gene

'''if __name__ == "__main__":

    arr = [16.966817, 19.426017, 21.037017]
 
    a = interpolation(arr)

    print(a)'''