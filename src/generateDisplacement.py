import numpy as np
import pandas as pd
from interpolation import interpolation
from methods import call_C_BASC, BASC_A, call_C_Stepminer, onestep, K_Means, shmulevich

def generateDisplacement(methods, genes):
    
    index = []
    
    for g in genes:
        
        g_max = max(g)
        
        index.append(np.ceil(g_max * 10) / 10)
    
    df = pd.DataFrame(columns=methods, index = index)
    
    for g in genes:
        
        g_max = max(g)
    
        r = np.ceil(g_max * 10) / 10
        
        if df[methods[0]][r] is np.nan:
            
            kmeans_thr = []
            basc_thr = []
            onestep_thr = []
            shmul_thr = []
            
            kmeans_disp = []
            basc_disp = []
            onestep_disp = []
            shmul_disp = []
            
            for i in range(100):

                random_profile = np.random.uniform(0, r, 10)
                
                for i in range(4):
                    
                    g_spline = interpolation(random_profile, i+1)
                    
                    #print("len", len(g_spline))
                    
                    for m in methods:
                        
                        if m == 'K-Means':
                            kmeans_thr.append(K_Means(g_spline))
                        elif m == 'BASC A':
                            basc_thr.append(call_C_BASC(g_spline))
                        elif m == 'Onestep':
                            onestep_thr.append(call_C_Stepminer(g_spline))
                        else:
                            shmul_thr.append(shmulevich(g_spline))
                
                for m in methods:
                    
                    if m == 'K-Means':
                            kmeans_disp.append(max(kmeans_thr) - min(kmeans_thr))
                    elif m == 'BASC A':
                            basc_disp.append(max(basc_thr) - min(basc_thr))
                    elif m == 'Onestep':
                            onestep_disp.append(max(onestep_thr) - min(onestep_thr))
                    else:
                            shmul_disp.append(max(shmul_thr) - min(shmul_thr))
            
            for m in methods:
                    
                    if m == 'K-Means':
                            count, bins = np.histogram(kmeans_disp, range=[0, 1])
                            desp = sum((count/100) * bins[:-1])

                            df.loc[r, m] = desp
                            
                    elif m == 'BASC A':
                            count, bins = np.histogram(basc_disp, range=[0, 1])
                            desp = sum((count/100) * bins[:-1])

                            df.loc[r, m] = desp
                            
                    elif m == 'Onestep':
                            count, bins = np.histogram(onestep_disp, range=[0, 1])
                            desp = sum((count/100) * bins[:-1])

                            df.loc[r, m] = desp
                            
                    else:
                            count, bins = np.histogram(shmul_disp, range=[0, 1])
                            desp = sum((count/100) * bins[:-1])

                            df.loc[r, m] = desp
                            
                
              
    return df