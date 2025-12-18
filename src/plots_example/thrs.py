import numpy as np
import pandas as pd
from binarization.normalize import geneNorm
from threshold_methods.methods import K_Means, call_C_BASC, call_C_Stepminer
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    ecoli = pd.read_csv("../datasets/ecoli_data/SOSData/Exp4.txt", sep='\t', index_col=0).reset_index(drop=True)
    yeast = pd.read_csv("../datasets/yeast_cell/yeast_data_elu.csv", header=None, index_col=0).reset_index(drop=True)
    p53 = pd.read_csv("../datasets/P53-MDM2/other/E-MEXP-549-A-AFFY-33-normalized-expressions.tsv", sep="\t")

    p53_rep1 = p53[['H_ARP1-0h', 'H_ARP1-2h', 'H_ARP1-4h', 'H_ARP1-6h', 'H_ARP1-8h', 'H_ARP1-10h', 'H_ARP1-12h']]

    p53_norm = geneNorm(p53_rep1)
    ecoli_norm = geneNorm(ecoli)
    yeast_norm = geneNorm(yeast)

    basc = []
    onestep = []
    kmeans = []

    for index, row in ecoli_norm.iterrows():
        gene = ecoli_norm.loc[index].values[1:]
        
        kmeans.append(K_Means(gene))
        basc.append(call_C_BASC(gene.copy()))
        onestep.append(call_C_Stepminer(gene))
        
    #print(kmeans)
    #print(basc)
    #print(onestep)
        
    for index, row in yeast_norm.iterrows():
        gene = yeast_norm.loc[index].values
        
        kmeans.append(K_Means(gene))
        basc.append(call_C_BASC(gene.copy()))
        onestep.append(call_C_Stepminer(gene))
        
    for index, row in p53_norm.iterrows():
        gene = p53_norm.loc[index].values
        
        kmeans.append(K_Means(gene))
        basc.append(call_C_BASC(gene.copy()))
        onestep.append(call_C_Stepminer(gene))

    df = pd.DataFrame(columns=['K-Means', 'BASC A', 'Onestep'])

    df['K-Means'] = kmeans
    df['BASC A'] = basc
    df['Onestep'] = onestep

    df_melted = pd.melt(df, value_vars=df.columns)
    
    #print(df_melted)
    
    df_melted.to_csv("thrs.csv")

    #sns.boxplot(data=df_melted, x="variable", y="value")
    #plt.show()