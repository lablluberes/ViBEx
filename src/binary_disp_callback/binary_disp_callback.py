##############################################
#
# This file contains the callback components for Binarization, Displacement tabs 
#
##############################################

import dash
from dash import dcc, html, Input, Output, ClientsideFunction, dash_table, State
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# import displacement and voting methods
from displacements.displacementMatrixes import getDisplacement
from binarization.voting_algos import election_strings

# function to return components 
def get_bin_disp_callback(app):
    """
        get_bin_disp_callback returns components of binarization, and displacement

        app: app object to add callbacks to ViBEx
    """

    def verify_thr_is_in_dict(gene, methods, thr_k, thr_b, thr_o, thr_s):

        """
            verify_thr_is_in_dict verifies that the threshold of a gene are in the selected methods 

            gene: selected genes
            methods: selected thr methods
            thr_k: dictionary for kmeans thr
            thr_b: dictionary for basca thr
            thr_o: dictionary for onestep thr
            thr_s: dictionary for shmulevich thr
        """

        # iterate over selected methods
        for method in methods:
            # verifies if thr of a gene was computed 
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

    def make_grid_disp(methods, gene, data, thr_k, thr_o, thr_s, thr_b, disps):
        """
            make_grid_disp makes a grid plot showing the displacement of thr by each selected method

            methods: selected thr methods
            gene: selected gene
            data: dataset of genes
            thr_k: dictionary for kmeans thr
            thr_b: dictionary for basca thr
            thr_o: dictionary for onestep thr
            thr_s: dictionary for shmulevich thr
            disps: displacement matrix 
        """
        
        #methods = ['BASC A', 'K-Means', 'Onestep']
        
        # create subplot 2x2 with titles for each method
        fig = make_subplots(rows=2, cols=2, subplot_titles=["Displacement of " + m for m in methods])
        
        # extract gene expression from dataset
        y = list(data[gene].values())
        # get name of gene
        label = y[-1]
        y.pop(-1)
        
        # row, col to add plot in subplot
        row = 1
        col = 1
        
        # legend
        legend = True

        # colors for displacements
        fillcolor = ['#dae5ef', '#ffdddd', '#ddf5dd', '#ffe7d2']
        
        # iterate selected thr methods
        for i in range(len(methods)):
            
            # based on each selected method extract the displacement, and threshold value
            if methods[i] == "BASC A":
                dis = disps['BASC_A'].values[0]
                thr = thr_b[str(gene)]
                
            elif methods[i] == "Onestep":
                dis = disps['onestep'].values[0]
                thr = thr_o[str(gene)]
                
            elif methods[i] == "K-Means":
                dis = disps['k-means'].values[0]
                thr = thr_k[str(gene)]
                
            else:
                dis = disps['shmulevich'].values[0]
                thr = thr_s[str(gene)]
                #print(thr, dis)
            
            # verifies that displacement does not end up less or more than the actual gene expression
            minY = thr - dis
            maxY = thr + dis
            
            if minY <= min(y):
                minY = min(y)
                
            if maxY >= max(y):
                maxY = max(y)
            
            # false so that gene expression only appears once in legend 
            if i >= 1:
                legend = False
            
            # create x array of numbers from 0 to n timesteps (based on length of gene)
            x = np.arange(len(y))
            
            # adds figure of plot in position row x col. This figure is the gene expression
            fig.add_trace(
                go.Scatter(x=x, y=y, name=label, showlegend=legend, line_color='blue'),
                row=row, col=col
            )
            
            # x, y coordinarted to create a rectangle for the displacement
            x_dis = [0, 0, len(y)-1, len(y)-1, 0]
            y_dis = [minY, maxY, maxY, minY, minY]
            
            # creates a displacement rectangle 
            fig.add_trace(
                go.Scatter(x=x_dis, y=y_dis, fill="toself", mode='none', name=methods[i], hoverinfo="skip", fillcolor=fillcolor[i], opacity=0.7), row=row, col=col
            )

          
            # make x axis range 0 to n-1
            fig.update_xaxes(
            range=[0, len(y)-1])
            
            # make y axis range min(gene) to max(gene) + 0.01
            fig.update_yaxes(
                range=[min(y), max(y)+0.01])
            
            # increase row position
            if col == 2:
                row += 1
                col = 1
            # increase column position
            else:
                col += 1
        
        # modifies xaxis color
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey')
        
        # modifies yaxis color
        fig.update_yaxes(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='black',
                gridcolor='lightgrey')
            
        # updates plot color and size 
        fig.update_layout(height=800, width=800, plot_bgcolor='white')
        
        # return figure 
        return fig
        

    def make_plot(methods, gene, data, thr_k, thr_o, thr_s, thr_b, splineGenes):
        """
            make_plot creates a single plot showing the thr of each method, og gene expression, and spline of gene

            methods: selected thr methods
            gene: selected gene
            data: dataset of genes
            thr_k: dictionary for kmeans thr
            thr_b: dictionary for basca thr
            thr_o: dictionary for onestep thr
            thr_s: dictionary for shmulevich thr
            splineGenes: gene interp
        """
        
        # create figure 
        fig = go.Figure()

        # color for lines 
        fillcolor = ['#dae5ef', '#ffdddd', '#ddf5dd', '#ffe7d2']
        fillcolor = ['red', 'blue', 'green', 'orange']
        
        # extract gene spline
        ySpline = splineGenes[str(gene)]

        # extract original gene 
        y = list(data[gene].values())
        # extract name of gene
        label = y[-1]
        y.pop(-1)
        
        # obtain x range of length of og gene
        x = np.arange(len(y))
        
        # plot original gene expression
        fig.add_trace(
                go.Scatter(x=x, y=y, name=label, showlegend=True, line_color='blue')
        )
        
        # create x based on range if spline but sized of original gene
        xSpline = np.linspace(0, len(y)-1, len(ySpline))
        
        # add plot of spline gene expression
        fig.add_trace(
                go.Scatter(x=xSpline, y=ySpline, name=label+" Spline", showlegend=True, line_color='red')
        )
        
        # lines for each thr method
        dash = ['dot', 'dash', 'longdash', 'dashdot']
        index= 0 
        
        # iterate over selected thr methods
        for m in methods:
            
            # extract thr value of each method based on gene
            if m == "BASC A":
                thr = thr_b[str(gene)]
                
            elif m == "Onestep":
                thr = thr_o[str(gene)]
                
            elif m == "K-Means":
                thr = thr_k[str(gene)]
                
            else:
                thr = thr_s[str(gene)]
            
            # create y thr line
            yThr = np.full(len(y), thr)
            
            # add line to plot of thr 
            fig.add_trace(
                go.Scatter(x=x, y=yThr, name=m, showlegend=True, line=dict(dash=dash[index], color=fillcolor[index]))
                
            )
            index += 1
        
        # update x axis range and color
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            range=[0, len(y)-1])
        
        # update y axis range and color
        fig.update_yaxes(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='black',
                gridcolor='lightgrey',
                range=[min(y), max(y)+0.01])
            
        # update plot layout and size 
        fig.update_layout(height=800, width=800, plot_bgcolor='white', title="Threshold for "+label,
                        xaxis_title="Time Series", yaxis_title="Expression Level")
            
        # return figure 
        return fig    

    #### Callback - Shows the displacement plots 
    @app.callback(Output('displacements-output', 'children'),
                Input('dropdown-gene', 'value'),
                Input('datatable-interactivity', 'data'),
                Input('dropdown-method', 'value'),
                Input('thr_k', 'data'),
                Input('thr_o', 'data'),
                Input('thr_s', 'data'),
                Input('thr_b', 'data'),
                Input('spline-genes', 'data'),
                prevent_initial_call=True)
    def displacement_tabs(gene, data, methods, thr_k, thr_o, thr_s, thr_b, spline_genes):
        """
            displacement_tabs renders the plots of displacements, and thrs.

            methods: selected thr methods
            gene: selected gene
            data: dataset of genes
            thr_k: dictionary for kmeans thr
            thr_b: dictionary for basca thr
            thr_o: dictionary for onestep thr
            thr_s: dictionary for shmulevich thr
            spline_genes: gene interp
        
        """

        # if no genes, method selected return message 
        if gene == [] or methods == None or methods == [] or gene == None:
            return "Select genes or threshold methods to binarize."
        
        # verify that the thr were computed 
        cond = verify_thr_is_in_dict(gene, methods, thr_k, thr_b, thr_o, thr_s)

        # if cond true then return None because thr computation not finished 
        if cond:
            return None
        
        # extract selected gene expression
        gene_selected = list(data[(gene)].values())
        # delete name of gene
        gene_selected.pop(-1)
        
        # obtain displacement of gene 
        disps = getDisplacement(methods,gene_selected)

        #print(thr_s)

        # return dash components for displacement tab
        return [ html.Div(style={"height": "20px"}), dbc.Card(
                    dbc.CardBody([
                        html.Hr(),html.P("Spline approximation of gene expression and threshold displacement for every algorithm. The voting table shows the binarization using selected algorithms and the consensus binarization.", style={'textAlign': 'center'}),
                        html.Br(), html.P("*Values that are too close to the threshold will be considered undecided with a (?) on the table."),
                    ]),
                    className="mb-3",
                ),
            
                # Tabs inside Displacement Tab (Thresholds, and Displacements)
                dcc.Tabs([
                            dcc.Tab(label='Thresholds', children=[
                                html.Div(style={"height": "20px"}),
                                dbc.Card(
                                    dbc.CardBody(html.P("Threshold for each algorithm on selected gene."),),
                                    className="mb-3",
                                ),
                                html.Div(style={"height": "20px"}),
                                dbc.Card(
                                    dbc.CardBody(dcc.Graph(figure=make_plot(methods, gene, data, thr_k, thr_o, thr_s, thr_b, spline_genes))),
                                    className="mb-3",
                                ),
                                
                        ]),
                        dcc.Tab(label='Displacements', children=[
                                
                                html.Div(style={"height": "20px"}),
                                dbc.Card(
                                    dbc.CardBody(dcc.Graph(figure=make_grid_disp(methods, gene, data, thr_k, thr_o, thr_s, thr_b, disps))),
                                    className="mb-3",
                                ),
                        
                        ])
                    
                    ])               
                
                ]

    #### Callback - Output Binarization table 
    @app.callback(Output('binarization-output', 'children'),
                Input('dropdown-gene', 'value'),
                Input('datatable-interactivity', 'data'),
                Input('dropdown-method', 'value'),
                Input('thr_k', 'data'),
                Input('thr_o', 'data'),
                Input('thr_s', 'data'),
                Input('thr_b', 'data'),
                prevent_initial_call=True)
    def binarization_tab(gene, data, methods, thr_k, thr_o, thr_s, thr_b): 

        """
            binarization_tab outputs a table showing binarizations of gene

            methods: selected thr methods
            gene: selected gene
            data: dataset of genes
            thr_k: dictionary for kmeans thr
            thr_b: dictionary for basca thr
            thr_o: dictionary for onestep thr
            thr_s: dictionary for shmulevich thr
        """

        # if no gene or methods selected send message 
        if gene == [] or methods == None or methods == [] or gene == None:
            return "Select genes or threshold methods to binarize."
        
        # verify that thr has been computed 
        cond = verify_thr_is_in_dict(gene, methods, thr_k, thr_b, thr_o, thr_s)

        # thr not computed wait until computation
        if cond:
            return None
        
        # return binarization table 
        return vote_table(gene, methods, data, thr_b, thr_k, thr_s, thr_o)


    def vote_table(row, selected_method, data, thr_b, thr_k, thr_s, thr_o):

        """
            vote_table - generates voting table 

            selected_method: selected thr methods
            row: selected gene
            data: dataset of genes
            thr_k: dictionary for kmeans thr
            thr_b: dictionary for basca thr
            thr_o: dictionary for onestep thr
            thr_s: dictionary for shmulevich thr
        """
        
        # if there are no gene, seleced methods or data selected then return None
        if row is None or selected_method is None or data is None:
            return None
        
        # get dataframe of dataset
        df = pd.DataFrame(data)
        # extract gene lanel
        labels = df['Gene ID']
        df = df.loc[:, df.columns!='Gene ID']

        # get selected gene
        selected = df.iloc[row]
        gene = selected.values
        
        # extract displacement based on gene range
        disps = getDisplacement(selected_method,gene)

        #print(disps)
        
        t = []
        d = []

        # go through each method and extract the thr, and disp
        for method in selected_method:

            # extract thr, and disp of each method of the gene
            if(method == 'BASC A'):
           
                t.append(thr_b[str(row)])
            
                d.append(disps['BASC_A'].iloc[0])
    
            elif(method == 'K-Means'):
            
                t.append(thr_k[str(row)])
            
                d.append(disps['k-means'].iloc[0])
        
            elif(method == 'Onestep'):
            
                t.append(thr_o[str(row)])
            
                d.append(disps['onestep'].iloc[0])
                
            else:
             
                t.append(thr_s[str(row)])
                
                d.append(disps['shmulevich'].iloc[0])
    
        #print(gene, t, d)
        # generate voting (elected string) of the gene based on thr, and displacements
        votes = election_strings(gene, t, d)
        
        rows_data = []
        
        # append each binarization (voting table) as a row 
        for line in votes[0]:
            rows_data.append(line)
            
        # append final (elected) vote as last row
        rows_data.append(votes[1])

        
        # append final label
        selected_method.append("Elected")
        
        # create dataframe of voting table 
        vote_df = pd.DataFrame(data=rows_data, index=selected_method)
        vote_df.reset_index(inplace=True)
    
        # return components and voting table. colors 0s to red, 1s to green, and ? to yellow 
        return  html.B('Voting Table of ' + labels[row]), dash_table.DataTable(vote_df.to_dict('records'), [{"name": str(i), "id": str(i)} for i in vote_df.columns],
                style_data = {'borderBottom': '5px solid white'},
                style_cell={'minWidth': '50px', 'maxWidth': '50px'},
                style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{{{col}}} = "?"'.format(col=str(col)),
                        'column_id': str(col),
                        'row_index': 'odd'
                    },
                    'backgroundColor': 'rgb(255, 255, 192, 0.3)',
                } for col in vote_df.columns
                ] +
                [
                {
                    'if': {
                        'filter_query': '{{{col}}} = "?"'.format(col=str(col)),
                        'column_id': str(col),
                        'row_index': 'even'
                    },
                    'backgroundColor': 'rgb(255, 255, 192, 0.3)',
                } for col in vote_df.columns
                ] +
                
                [
                    {
                        'if': {
                            'filter_query': '{{{col}}} = 1'.format(col=str(col)),
                            'column_id': str(col),
                            'row_index': 'odd'
                        },
                        'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                    } for col in vote_df.columns
                ] +
                [
                    {
                        'if': {
                            'filter_query': '{{{col}}} = 0'.format(col=str(col)),
                            'column_id': str(col),
                            'row_index': 'odd'
                        },
                        'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                    } for col in vote_df.columns
                ] +
                [
                    {
                        'if': {
                            'filter_query': '{{{col}}} = 0'.format(col=str(col)),
                            'column_id': str(col),
                            'row_index': 'even'
                        },
                        'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                    } for col in vote_df.columns
                ] +
                [
                    {
                        'if': {
                            'filter_query': '{{{col}}} = 1'.format(col=str(col)),
                            'column_id': str(col),
                            'row_index': 'even'
                        },
                        'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                    } for col in vote_df.columns
                ],
                style_table={'height': '300px', 'overflowY': 'auto', 'overflowX':'auto'}
                ), 