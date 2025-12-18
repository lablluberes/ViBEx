import numpy as np
import pandas as pd
from methods import K_Means, BASC_A, shmulevich, call_C_BASC, call_C_Stepminer, call_C_shmulevich
from scipy.stats import norm, rv_histogram
import matplotlib.pyplot as plt

def pdf():
    
    # create range intervals from 0.1 to 1
    intervals = np.arange(0.1, 1.1, 0.1)

    # dataframe
    df = pd.DataFrame(columns=['val', 'shmulevich', 'basca', 'onestep', 'kmeans'])
    
    # iterate across all ranges 
    for interval in intervals:
        
        # create random vectors 
        randomVectors = np.random.uniform(0, interval, size=(1000, 10))
        
        # save thrs
        thr_b = []
        thr_o = []
        thr_s = []
        thr_k = []
        
        # iterate vectors and compute thrs 
        for vector in randomVectors:
            
            thr_b.append(call_C_BASC(vector.copy()))
            thr_k.append(K_Means(vector))
            thr_o.append(call_C_Stepminer(vector))
            thr_s.append(call_C_shmulevich(vector))
        
        
        r = rv_histogram(np.histogram(thr_b, bins=100))
        probs = r.pdf(np.linspace(0.01, interval, 100))
        
        plt.plot(np.arange(100), probs)
        
        plt.show()
        
        #print("aqui")
        print(probs)
        
        break


def saveThrs():

    df = pd.DataFrame(columns=['shmulevich', 'basca', 'onestep', 'kmeans'])
        
    # create random vectors 
    np.random.seed(42) 

    randomVectors = np.random.uniform(0, 1, size=(1000, 10))
        
    # save thrs
    thr_b = []
    thr_o = []
    thr_s = []
    thr_k = []
        
    # iterate vectors and compute thrs 
    for vector in randomVectors:
            
        thr_b.append(call_C_BASC(vector.copy()))
        thr_k.append(K_Means(vector))
        thr_o.append(call_C_Stepminer(vector))
        thr_s.append(call_C_shmulevich(vector))
        
        
    df['shmulevich'] = thr_s
    df['basca'] = thr_b
    df['onestep'] = thr_o
    df['kmeans'] = thr_k

    df.to_csv('thrs.csv', index=False)


if __name__ == "__main__":
    
    #pdf()
    saveThrs()