# import gene normalization function
from binarization.normalize import geneNorm
# import interpolation function
from binarization.interpolation import interpolation
# import functions that call C code of threshold algorithms
from threshold_methods.methods import call_C_BASC, call_C_kmeans, call_C_Stepminer, call_C_shmulevich, K_Means

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    sns.set_theme(style="whitegrid", palette="pastel")
    sns.set_style("whitegrid")
    plt.rcParams['axes.grid.axis'] = 'x'

    base_colors = ["#56B4E9", "#66c2a5","#FC8D62", "#ededed",]
    
    p53 = [6.495043069,6.954698878,7.189797494,7.007641718,6.728389309,6.448082276,6.246030288]
    lexA = [1572.176667,2219.958333,2647.42,2407.458333,2032.263333,1750.646667,1388.028333,1170.693333,963.02,759.8283333,656.4083333,570.5116667,516.91,512.96,503.9016667,446.9216667,446.9033333,462.6583333,402.425,324.93,335.3,322.13,268.08,311.27,331.8033333,288.8933333,236.8033333,270.8716667,278.8866667,310.0533333,318.135,312.555,265.755,181.0033333,171.2733333,178.4683333,176.6633333,203.1583333,204.5333333,218.35,209.5016667,185.9666667,191.0316667,218.12,192.1,168.4233333,167.4766667,148.3916667,132.2366667]
    example = [0.332, 0.5453, 0.6554, 0.5044, 0.59544, 0.3443]
    
    
    p53 = pd.DataFrame([p53])
    lexA = pd.DataFrame([lexA])
    example = pd.DataFrame([example])
    
    p53 = geneNorm(p53)
    lexA = geneNorm(lexA)
    example = geneNorm(example)
    
    p53 = p53.iloc[0].values
    lexA = lexA.iloc[0].values
    example = example.iloc[0].values
   
    #p53Interp =interpolation(p53)
    #lexAInterp = interpolation(lexA)
    
    p53Thrs = {'BASC A':call_C_BASC(p53.copy()), 'Onestep': call_C_Stepminer(p53.copy()), 'K-Means': K_Means(p53.copy())}
    lexAThrs = {'BASC A':call_C_BASC(lexA.copy()), 'Onestep': call_C_Stepminer(lexA.copy()), 'K-Means': K_Means(lexA.copy())}
    exampleThrs = {'BASC A':call_C_BASC(example.copy()), 'Onestep': call_C_Stepminer(example.copy()), 'K-Means': K_Means(example.copy())}
    
    #print(p53Thrs)
    dfp53 = pd.DataFrame({'Time Series':range(1,len(p53)+1),
                       'Gene Expression':p53})
    
    #print(df)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.lineplot(data=dfp53, x='Time Series', y='Gene Expression', color='black', marker='o')
    plt.axhline(y=p53Thrs['BASC A'], color=base_colors[0], linestyle='--', label='BASC A')
    plt.axhline(y=p53Thrs['K-Means'], color=base_colors[1], linestyle='-.', label='K-Means')
    plt.axhline(y=p53Thrs['Onestep'], color=base_colors[2], linestyle=':', label='Onestep')
    sns.despine(left=True)
    plt.legend(title='Threshold Computation Method')
    plt.title('Gene Expression of p53')
    plt.savefig("p53.png")
    plt.show()
    
    
    dflexA = pd.DataFrame({'Time Series':range(1,len(lexA)+1),
                       'Gene Expression':lexA})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.lineplot(data=dflexA, x='Time Series', y='Gene Expression', color='black', marker='o')
    plt.axhline(y=lexAThrs['BASC A'], color=base_colors[0], linestyle='--', label='BASC A')
    plt.axhline(y=lexAThrs['K-Means'], color=base_colors[1], linestyle='-.', label='K-Means')
    plt.axhline(y=lexAThrs['Onestep'], color=base_colors[2], linestyle=':', label='Onestep')
    sns.despine(left=True)
    plt.legend(title='Threshold Computation Method')
    plt.title('Gene Expression of lexA')
    plt.savefig("lexA.png")
    plt.show()
    
    
    dfexample = pd.DataFrame({'Time Series':range(1,len(example)+1),
                       'Gene Expression':example})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.lineplot(data=dfexample, x='Time Series', y='Gene Expression', color='black', marker='o')
    plt.axhline(y=exampleThrs['BASC A'], color=base_colors[0], linestyle='--', label='BASC A')
    #plt.axhline(y=exampleThrs['K-Means'], color=base_colors[1], linestyle='-.', label='K-Means')
    #plt.axhline(y=exampleThrs['Onestep'], color=base_colors[2], linestyle=':', label='Onestep')
    sns.despine(left=True)
    plt.legend(title='Threshold Computation Method')
    plt.title('Gene Expression with TCMs')
    plt.savefig("example.png")
    plt.show()
    
    