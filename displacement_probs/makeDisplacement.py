import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy import interpolate

from methods import call_C_BASC, call_C_Stepminer, call_C_shmulevich, shmulevich

def interpolation(vect, iter=4):
    """
        interpolation - function to interpolate only n (iter) number of times

        vect: gene expression
        iter: number of iterations
    """

    # get indices from 0 n-1
    indices = np.arange(len(vect))

    # size of the first interpolation
    newSize = len(vect) + (len(vect) - 1)

    # gene expr
    gene = vect

    # for loop to interpolate iter times
    for i in range(iter):
        
        # cubic spline
        bspl = interpolate.CubicSpline(indices, gene)

        # indices of spline gene
        indices = np.linspace(0, len(vect)-1, newSize)

        # interpolate gene expression with a new size
        interpolated_values = bspl(indices)

        # save new gene spline
        gene = interpolated_values

        # get gene size for new interpolation
        newSize = len(gene) + (len(gene) - 1)

    #print(len(gene))
    # return spline gene
    gene[gene < 0] = 0
    gene[gene > 1] = 1
    return gene

def K_means(gene):
    """
        K_means - K-means algorithm 

        gene: gene expression
    """
    
    # reshape gene    
    gene = np.array(gene).reshape(-1, 1)
      
    # run kmeans algorithm  
    kmeans = KMeans(n_clusters=2, random_state=42, n_init="auto").fit(gene)

    # return thr
    return sum(kmeans.cluster_centers_)[0]/2


def generateDisplacement():
    """
        generateDisplacement - generates displacement table
    """
   
    
    # create range intervals from 0.1 to 1
    intervals = np.arange(0.1, 1.1, 0.1)

    # dataframe for displacement
    df = pd.DataFrame(columns=['range', 'shmulevich', 'basca', 'onestep', 'kmeans'])

    # save intervals
    df['range'] = intervals

    # the displacement values for each method
    kmeans_estimated_disp = []
    onestep_estimated_disp = []
    basc_estimated_disp = []
    shmulevich_estimated_disp = []

    # iterate across all ranges 
    for interval in intervals:
      
            #randomVectors = np.random.uniform(0, interval, size=(100,10))
        
        # read random data 
        randomVectors = np.loadtxt(f'./datasets/RD{int(interval*10)}.csv', delimiter=',')
        
            #print(interval, int(np.ceil((max(randomVectors[0])-min(randomVectors[0]))*10)-1))

        # to save the displacements 
        kmeans_disp = []
        onestep_disp = []
        basc_disp = []
        shmulevich_disp = []

        # iterate each random vector
        for vector in randomVectors:
            
                #print(interval, int(np.ceil((max(vector)-min(vector)) * 10) - 1), max(vector))

            # get threshold of original vector
            kmeans_thrs = [K_means(vector)]
            onestep_thrs = [call_C_Stepminer(vector)]
            basc_thrs = [call_C_BASC(vector.copy())]
            shmulevich_thrs = [call_C_shmulevich(vector)]
            
            # interpolate gene 4 times
            for i in range(1,5):
                
                # interpolates gene i times
                interpolatedVector = interpolation(vector, i)
                #print(len(interpolatedVector))
                
                # get threshold of interpolation
                kmeans_thrs.append(K_means(interpolatedVector))
                onestep_thrs.append(call_C_Stepminer(interpolatedVector))
                basc_thrs.append(call_C_BASC(interpolatedVector.copy()))
                shmulevich_thrs.append(call_C_shmulevich(interpolatedVector))
            
            # calculate displacements for each method max - min
            kmeans_disp.append(max(kmeans_thrs) - min(kmeans_thrs))
            onestep_disp.append(max(onestep_thrs) - min(onestep_thrs))
            basc_disp.append(max(basc_thrs) - min(basc_thrs))
            shmulevich_disp.append(max(shmulevich_thrs) - min(shmulevich_thrs))

        # create lists with displacements and estimated displacement
        list_disp = [kmeans_disp, onestep_disp, basc_disp, shmulevich_disp]
        list_estimated_disp = [kmeans_estimated_disp, onestep_estimated_disp, basc_estimated_disp, shmulevich_estimated_disp]

        # iterate each displacement list and save estimated disp
        for displacements, estimated_list in zip(list_disp, list_estimated_disp):

            # histogram from 0 to interval (0.1, 0.2, ..., 1). passes the displacement to histogram with bins the size of interval/0.01 (0.1/0.01=10, 0.2/0.01=20)
            count, bins = np.histogram(displacements, range = [0, interval], bins=int(interval/0.01), density=True)

            #print(count, bins[1:])
            
            # calculate the estimated displacement
            desp = sum((count/100) * bins[1:])
            
            # save displacement
            estimated_list.append(desp)

        #break

    # save estimated displacement to each method
    df['kmeans'] = kmeans_estimated_disp
    df['basca'] = basc_estimated_disp
    df['shmulevich'] = shmulevich_estimated_disp
    df['onestep'] = onestep_estimated_disp
   
    # return dataframe
    return df


if __name__ == "__main__":

    # calls generate displacement
    disp = generateDisplacement()

    # print displacement table
    print(disp)
