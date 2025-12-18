# libraries import 
import pandas as pd
import numpy as np
import sys, os
import math
from bitarray import bitarray
from itertools import chain, combinations
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, to_hex
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


# import gene normalization function
from binarization.normalize import geneNorm
# import interpolation function
from binarization.interpolation import interpolation
# import functions that call C code of threshold algorithms
from threshold_methods.methods import call_C_BASC, call_C_kmeans, call_C_Stepminer, call_C_shmulevich, K_Means #### VERIFICAR COMMENTS

# import functions that create network (of binarizations) and elected methodology
from networks.networks import create_boolean_network, create_boolean_network_votes

# import MissForest imputation
from imputation.imputation_ml import imputate_missforest
# import function to extract displacement from displacement table
from displacements.displacementMatrixes import getDisplacement   #### VERIFICAR COMMENTS
# import function to call probabilistic C code
from statistics_methods.stringProbabilistic import run as run_stats

# import functions to run Bestfit inference
from inference_methods.BooleanModeling2post.BinInfer import run
# import functions to run Logicgep inference
from inference_methods.logicgep import LogicGep
# import functions to run MIBNI inference
from inference_methods.mibni.Mibni import Mibni

# import function to create BN from boolean functions
from networks.network_rule import createNetwork, attractors
# import function to extract path from BN based on initial state
from networks.hamming import extract_path

# import functions to calculate Metrics, and dynamic accuracy
from networks.metrics import Metrics, dynamic_accuracy

from statistics_methods.probImpute import build_kde_cdf, binarize_and_impute_matrix_with_probs_multi_methods

# read displacement table
displacements = pd.read_csv("./displacements/Displacements.csv")

thrs = pd.read_csv('./statistics_methods/thrs.csv')
    
thrsBasc = list(thrs['basca'].values)
thrsOnestep = list(thrs['onestep'].values)
thrsKmeans = list(thrs['kmeans'].values)
thrsShmulevich = list(thrs['shmulevich'].values)
    
cdfBasc = build_kde_cdf(thrsBasc)
cdfOnestep = build_kde_cdf(thrsOnestep)
cdfKmeans = build_kde_cdf(thrsKmeans)
cdfShmulevich = build_kde_cdf(thrsShmulevich)

cdf_dict = {'BASC A':cdfBasc, 'K-Means':cdfKmeans, 'Onestep': cdfOnestep, 'Shmulevich': cdfShmulevich}


def adjacency_from_binarized(X):
    """
    X: binarized matrix, shape (n_samples, n_genes)
    Returns adjacency matrix (n_genes x n_genes)
    """
    n_genes = X.shape[1]
    adj = np.zeros((n_genes, n_genes), dtype=int)

    #print(X)
    
    for target_idx in range(n_genes):
        for source_idx in range(n_genes):
            if target_idx == source_idx:
                continue
            #print("target, source:",target_idx, source_idx)
            #print("target:", X[1:, target_idx], "source:", X[:-1, source_idx])

            target_vals = X[1:, target_idx]    # t+1
            source_vals = X[:-1, source_idx]   # t
            # If source correlates with target at next step (simple Boolean dependency)
            if np.any(source_vals != target_vals):  # rough heuristic: if flipping observed
                adj[target_idx, source_idx] = 1
    return adj


# Both method are used to compare similarity between edges of diff BN. 
# jaccard counts equal edges, the larger the better the similarity
def jaccard_similarity(adj1, adj2):
    set1 = set(zip(*np.where(adj1==1)))
    set2 = set(zip(*np.where(adj2==1)))
    if len(set1 | set2) == 0:  # avoid division by zero
        return 1.0
    return len(set1 & set2) / len(set1)
    
# this hamming counts differences, the lower the better the similarity (can be done the other way around but to make it diff from jaccards)
def hamming_distance(adj1, adj2):
    return np.sum(adj1 != adj2)/adj2.size


def jaccardPlot(jaccard_df):
    
    mask = np.triu(np.ones_like(jaccard_df, dtype=bool),k=1)  # True for upper triangle
    colors = ["#56B4E9", "#66c2a5","#FC8D62", "#ededed"] #gray for diagonal so last place
    cmap = LinearSegmentedColormap.from_list("dynacc_cmap", colors)
    plt.figure(figsize=(6,5))
    sns.heatmap(jaccard_df, annot=True, fmt=".2f", cmap=cmap, cbar_kws={'label': 'Structural Similarity (Jaccard)'}, mask=mask)
    plt.title("Structural Similarity Between Binarization Methods")
    plt.tight_layout()
    plt.show()
    
def hammingPlot(hamming_df):
    
    mask = np.triu(np.ones_like(hamming_df, dtype=bool),k=1)  # True for upper triangle
    colors = ["#ededed","#56B4E9", "#66c2a5","#FC8D62"] #gray foe diagonal so first place
    cmap = LinearSegmentedColormap.from_list("dynacc_cmap", colors)
    plt.figure(figsize=(6,5))
    sns.heatmap(hamming_df, annot=True, fmt=".2f", cmap=cmap, cbar_kws={'label': 'Structural Similarity (Hamming)'}, mask=mask)
    plt.title("Structural Similarity Between Binarization Methods")
    plt.tight_layout()
    plt.show()
    
def inferenceAttractors(binarizations, power_set, data, genes_labels):
    
    attractorBF = []
    attractorMB = []
    attractorLG = []
    
    data = data.apply(pd.to_numeric)

    # make sure indexes are ints
    data.index = data.index.astype(int)
    
    for bin, p in zip(binarizations, power_set):
        
        print(bin)
        
        ########## LOGICGEP #############
        
        bin = pd.DataFrame(bin)
        bin = bin.apply(pd.to_numeric)
        bin.index = bin.index.astype(int)
        
        #dfRulesLG = LogicGep(bin, data)
        
        
        ########## MIBNI #############
         
        mibni = Mibni(10, bin, "dynamics.tsv")
        result = mibni.run()

        # save infered boolean functions in dataframe
        rules_infered = {'Gene':[],
                         'Rule':[]}
                    
        # save rules in dictionary
        for r in result:
            rul = r.split(" = ")
            rules_infered['Gene'].append(rul[0])
            rules_infered['Rule'].append(rul[1])

        # turn rules to dataframe
        dfRulesMB = pd.DataFrame(rules_infered)
        
        ########## BEST FIT #############
        
        # to save binarizations 
        data = {}
            
        # iterate binarization dataframe
        for i in bin:
                        
            # turn gene binarization values to list
            nums = list(bin[i].values)
                        
            # turn each state to a string
            nums = [str(int(i)) for i in nums]
                        
            # join binarization states as a single string 
            array_nums = "".join(nums)
                        
            # add binarization string as a bitarray to dictionary
            data[i] = bitarray(array_nums)
  
        # infer boolean functions using Bestfit
        rules = run(data, 100, 0.05)
                        
        # turn inferred rules to dataframe
        dfRulesBF = pd.DataFrame(rules)
        
        # create network based on inferred rules
        #_, netLG = createNetwork(dfRulesLG)
        _, netBF = createNetwork(dfRulesBF)
        _, netMB = createNetwork(dfRulesMB)
        
        #attractorLG.append(attractors(netLG)[0])
        attractorBF.append(attractors(netBF)[0])
        attractorMB.append(attractors(netMB)[0])
        
    #print(power_set, attractorBF)
    #print(power_set, attractorMB)
    
    return attractorLG, attractorBF, attractorMB

def attrOverlapPlot(matrix_labels, overlap_df):
    # Attractor overlap grap. It compares x number of BN created with different binarization algoritms
    # All BN should be inferred with same algorithm to reduce discrepancies due to inference and compare binariz. alg
    # Not comparing to ground truth
    # Here, attractors 
    # toy data

    binarizations2 = matrix_labels

    sim_thrsh = 0.0
    G = nx.Graph()
    for i in binarizations2:
        for j in binarizations2:
            if i != j and overlap_df.loc[i, j] > sim_thrsh:  # threshold for visibility
                G.add_edge(i, j, weight=overlap_df.loc[i, j])# Edge visual mapping (colors based on weight)

    colors = ["#56B4E9", "#66c2a5","#FC8D62"]
    cmap = LinearSegmentedColormap.from_list("dynacc_cmap", colors)
            
    # Add dynamic accuracy to df to create nodes w/size rel to dyn acc
    # Node visual mapping 
    # Uncomment when dynamic accuracy is added
    # acc_map = df.groupby("Binarization")["DynamicAccuracy"].mean().to_dict()
    # node_colors = [cmap(acc_map[b]) for b in G.nodes]
    # node_sizes = [800 * acc_map[b] for b in G.nodes]
    # print(node_sizes)

    edges = G.edges()
    weights = np.array([G[u][v]['weight'] for u, v in edges])
    cmap = cmap
    norm = plt.Normalize(vmin=min(weights), vmax=max(weights))
    edge_colors = cmap(norm(weights))
    print(weights)

    # Plot
    plt.figure(figsize=(6, 6))
    ax = plt.gca()  

    pos = nx.spring_layout(G, seed=42)
    # nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9, ax=ax)
    nx.draw_networkx_nodes(G, pos,  alpha=0.9, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=3, alpha=0.8, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
    plt.title("(D) Dynamic Similarity Between Binarization Methods")
    plt.axis("off")

    # Colorbar for edge weights
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)  
    cbar.set_label("Attractor Overlap Weight",  labelpad=15)

    plt.tight_layout()
    # Use this for all figs so we can check how they will behave when reduced/enlarged for the article
    #plt.savefig("Fig1_DynamicSimilarity.pdf", dpi=600, bbox_inches="tight")
    #plt.savefig("Fig1_DynamicSimilarity.png", dpi=600, bbox_inches="tight")
    plt.show()

# jaccards. But counts points rather than the whole string
def attractor_overlap(A, B):
    if len(A | B) == 0:
        return 1.0
    # return len(A & B) / len(A | B)
    return sum(A==B)/len(A)

if __name__ == "__main__":
    
    df = pd.DataFrame({
    0: [0.25,0.20,0.92,0.88],
    1: [0.22,0.10,0.12,0.08],
    2: [0.78,0.15,0.09,0.11],
    3: [0.81,0.77,0.22,0.79],
    4: [0.12,0.05,0.18,0.14]
    })
    
    df = df.T
    
    #df = geneNorm(df)
    
    genes_labels = ['A', 'B', 'C', 'D', 'E']

    
    thr_methods = ['BASC A', 'K-Means', 'Onestep']
    
    power_set = list(chain.from_iterable(combinations(thr_methods, r) for r in range(len(thr_methods) + 1)))
    
    power_set = [p for p in power_set if len(p) > 0]
    
    #print(df)
    
    thrs_dict = {'BASC A':{}, 'K-Means':{}, 'Onestep':{}}
    
    disps = {'BASC A':{}, 'K-Means':{}, 'Onestep':{}}
    
    for i, g in enumerate(genes_labels):
        
        gene_val = df.iloc[i].values
        
        thrs_dict['BASC A'][i] = call_C_BASC(gene_val.copy())
        thrs_dict['K-Means'][i] = K_Means(gene_val)
        thrs_dict['Onestep'][i] = call_C_Stepminer(gene_val)
        
        disps['BASC A'][i] = getDisplacement(['BASC A'], gene_val).loc[0].values[0]
        disps['K-Means'][i] = getDisplacement(['K-Means'], gene_val).loc[0].values[0]
        disps['Onestep'][i] = getDisplacement(['Onestep'], gene_val).loc[0].values[0]
    
    #print(thrs_dict, disps)
    
    binarizations = []
    
    for p in power_set:
        
        p_label = "{" + ", ".join(p) + "}"
        
        timeImpu = pd.DataFrame(columns=genes_labels)
        
        for idx, label in enumerate(genes_labels):
            
            g = list(df.loc[idx])
    
            t = []
            cdfList = []
            d = []
                
            for m in p:
                    
                cdfList.append(cdf_dict[m])
                    
                t.append(thrs_dict[m][idx])
                d.append(disps[m][i])
            
            timeImpu[label] = list(binarize_and_impute_matrix_with_probs_multi_methods([g], cdfList, t, d, 0.5, 3)[0])
            
        timeImpu = timeImpu.fillna(-1)
        timeImpu = timeImpu.astype(int) 
        timeImpu = timeImpu.replace(-1, '?')
        imputedDF = pd.DataFrame(imputate_missforest(timeImpu.copy())).astype(int)
        
        #print(p_label)
        #print(imputedDF)
        imputedDF.columns = genes_labels
        binarizations.append(imputedDF)
        
    adjacency_matrices = [adjacency_from_binarized(bin.values) for bin in binarizations]
    
    n_matrices = len(adjacency_matrices)
    jaccard_mat = np.zeros((n_matrices, n_matrices))
    hamming_mat = np.zeros((n_matrices, n_matrices))

    for i in range(n_matrices):
        for j in range(n_matrices):
            jaccard_mat[i,j] = jaccard_similarity(adjacency_matrices[i], adjacency_matrices[j])
            hamming_mat[i,j] = hamming_distance(adjacency_matrices[i], adjacency_matrices[j])

    # Convert to DataFrame for readability
    matrix_names = ["{" + ", ".join(p) + "}" for p in power_set] #kmeans, basc, os, etc
    jaccard_df = pd.DataFrame(jaccard_mat, index=matrix_names, columns=matrix_names)
    hamming_df = pd.DataFrame(hamming_mat, index=matrix_names, columns=matrix_names)

    jaccardPlot(jaccard_df)
    hammingPlot(hamming_df)
    
    #print(binarizations)
     
    attractorLG, attractorBF, attractorMB = inferenceAttractors(binarizations, matrix_names, df, genes_labels)

    print(attractorBF, attractorMB)
    
    for i, attr in enumerate(attractorBF):
        for a in attr:
            el = [int(e) for e in a]
        
        eshaped_chars = np.array(el).reshape(-1, len(el))
        df_attr = pd.DataFrame(eshaped_chars, columns=genes_labels)

        last_state = (df_attr.iloc[-1, :])
        
        attractorBF[i] = last_state

    n_matrices = len(binarizations)
    overlap_mat = np.zeros((n_matrices, n_matrices))

    for i in range(n_matrices):
        for j in range(n_matrices):
            overlap_mat[i,j] = attractor_overlap(attractorBF[i], attractorBF[j])

    overlap_df = pd.DataFrame(overlap_mat, index=matrix_names, columns=matrix_names)
    
    attrOverlapPlot(matrix_names, overlap_df)
        
            
 
            