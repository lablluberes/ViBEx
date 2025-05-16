import numpy as np
import pandas as pd
import sklearn.metrics as metrics  

def getEdgeList(rule_net):
    
    gene_names = rule_net['Gene'].values
    
    gene_dict = {}
    
    for i in range(len(gene_names)):
        
        gene_dict[gene_names[i]] = i + 1
        
    
    edge_list = set()
    for index, row in rule_net.iterrows():
        rule = row['Rule']
        gene = row['Gene']
        
        for g in gene_names:
            
            if g in rule:
                
                edge_list.add((gene_dict[gene], gene_dict[g]))
    
    return edge_list

def Metrics(ground_truth, inferred):
    
    sizeNet = len(ground_truth)
    
    edges_ground = getEdgeList(ground_truth)
    edges_inferred = getEdgeList(inferred)
    
    edge_true = np.zeros((sizeNet, sizeNet))   
    edge_pred = np.zeros((sizeNet, sizeNet)) 
    
    for e in edges_ground: 
        edge_true[e[0]-1, e[1]-1] = 1
        edge_true[e[1]-1, e[0]-1] = 1   

    for e in edges_inferred:       
        edge_pred[int(e[0])-1, int(e[1])-1] = 1
        edge_pred[int(e[1])-1, int(e[0])-1] = 1  
        
    y_true = edge_true[np.triu_indices(sizeNet)]           
    y_pred = edge_pred[np.triu_indices(sizeNet)]  
    
    #print(edges_ground, edges_inferred)
    
    #print(edge_true, edge_pred)
    
    #print(y_true, y_pred)
    
    accuracy = round(metrics.accuracy_score(y_true, y_pred), 2)
    precision = round(metrics.precision_score(y_true, y_pred), 2)
    recall = round(metrics.recall_score(y_true, y_pred), 2)
    f1 = round(metrics.f1_score(y_true, y_pred), 2)
    
    metrics_dict = {'Accuracy': [accuracy], 'Precision':[precision], 'Recall':[recall], 'F1-Score':[f1]}
    
    return metrics_dict


def getEdgeList_BN(net):
    
    edge_list = []

    for e in net:

        from_ = int(e, 2)
        to = int(net[e], 2)

        edge_list.append((from_, to))

    return edge_list

def Metrics_BN(ground_truth, inferred):
    
    sizeNet = len(ground_truth)
    #print(sizeNet)
    
    edges_ground = getEdgeList_BN(ground_truth)
    edges_inferred = getEdgeList_BN(inferred)

    #print(ground_truth, inferred)
    #print(edges_ground, edges_inferred)
    
    edge_true = np.zeros((sizeNet, sizeNet))   
    edge_pred = np.zeros((sizeNet, sizeNet)) 
    
    for e in edges_ground: 
        edge_true[e[0], e[1]] = 1
        #edge_true[e[1], e[0]] = 1   

    for e in edges_inferred:       
        edge_pred[e[0], e[1]] = 1
        #edge_pred[e[1], e[0]] = 1 

    #print(edge_true)

    #print(edge_pred)
        
    #y_true = edge_true[np.triu_indices(sizeNet)]           
    #y_pred = edge_pred[np.triu_indices(sizeNet)]  

    y_true = edge_true.flatten()
    y_pred = edge_pred.flatten()
    
    #print(edges_ground, edges_inferred)
    
    #print(edge_true, edge_pred)
    
    print(y_true, y_pred)
    
    accuracy = round(metrics.accuracy_score(y_true, y_pred), 2)
    precision = round(metrics.precision_score(y_true, y_pred), 2)
    recall = round(metrics.recall_score(y_true, y_pred), 2)
    f1 = round(metrics.f1_score(y_true, y_pred), 2)
    
    metrics_dict = {'Accuracy': [accuracy], 'Precision':[precision], 'Recall':[recall], 'F1-Score':[f1]}
    
    return metrics_dict


"""if __name__ == "__main__":

    bn = {'000':'001',
          '001':'000',
          '010':'111',
          '100':'000',
          '011':'000',
          '101':'000',
          '110':'000',
          '111':'000'}
    
    bn_n = {'000':'000',
          '001':'000',
          '010':'111',
          '100':'000',
          '011':'000',
          '101':'000',
          '110':'000',
          '111':'000'}
    
    print(Metrics_BN(bn, bn_n))

    print(int('011',2))"""