import numpy as np
import pandas as pd
import scipy
from methods import K_Means, BASC_A, onestep, shmulevich

methods = [K_Means, onestep, BASC_A, shmulevich]
vals = np.arange(1,11)
vals = vals/10
for v in vals:
    m = np.random.rand(1000,10)
    m *= v
    thresholds = [[],[],[],[]]
    cols = ['k-means','onestep','BASC_A','shmulevich']

    for i in range(1000):
    
        x = m[i]
        for a in range(len(methods)):
    
            thr = methods[a](x)
            thresholds[a].append(thr)
            
            
    prob = []

    #create PDF
    for i in range(len(cols)):
        col = thresholds[i]
        r = scipy.stats.rv_histogram(np.histogram(col, bins=100))
        probs = r.cdf(np.linspace(0.01,v,100))
        prob.append(probs) 

    pdf_df = pd.DataFrame(prob).transpose()
    pdf_df.columns = cols
    pdf_df['val'] = np.linspace(0.01,v,100)
    
    
    pdf_df.to_csv('cdf_'+ str(int(v * 10)) + ".csv",index=False)  
    