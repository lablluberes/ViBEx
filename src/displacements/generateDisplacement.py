##############################################
#
# This file contains function that generates displacement ranges 
#
##############################################
import numpy as np
import pandas as pd
from binarization.interpolation import interpolation
from threshold_methods.methods import call_C_BASC, BASC_A, call_C_Stepminer, onestep, K_Means, shmulevich, call_C_kmeans, call_C_shmulevich

def generateDisplacement(methods, genes):
    """
        generateDisplacement -  generates displacement table based on thr methods and genes

        methods: selected thr methods
        genes: selected genes 
    """
    
    # to save ranges of table
    index = []
    
    # iterate selected genes and get range 
    for g in genes:
        
        # max expression
        g_max = max(g)
        
        # append range 
        index.append(np.ceil(g_max * 10) / 10)
    
    # create dataframe with selected methods as columns, and ranges as indexes
    df = pd.DataFrame(columns=methods, index = index)
    
    # iterate over selected genes 
    for g in genes:
        
        # max expression
        g_max = max(g)

        # get range 
        r = np.ceil(g_max * 10) / 10
        
        # if displacement value is not in table then compute it 
        if df[methods[0]][r] is np.nan:
            
            # thresholds lists per method 
            kmeans_thr = []
            basc_thr = []
            onestep_thr = []
            shmul_thr = []
            
            # displacement lists per method 
            kmeans_disp = []
            basc_disp = []
            onestep_disp = []
            shmul_disp = []
            
            # create 100 random vectors of 10 time points
            for i in range(100):
                
                # random profile of 10 time points from range 0 to r 
                random_profile = np.random.uniform(0, r, 10)
                
                # interpolate profile four times 
                for i in range(4):
                    
                    # get spline of profile
                    g_spline = interpolation(random_profile, i+1)
                    
                    #print("len", len(g_spline))
                    
                    # based on selected methods get the thr of spline profile 
                    for m in methods:
                        
                        if m == 'K-Means':
                            kmeans_thr.append(call_C_kmeans(g_spline))
                        elif m == 'BASC A':
                            basc_thr.append(call_C_BASC(g_spline))
                        elif m == 'Onestep':
                            onestep_thr.append(call_C_Stepminer(g_spline))
                        else:
                            shmul_thr.append(call_C_shmulevich(g_spline))
                
                # iterate selected methods and calculate disps
                for m in methods:
                    
                    if m == 'K-Means':
                            kmeans_disp.append(max(kmeans_thr) - min(kmeans_thr))
                    elif m == 'BASC A':
                            basc_disp.append(max(basc_thr) - min(basc_thr))
                    elif m == 'Onestep':
                            onestep_disp.append(max(onestep_thr) - min(onestep_thr))
                    else:
                            shmul_disp.append(max(shmul_thr) - min(shmul_thr))
            
            # for each selected method divide disps into histogram in bins from 0 to 1
            for m in methods:
                    
                    if m == 'K-Means':
                            # get bins 
                            count, bins = np.histogram(kmeans_disp, range=[0, 1])

                            # get displacement
                            desp = sum((count/100) * bins[:-1])

                            # save displacement in table
                            df.loc[r, m] = desp
                            
                    elif m == 'BASC A':
                            # get bins 
                            count, bins = np.histogram(basc_disp, range=[0, 1])

                            # get displacement
                            desp = sum((count/100) * bins[:-1])

                            # save displacement in table
                            df.loc[r, m] = desp
                            
                    elif m == 'Onestep':
                            # get bins 
                            count, bins = np.histogram(onestep_disp, range=[0, 1])

                            # get displacement
                            desp = sum((count/100) * bins[:-1])

                            # save displacement in table
                            df.loc[r, m] = desp
                            
                    else:
                            # get bins 
                            count, bins = np.histogram(shmul_disp, range=[0, 1])

                            # get displacement
                            desp = sum((count/100) * bins[:-1])

                            # save displacement in table
                            df.loc[r, m] = desp
                            
                
    # return displacements     
    return df