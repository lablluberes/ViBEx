import dash
from dash import dcc, html, Input, Output, ClientsideFunction, dash_table, State
import numpy as np
import pandas as pd
import altair as alt
import math
from displacements.displacementMatrixes import getDisplacement
from statistics_methods.ProbabilityPerm import probBin
from statistics_methods.stringProbabilistic import call_C_statistics
import dash_vega_components as dvc

standard_dev = pd.read_csv("./statistics_methods/standard_dev.csv")

def get_stats_callback(app):

    def verify_thr_is_in_dict(gene, methods, thr_k, thr_b, thr_o, thr_s):
        for method in methods:
            if(method == 'BASC A'):
                if not all(key in thr_b for key in str(gene)):
                    return True

            elif(method == 'Onestep'):
                if not all(key in thr_o for key in str(gene)):
                    return True  

            elif(method == 'Shmulevich'):
                if not all(key in thr_s for key in str(gene)):
                    return True

            elif(method == 'K-Means'):
                if not all(key in thr_k for key in str(gene)):
                    return True
        
        return False

    @app.callback(
        Output('statistics-output', 'children'),
        Input('dropdown-method', 'value'),
        Input('dropdown-gene', 'value'), 
        Input('datatable-interactivity', 'data'),
        Input('thr_k','data'),
        Input('thr_o','data'),
        Input('thr_s','data'),
        Input('thr_b', 'data'),
        prevent_initial_call=True)
    def statistics_page(selected_method, selected_gene, data, thr_k, thr_o, thr_s, thr_b):

        # return none if values are none
        if selected_method is None or selected_method == []:
                return None
        if selected_gene is None or selected_gene == []:
                return None
        if data is None or data == []:
                return None
        
        cond = verify_thr_is_in_dict(selected_gene, selected_method, thr_k, thr_b, thr_o, thr_s)

        if cond:
            return None
            
        #create dataframe to access gene
        df = pd.DataFrame(data)
        labels = df['Gene ID']
        df = df.loc[:, df.columns!='Gene ID']

        selected = df.iloc[selected_gene]
        gene = selected.values
        sizeGene = len(gene)
        ogGene = pd.DataFrame({'x':np.arange(0,sizeGene),'y':gene, 'label': [f'{labels[selected_gene]}']* sizeGene})
        
        if len(gene) > 25:
            return html.Div("Most probable string cant be computed because the gene expression is too long. Performence issues arise.")
        
        xx = np.arange(0,sizeGene)
        #dict of thresholds and labels for graph display
        thr_dict = {'label':[],'y':[],'x':[]}

        #print(thr_k, selected_gene, gene)

        #print(thr_k, gene)


        for method in selected_method:
            if method == 'K-Means':
            #if thr_k is not None:
                    thr_k = thr_k[str(selected_gene)]

                    thr_dict['label'] = thr_dict['label'] + (['k-means']*sizeGene)
                    thr_dict['y'] = thr_dict['y'] + ([thr_k]*sizeGene)
                    thr_dict['x'] = thr_dict['x'] + xx.tolist()
            #if thr_o is not None:
            if method == 'Onestep':
                    thr_o = thr_o[str(selected_gene)]

                    thr_dict['label'] = thr_dict['label'] + (['onestep']*sizeGene)
                    thr_dict['y'] = thr_dict['y'] + ([thr_o]*sizeGene)
                    thr_dict['x'] = thr_dict['x'] + xx.tolist()
            #if thr_s is not None:
            if method == 'Shmulevich':
                    thr_s = thr_s[str(selected_gene)]

                    thr_dict['label'] = thr_dict['label'] + (['shmulevich']*sizeGene)
                    thr_dict['y'] = thr_dict['y'] + ([thr_s]*sizeGene)
                    thr_dict['x'] = thr_dict['x'] + xx.tolist()
            #if thr_b is not None:
            if method == 'BASC A':
                    thr_b = thr_b[str(selected_gene)]

                    thr_dict['label'] = thr_dict['label'] + (['BASC_A']*sizeGene)
                    thr_dict['y'] = thr_dict['y'] + ([thr_b]*sizeGene)
                    thr_dict['x'] = thr_dict['x'] + xx.tolist()


        thrs = pd.DataFrame.from_dict(thr_dict)

        #base graph
        ch = alt.Chart(
                ogGene
            ).mark_line(point=True).encode(
                        x=alt.X('x'),
                        y=alt.Y('y').scale(zero=False),
                        tooltip=['y','label'],
                        color='label'
            ).interactive()

        #line graph 

        lines = alt.Chart(thrs).mark_line().encode(
                            x=alt.X('x'),
                            y=alt.Y('y').scale(zero=False),
                            tooltip=['y','label'],
                            color='label'
                            ).interactive()
                            
        #combine to one chart

        chart = ch + lines

        #displacement index

        #label -> algorithm
        #string -> selected string
        #prob -> prob of said string
        #mean -> 1/3^n
        #sd -> standard deviation
        #res -> number of defined binarization/size of gene
        #highest -> string with highest probability
        #highestprob -> prob of said string
            
        prob_dict = {'label':[],'string':[],'prob':[],'mean':[],'sd':[],'res':[],'highest':[],'highestprob':[]}

        #range for displacement
        rangeIndex = math.ceil((max(gene)-min(gene))*10) - 1

        #get PDF for gene
        probden = pd.read_csv("./statistics_methods/cdf_"+str(rangeIndex+1)+".csv")
        disps = getDisplacement(selected_method,gene)

        #print(disps)
        #print("aqui estoy2")

        for method in selected_method:
            if method == 'K-Means':
            #if thr_k is not None:
                    
                    #get binarized gene string
                    count = 0
                    bin = ""
                    d = disps['k-means']
                    for g in gene:
                        if g > thr_k + d.iloc[0]:
                            bin += "1"
                        elif g < thr_k - d.iloc[0]:
                            bin += "0"
                        else:
                            bin += "?"
                            count += 1

                    #generate dataframe with all possible strings and their probabilities
                    #probBin function 
                    #probDF = probBin(gene,d.iloc[0],sizeGene,'k-means',probden)

                    high_p, high_string, p = call_C_statistics(gene, d.iloc[0], "k-means", bin)


                    #extract probability of selected string
                    #from dataframe probBin
                    binProb = p #probDF.loc[probDF['string']==bin]['prob'].iloc[0]
                    
                    #append selected val
                    prob_dict['label'].append('k-means')
                    prob_dict['string'].append(bin)
                    prob_dict['prob'].append(binProb)
                    prob_dict['res'].append((len(gene)-count)/len(gene))
                    prob_dict['mean'].append(1/(3**sizeGene))
                    prob_dict['sd'].append(standard_dev['k-means'].iloc[0])
                    
                    #append highest string prob and its prob
                    #probDF = probDF.sort_values(by=['prob'])
                    prob_dict['highest'].append(high_string)#probDF['string'].iloc[-1])
                    prob_dict['highestprob'].append(high_p)#probDF['prob'].iloc[-1])
                
            if method == 'Onestep': 
            #if thr_o is not None:
                    #get binarized gene
                    count = 0
                    bin = ""
                    d = disps['onestep']
                    for g in gene:
                        if g > thr_o + d.iloc[0]:
                            bin += '1'
                        elif g < thr_o - d.iloc[0]:
                            bin += '0'
                        else:
                            bin += '?'
                            count += 1

                    #generate dataframe with all possible strings and their probabilities
                    #probBin function 
                    #probDF = probBin(gene,d.iloc[0],sizeGene,'k-means',probden)

                    high_p, high_string, p = call_C_statistics(gene, d.iloc[0], "onestep", bin)


                    #extract probability of selected string
                    #from dataframe probBin
                    binProb = p #probDF.loc[probDF['string']==bin]['prob'].iloc[0]
                    
                    #append selected val
                    prob_dict['label'].append('onestep')
                    prob_dict['string'].append(bin)
                    prob_dict['prob'].append(binProb)
                    prob_dict['res'].append((len(gene)-count)/len(gene))
                    prob_dict['mean'].append(1/(3**sizeGene))
                    prob_dict['sd'].append(standard_dev['onestep'].iloc[0])
                    
                    #append highest string prob and its prob
                    #probDF = probDF.sort_values(by=['prob'])
                    prob_dict['highest'].append(high_string)#probDF['string'].iloc[-1])
                    prob_dict['highestprob'].append(high_p)#probDF['prob'].iloc[-1])

            #DO THE SAME FOR ALL ALGORITHMS
            if method == 'Shmulevich': 
            #if thr_s is not None:
                    #get binarized gene
                    count = 0
                    bin = ""
                    d = disps['shmulevich']
                    for g in gene:
                        if g > thr_s + d.iloc[0]:
                            bin += '1'
                        elif g < thr_s - d.iloc[0]:
                            bin += '0'
                        else:
                            bin += '?'
                            count += 1
                    
                    
                    #generate dataframe with all possible strings and their probabilities
                    #probBin function 
                    #probDF = probBin(gene,d.iloc[0],sizeGene,'k-means',probden)

                    high_p, high_string, p = call_C_statistics(gene, d.iloc[0], "shmulevich", bin)


                    #extract probability of selected string
                    #from dataframe probBin
                    binProb = p #probDF.loc[probDF['string']==bin]['prob'].iloc[0]
                    
                    #append selected val
                    prob_dict['label'].append('shmulevich')
                    prob_dict['string'].append(bin)
                    prob_dict['prob'].append(binProb)
                    prob_dict['res'].append((len(gene)-count)/len(gene))
                    prob_dict['mean'].append(1/(3**sizeGene))
                    prob_dict['sd'].append(standard_dev['shmulevich'].iloc[0])
                    
                    #append highest string prob and its prob
                    #probDF = probDF.sort_values(by=['prob'])
                    prob_dict['highest'].append(high_string)#probDF['string'].iloc[-1])
                    prob_dict['highestprob'].append(high_p)#probDF['prob'].iloc[-1])

            if method == 'BASC A': 
            #if thr_b is not None:
                    #get binarized gene
                    count = 0
                    bin = ""
                    d = disps['BASC_A']
                    for g in gene:
                        if g > thr_b + d.iloc[0]:
                            bin += '1'
                        elif g < thr_b - d.iloc[0]:
                            bin += '0'
                        else:
                            bin += '?'
                            count += 1
                    
                    
                    #generate dataframe with all possible strings and their probabilities
                    #probBin function 
                    #probDF = probBin(gene,d.iloc[0],sizeGene,'k-means',probden)

                    high_p, high_string, p = call_C_statistics(gene, d.iloc[0], "BASC_A", bin)


                    #extract probability of selected string
                    #from dataframe probBin
                    binProb = p #probDF.loc[probDF['string']==bin]['prob'].iloc[0]
                    
                    #append selected val
                    prob_dict['label'].append('BASC_A')
                    prob_dict['string'].append(bin)
                    prob_dict['prob'].append(binProb)
                    prob_dict['res'].append((len(gene)-count)/len(gene))
                    prob_dict['mean'].append(1/(3**sizeGene))
                    prob_dict['sd'].append(standard_dev['BASC_A'].iloc[0])
                    
                    #append highest string prob and its prob
                    #probDF = probDF.sort_values(by=['prob'])
                    prob_dict['highest'].append(high_string)#probDF['string'].iloc[-1])
                    prob_dict['highestprob'].append(high_p)#probDF['prob'].iloc[-1])
                
        #create dataframe from dict
        df = pd.DataFrame.from_dict(prob_dict)

        #FOR STRINGS
        strngs = df.drop(columns=['res','mean','sd']).copy()
        strngs = strngs.round(5)

        #FOR STATS
        df['dif'] = df['mean'] - df['prob']
        df['z'] = df['dif']/df['sd']
        df = df.drop(columns=['highest','highestprob'])
        df = df.round(5)
        
        # return only the selected gene plot with threshold if number of interpolation is not selected
        if(selected_gene is not None):

                return [ 
                        html.Div([
                            html.Div([
                            
                                dvc.Vega(
                                        id="altair2",
                                        opt={"renderer": "svg", "actions": False},
                                        spec=chart.to_dict(),
                                    ),
                            dash_table.DataTable(df.to_dict('records'),style_table={'overflowX': 'auto'}),
                                            
                            ], style={'display':'flex', 'flexDirection':'column', 'padding': 3, 'flex': 1, 'width': '50%'}),
                            
                            dash_table.DataTable(strngs.to_dict('records'),style_table={'overflowX': 'auto'}),
                            
                            
                        ], style={'display':'flex', 'flexDirection':'row', 'flex': 1})
                    ]

            # return nothing
        else:
                return None