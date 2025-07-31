##############################################
#
# This file contains the callback components for value imputation buttons and dropdowns.
# In addition, functions doing each type of imputations are given
#
##############################################
from dash import dcc, html, Input, Output, ClientsideFunction, dash_table, State
import dash
import pandas as pd
import numpy as np
import math

# import get displacement function
from displacements.displacementMatrixes import getDisplacement
# import string probabilistic function
from statistics_methods.stringProbabilistic import probabilistic, call_C_statistics
# import missforest imputation 
from imputation.imputation_ml import imputate_missforest, imputate_mice_logictic

from statistics_methods.ProbabilityPerm import probBin

# function to return components 
def get_imputation_callbacks(app):
    """
        get_imputation_callbacks returns components of value imputation 

        app: app object to add callbacks to ViBEx
    """

    #### Callback - Outputs dropdowns of binarization to imputate and dropdown of type of imputation
    @app.callback(
        Output("imputate-dropdowns", 'children'),
        Input('dropdown-method', 'value'), 
        prevent_initial_call=True)
    def imputate_dropdowns(methods):
        """
            imputate_dropdowns - generates dropdowns of binarization to imputate and dropdown of type of imputation

            methods: selected thr methods
        """

        # if no selected thr methods return None
        if methods is None or methods == []:
            #methods = []
            return None
        
        # check which methods were not selected (so callback gives no errors)
        all_methods = list(set(['BASC A', 'K-Means', 'Shmulevich', 'Onestep']) - set(methods))

        components_tables = []

        # save in storage the not selected methods binarizations as empty (to prevent callback error)
        for m in all_methods:
            components_tables.append(dcc.Store(f"{m}-data", data={}))

        
        #print(methods, " en imputation")
        
        # returns dash components of value imputation 
        return html.Div(children = [
            
            # dropdown to select binarization
            html.B('Select method state table to imputate values:'),
                            dcc.Dropdown(
                                methods+['Elected'],
                                placeholder="Select method table",
                                id="imputate-method",
                                multi=False,
                                searchable=False),
            
            # dropdown select imputation type 
            html.B('Select an option to imputate values:'),
                            dcc.Dropdown(
                                options=[
                                {'label': 'MissForest Imputation', 'value':4},
                                {'label': 'IterativeImputer (MICE with LogReg) Imputation', 'value':5},
                                {'label': 'Framework Statistics Algorithm', 'value':3},
                                {'label': 'Global Imputation (ex: changes all "?" to either 0 or 1)', 'value':0},
                                {'label': 'Gene Imputation (ex: imputates a value for only one gene)', 'value':1},
                                {'label': 'Time Impuation (ex: imputates values based on time course)', 'value':2},
                                ],
                                placeholder="Select option",
                                id="imputate-option",
                                multi=False,
                                searchable=False),
            

            # imputation buttons not displayed (to prevent callback error)
            html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),

            html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
            html.Button('Imputate', id='other-impu-button', style={'display':'none'}),
            
            # generate dropdown for imputation based on imputation type selected
            html.Div(id='dropdown-imputate-options'),

            # save storage variables
            html.Div(components_tables),

            # button to reset binarization to original state
            html.Button('Reset Imputations', id='reset-imputation'),

            
            # more components (buttons and dropdowns) set hidden (to prevent callback error)
            html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
        
            html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
            
            html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
            
            dcc.Dropdown(
                [],
                placeholder="Select gene",
                id="imputate-gene",
                multi=True,
                searchable=False,
                style={'display': 'none'}),

            dcc.Dropdown(
                    [],
                    placeholder="Select time courses",
                    id="imputate-time",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'}),
            
        ])


    #### Callback - Outputs and resets each binarization state table to original values
    @app.callback(
        Output('Elected-table-dropdown', 'data', allow_duplicate=True),
        Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
        Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
        Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
        Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
        Output('reset-imputation', 'n_clicks'),
        Input('reset-imputation', 'n_clicks'),
        State('Elected-data', 'data'),
        State('K-Means-data', 'data'),
        State('Shmulevich-data', 'data'),
        State('BASC A-data', 'data'),
        State('Onestep-data', 'data'),
        Input('imputate-method', 'value'),
        prevent_initial_call=True
    )
    def reset_table(n_clicks, elected, kmeans, shmulevich, basc, onestep, table):
        """
            reset_table - resets binarization table to original values

            n_clicks: reset button pressed
            elected: elected orignal table data
            kmeans: kmeans orignal table data
            shmulevich: shmulevich orignal table data
            basc: basc orignal table data
            onestep: onestep orignal table data
            table: selected table to reset
        """

        # if no clicks or table selected do nothing 
        if n_clicks is None or table is None or table == []:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None
        
        # result list to reset values (outputs)
        result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None]

        # based on the selected binarization table reset data to original binarization
        if table == "Elected":
        
            result[0] = elected

            return tuple(result)
        
        elif table == "BASC A":

            result[1] = basc

            return tuple(result) 
        
        elif table == "K-Means":

            result[2] = kmeans

            return tuple(result)
            
        elif table == "Onestep":

            result[4] = onestep

            return tuple(result)
        
        else:

            result[3] = shmulevich

            return tuple(result)

    #### Callback - Ouputs imputate button based on selected type of value imputation
    @app.callback(
        Output("dropdown-imputate-options", 'children'),
        Input('imputate-option', 'value'),
        Input('datatable-interactivity', 'selected_rows'),
        Input('datatable-interactivity','data'),
        prevent_initial_call=True)
    def imputate_options(option, rows, data):
        """
            imputate_options - generates buttons to imputate based on selected type

            option: selected type of imputation
            rows: rows selected from dataset
            data: gene exp dataset
        
        """

        # if no option selected do nothing
        if option is None or option == []:
            return None
        
        # sort rows (selected genes)
        rows.sort()

        # return button to imputate all undecided values to 0s or 1s
        if option == 0:

            return html.Div([
            html.Button('Imputate 1', id='all-to-1'),
            html.Button('Imputate 0', id='all-to-0'),

            # hidden components to prevent callback error
            html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
            html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
            html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),
            html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
            html.Button('Imputate', id='other-impu-button', style={'display':'none'}),
            dcc.Dropdown(
                [],
                placeholder="Select gene",
                id="imputate-gene",
                multi=True,
                searchable=False,
                style={'display': 'none'}),
            dcc.Dropdown(
                    [],
                    placeholder="Select time courses",
                    id="imputate-time",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'}),
        ])

        # return dropdown to select which gene to imputate and buttons to imputate all undecided values to 0s, and 1s
        elif option == 1:

            # read gene dataset
            df = pd.DataFrame(data)

            # extract labels
            df = df['Gene ID']
            labels = df[rows]

            # returns dropdown to which gene to imputate values, and imputation buttons 
            return html.Div(children = [
                html.B('Select a gene to imputate values:'),
                dcc.Dropdown(
                    labels,
                    placeholder="Select gene",
                    id="imputate-gene",
                    multi=True,
                    searchable=False),
                html.Button('Imputate 1', id='gene-to-1'), html.Button('Imputate 0', id='gene-to-0'),

                # hidden components to prevent callback error
                html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
                html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),
                html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
                html.Button('Imputate', id='other-impu-button', style={'display':'none'}),
                dcc.Dropdown(
                        [],
                        placeholder="Select time courses",
                        id="imputate-time",
                        multi=True,
                        searchable=False,
                        style={'display': 'none'}),
                ])


        # return dropdown to select which time course to imputate and buttons to imputate all undecided values to 0s, and 1s
        elif option == 2:

            # read dataset of genes
            df = pd.DataFrame(data)

            # number of time points
            df = len(df['Gene ID'])

            # create dropdown options 
            options = [{'label':"Time " + str(i), 'value': i} for i in np.arange(0, df)]

            #print(options)

            # return dropdown to select time course to imputate, and buttons 
            return html.Div(children = [
                html.B('Select an time courses to imputate values:'),
                dcc.Dropdown(
                    options,
                    placeholder="Select time courses",
                    id="imputate-time",
                    multi=True,
                    searchable=False),
                html.Button('Imputate 1', id='time-to-1'), html.Button('Imputate 0', id='time-to-0'),

                # hidden components to prevent callback error
                html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
                html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
                html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),
                html.Button('Imputate', id='other-impu-button', style={'display':'none'}),
                dcc.Dropdown(
                    [],
                    placeholder="Select gene",
                    id="imputate-gene",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'}),
                ])
        

        # return button to imputate all undecided values to 0s, and 1s using statistics 
        elif option == 3:

            # returns buttons 
            return html.Div([

                html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
                html.Button('Imputate', id='other-impu-button', style={'display':'none'}),
                
                # button to imputate based on statistics
                html.Button('Imputate Strings based on Statistics', id='stat-impu-button'),
                

                html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
                dcc.Dropdown(
                    [],
                    placeholder="Select gene",
                    id="imputate-gene",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'}),
                dcc.Dropdown(
                    [],
                    placeholder="Select time courses",
                    id="imputate-time",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'})

            ])


        # return button to imputate all undecided values to 0s, and 1s using MissForest
        elif option == 4:
            
            # returns buttons 
            return html.Div([

                # MissForest button
                html.Button('Imputate MissForest', id='missforest-button'),

                # return hidden buttons (prevents callback error)
                html.Button('Imputate Strings based on Statistics', id='stat-impu-button', style={'display': 'none'}),
                html.Button('Imputate', id='other-impu-button', style={'display':'none'}),
                html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
    
                dcc.Dropdown(
                    [],
                    placeholder="Select gene",
                    id="imputate-gene",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'}),

                dcc.Dropdown(
                    [],
                    placeholder="Select time courses",
                    id="imputate-time",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'})

            ])
        elif option == 5:
            # returns buttons 
            return html.Div([

        
                html.Button('Imputate', id='other-impu-button'),

                # return hidden buttons (prevents callback error)
                html.Button('Imputate Strings based on Statistics', id='stat-impu-button', style={'display': 'none'}),
                html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
                html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
                html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
                html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
    
                dcc.Dropdown(
                    [],
                    placeholder="Select gene",
                    id="imputate-gene",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'}),

                dcc.Dropdown(
                    [],
                    placeholder="Select time courses",
                    id="imputate-time",
                    multi=True,
                    searchable=False,
                    style={'display': 'none'})

            ])
            
        # return none if no option chosen 
        else:
            return None
            

    def imputate_value_all(data, value):
        """
            imputate_value_all - imputates all undecided values to either 1s or 0s
        """

        # read dataset
        df = pd.DataFrame(data)

        # imputate values 
        df.replace("?", value, inplace=True)

        # return imputation 
        return df.to_dict('records')


    #### Callback - assigns the output binarization tables the imputation values (either all to 0s or all 1s)
    @app.callback(
        Output('Elected-table-dropdown', 'data', allow_duplicate=True),
        Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
        Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
        Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
        Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
        Output('all-to-1', 'n_clicks'),
        Output('all-to-0', 'n_clicks'),
        Input('all-to-1', 'n_clicks'),
        Input('all-to-0', 'n_clicks'),
        Input('imputate-option', 'value'),
        Input('imputate-method', 'value'),
        State('Elected-table', 'data'),
        State('BASC A-table', 'data'),
        State('K-Means-table', 'data'),
        State('Shmulevich-table', 'data'),
        State('Onestep-table', 'data'),
        prevent_initial_call=True)
    def imputate_table(n_clicks, n_clicks2, option, method, elected, basc, kmeans, shmulevich, onestep):
        """
            imputate_table - assigns the output binarization tables the imputation values (either all to 0s or all 1s)

            n_clicks - button to imputate to 1s
            n_clicks2 - button to imputate to 0s
            option - type of imputation selected
            method - table to imputate values
            elected: elected table data
            kmeans: kmeans table data
            shmulevich: shmulevich table data
            basc: basc table data
            onestep: onestep table data

        """
        
        # if no button pressed, opption selected or methods. return None
        if n_clicks is None and n_clicks2 is None or option == None or method == [] or method is None:
            #print("aquiii")
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None
        
        #print("imputate all")

        # get the table that will be imputated based on method
        if method == "Elected":
            indx = 0
            data = elected
        
        elif method == "BASC A":
            indx = 1
            data = basc
        
        elif method == "K-Means":
            indx = 2
            data = kmeans

        elif method == "Onestep":
            indx = 4
            data = onestep
        
        else:
            indx = 3
            data = shmulevich
        
        # output variable to update tables
        result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None]


        # when imputate all to 1s is pressed imputate it
        if n_clicks != None and option == 0:

            # imputate datatable
            data = imputate_value_all(data, 1)
            
            # return changes
            result[indx] = data

            #print(result)
        
            return tuple(result)
        
        # when imputate all to 0s is pressed imputate it
        elif n_clicks2 != None and option == 0:

            # imputate datatable
            data = imputate_value_all(data, 0)

            # return changes
            result[indx] = data

            return tuple(result)


    def imputate_value_gene(df, value, genes):
        """
            imputate_value_gene - imputates selected genes to either all 1s or 0s
        """
        
        # get dataset
        df = pd.DataFrame(df)


        # for every selected gene imputate undecided states to either 1s or 0s
        for g in genes:

            df[g] = df[g].replace("?", value)

        #print(df)

        # return changes
        return df.to_dict('records')


    #### Callback - Outputs imputated tables based on statistics 
    @app.callback(
        Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
        Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
        Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
        Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
        Output('Elected-table-dropdown', 'data', allow_duplicate=True),
        Output('stat-impu-button', 'n_clicks'),
        

        Input('stat-impu-button', 'n_clicks'),
        Input('imputate-method', 'value'),
        Input('datatable-interactivity','data'),
        Input('datatable-interactivity', 'selected_rows'),
        State('BASC A-table', 'data'),
        State('K-Means-table', 'data'),
        State('Shmulevich-table', 'data'),
        State('Onestep-table', 'data'),
        Input('dropdown-method', 'value'),
        State('Elected-table', 'data'),
        prevent_initial_call=True)
    def imputate_based_statistics(n_clicks, method, dataset, rows, basc, kmeans, shmulevich, onestep, thr_methods_selected, elected):

        """
            imputate_based_statistics - imputates table based on statistics 

            n_clicks: button pressed
            method: table to imputate
            dataset: dataset genes
            rows: selected genes
        
        """
        
        # return none if Inputs are not selected
        if n_clicks is None or method == [] or method is None:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None
        
        # output list variable 
        result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None]
        #print("aqui estoy")
        # if button is pressed imputate 
        if n_clicks != None:

            # read dataset
            data = pd.DataFrame(dataset)

            # sort selected genes
            rows.sort()

            # get labels of genes
            labels = data['Gene ID']

            data = data.loc[:, data.columns!='Gene ID']

            # get selected gene expressions
            genes = data.iloc[rows].values.astype(float)

            # organize labels 
            labels = [labels[i] for i in rows]

            string_dict = {} 


            # iterate selected genes
            for i in range(len(genes)):
                
                # displacement table
                if method != 'Elected':
                    disps = getDisplacement([method], genes[i])
                rangeIndex = math.ceil((max(genes[i])-min(genes[i]))*10) - 1

                #get PDF for gene
                #probden = pd.read_csv("./statistics_methods/cdf_"+str(rangeIndex+1)+".csv")

                # extracts displacement based on selected method
                if(method == 'BASC A'):
                    print("basc stats")
                    d = disps['BASC_A'].iloc[0]

                    df = pd.DataFrame(basc)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'BASC_A', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string
        
                elif(method == 'K-Means'):
                    print("kmeans stats")
                    d = disps['k-means'].iloc[0]

                    df = pd.DataFrame(kmeans)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'k-means', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string
            
                elif(method == 'Onestep'):
                    print("onestep stats")
                    d = disps['onestep'].iloc[0]

                    df = pd.DataFrame(onestep)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'onestep', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string

                elif method == 'Elected':
                    
                    high_probs = []
                    strings_probs = []

                    df1 = pd.DataFrame(elected)

                    og_binarization = df1[labels[i]].values

                    print("doing elected stats")
                    for m in thr_methods_selected:
                        disps = getDisplacement([m], genes[i])
                        if m == 'BASC A':
                            d = disps['BASC_A'].iloc[0]

                            df = pd.DataFrame(basc)

                            og_bina = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bina)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'BASC_A', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)
                        
                        elif m == 'Onestep':

                            d = disps['onestep'].iloc[0]

                            df = pd.DataFrame(onestep)

                            og_bina = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bina)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'onestep', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                        elif m == 'K-Means':

                            d = disps['k-means'].iloc[0]

                            df = pd.DataFrame(kmeans)

                            og_bin = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bin)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'k-means', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                        else:
                            d = disps['shmulevich'].iloc[0]

                            df = pd.DataFrame(shmulevich)

                            og_bin = df[labels[i]].values

                            binary = "".join(str(x) for x in og_bin)

                            high_p, high_string, p = call_C_statistics(genes[i], d, 'shmulevich', binary)

                            #probDF = probDF.sort_values(by=['prob'])

                            high_probs.append(high_p)
                            strings_probs.append(high_string)

                    max_value = max(high_probs)

                    max_index = high_probs.index(max_value)
                    print("ended elected stats")
                    highest = strings_probs[max_index]
                    
                else:
                    print("shmulevich stats")
                    d = disps['shmulevich'].iloc[0]

                    df = pd.DataFrame(shmulevich)

                    og_binarization = df[labels[i]].values

                    binary = "".join(str(x) for x in og_binarization)

                    high_p, high_string, p = call_C_statistics(genes[i], d, 'shmulevich', binary)

                    #probDF = probDF.sort_values(by=['prob'])

                    highest = high_string

                array_high_P = []

                for j in range(len(og_binarization)):

                    if og_binarization[j] == '?' and highest[j] != '?':
                        array_high_P.append(int(highest[j]))
                    #elif str(og_binarization[j]) != highest[j]:
                    #    array_high_P.append('?')
                    else:
                        array_high_P.append(og_binarization[j])

                # get probability of strings 
                #Z = probabilistic(np.array(genes[i]), [method], d)

                # highest string probability 
                #string_high_P = max(Z, key=Z.get)
                
                # save string key to array
                #array_high_P = [e for e in string_high_P]

                # save highest prob string to each gene 
                string_dict[labels[i]] = array_high_P

            #print(string_dict)

            # turn to imputation to dataframe
            df = pd.DataFrame(string_dict)
            
            # returns imputation to a selected table 
            if(method == 'BASC A'):
                result[0] = df.to_dict('records')
            
        
            elif(method == 'K-Means'):
                result[1] = df.to_dict('records')
        
            
            elif(method == 'Onestep'):
                result[3] = df.to_dict('records')

            elif method == 'Elected':
                result[4] = df.to_dict('records')

            else:
                result[2] = df.to_dict('records')
            
            return tuple(result)

                #bin_array = bin_strings[labels[i]].tolist()

                #bin_s = ""

                #for e in bin_array:

                #    bin_s += str(e)
                


                #high_P = Z[string_high_P]
                
    
    #### Callback - imputates selected table using Other imputation method
    @app.callback(
        Output('Elected-table-dropdown', 'data', allow_duplicate=True),
        Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
        Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
        Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
        Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
        Output('other-impu-button', 'n_clicks'),

        Input('other-impu-button', 'n_clicks'),
        Input('imputate-method', 'value'),
        State('Elected-table', 'data'),
        State('BASC A-table', 'data'),
        State('K-Means-table', 'data'),
        State('Shmulevich-table', 'data'),
        State('Onestep-table', 'data'),

        prevent_initial_call=True)
    def imputate_based_other(n_clicks, method, elected, basc, kmeans, shmule, onestep):
        """
            imputate_based_other - imputates selected table using other method

            n_clicks: pressed button
            method: table to imputate
            elected: elected data
            basc: basc data
            kmeans: kmeans data
            shule: shmulevich data
            onestep: onestep data
        """
        
        # return none if Inputs are empty 
        if n_clicks is None or method == [] or method is None or method == []:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, None
        
        # result output 
        result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None]

        # if button is clicked imoutate
        if n_clicks != None:
            
            # imputate based on selected method (table)
            if(method == 'Elected'):
                
                # imputate using missforest
                result[0] = imputate_mice_logictic(elected)
            
            
            if(method == 'BASC A'):
                result[1] = imputate_mice_logictic(basc)
            
        
            elif(method == 'K-Means'):
                result[2] = imputate_mice_logictic(kmeans)
        
            
            elif(method == 'Onestep'):
                result[4] = imputate_mice_logictic(onestep)
                
            else:
                result[3] = imputate_mice_logictic(shmule)
            
            # returns changes (output)
            return tuple(result)


    #### Callback - imputates selected table using MissForest
    @app.callback(
        Output('Elected-table-dropdown', 'data', allow_duplicate=True),
        Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
        Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
        Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
        Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
        Output('missforest-button', 'n_clicks'),

        Input('missforest-button', 'n_clicks'),
        Input('imputate-method', 'value'),
        State('Elected-table', 'data'),
        State('BASC A-table', 'data'),
        State('K-Means-table', 'data'),
        State('Shmulevich-table', 'data'),
        State('Onestep-table', 'data'),

        prevent_initial_call=True)
    def imputate_based_missforest(n_clicks, method, elected, basc, kmeans, shmule, onestep):
        """
            imputate_based_missforest - imputates selected table using MissForest

            n_clicks: pressed button
            method: table to imputate
            elected: elected data
            basc: basc data
            kmeans: kmeans data
            shule: shmulevich data
            onestep: onestep data
        """
        
        # return none if Inputs are empty 
        if n_clicks is None or method == [] or method is None or method == []:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, None
        
        # result output 
        result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None]

        # if button is clicked imoutate
        if n_clicks != None:
            
            # imputate based on selected method (table)
            if(method == 'Elected'):
                
                # imputate using missforest
                result[0] = imputate_missforest(elected)
            
            
            if(method == 'BASC A'):
                result[1] = imputate_missforest(basc)
            
        
            elif(method == 'K-Means'):
                result[2] = imputate_missforest(kmeans)
        
            
            elif(method == 'Onestep'):
                result[4] = imputate_missforest(onestep)
                
            else:
                result[3] = imputate_missforest(shmule)
            
            # returns changes (output)
            return tuple(result)


    #### Callback - Outputs the imputated tables based on imputation based by gene
    @app.callback(
        Output('Elected-table-dropdown', 'data', allow_duplicate=True),
        Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
        Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
        Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
        Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
        Output('gene-to-1', 'n_clicks'),
        Output('gene-to-0', 'n_clicks'),
        Input('gene-to-1', 'n_clicks'),
        Input('gene-to-0', 'n_clicks'),
        Input('imputate-option', 'value'),
        Input('imputate-gene', 'value'),
        Input('imputate-method', 'value'),
        State('Elected-table', 'data'),
        State('BASC A-table', 'data'),
        State('K-Means-table', 'data'),
        State('Shmulevich-table', 'data'),
        State('Onestep-table', 'data'),
        prevent_initial_call=True)
    def imputate_gene(n_clicks, n_clicks2, option, genes, method, elected, basc, kmeans, shmulevich, onestep):
        """
            imputate_gene - imputates table based on selected genes 

            n_clicks: button imputate genes to 1s
            n_clicks: button imputate genes to 0s
            option: type of imputation
            genes: genes to be imputated
            method: table to imputate
            elected: elected data
            basc: basc data
            kmeans: kmeans data
            shule: shmulevich data
            onestep: onestep data
        """
        
        # return none if Inputs are empty 
        if n_clicks is None and n_clicks2 is None or option == None or genes == None or genes == []:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None
        
        # get which table will be imputated
        if method == "Elected":
            indx = 0
            data = elected
        
        elif method == "BASC A":
            indx = 1
            data = basc
        
        elif method == "K-Means":
            indx = 2
            data = kmeans

        elif method == "Onestep":
            indx = 4
            data = onestep
        
        else:
            indx = 3
            data = shmulevich
        
        # result array (output)
        result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None]

        # imputate values to 1s if button is clicked
        if n_clicks != None and option == 1:

            # imputate genes as 1s 
            data = imputate_value_gene(data, 1, genes)

            # return imputation result
            result[indx] = data
        
            return tuple(result)
        
        # imputate values to 0s if button is clicked
        elif n_clicks2 != None and option == 1:

            # imputate genes as 0s 
            data = imputate_value_gene(data, 0, genes)

            # return imputation result
            result[indx] = data

            return tuple(result)



    def imputate_value_time(df, value, timeCourse):
        """
            imputate_value_time - imputate values based on selected time course

            df: binary dataset
            value: type of imputation
            timeCourse: time points to imputate
        """

        # read binary dataset
        df = pd.DataFrame(df)

        # iterate time points and imputate
        for time in timeCourse:

            df.iloc[time] = df.iloc[time].replace("?", value)

        # return changes
        return df.to_dict('records')


    #### Callback - imputates values based on time course 
    @app.callback(
        Output('Elected-table-dropdown', 'data', allow_duplicate=True),
        Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
        Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
        Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
        Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
        Output('time-to-1', 'n_clicks'),
        Output('time-to-0', 'n_clicks'),
        Input('time-to-1', 'n_clicks'),
        Input('time-to-0', 'n_clicks'),
        Input('imputate-option', 'value'),
        Input('imputate-time', 'value'),
        Input('imputate-method', 'value'),
        State('Elected-table', 'data'),
        State('BASC A-table', 'data'),
        State('K-Means-table', 'data'),
        State('Shmulevich-table', 'data'),
        State('Onestep-table', 'data'),
        prevent_initial_call=True)
    def imputate_gene(n_clicks, n_clicks2, option, timecourse, method, elected, basc, kmeans, shmulevich, onestep):
        """
            imputate_gene - imputates values based on time course 

            n_clicks: button imputate time courses to 1s
            n_clicks: button imputate time courses to 0s
            option: type of imputation
            timecourse: timecourse to be imputated
            method: table to imputate
            elected: elected data
            basc: basc data
            kmeans: kmeans data
            shmulevich: shmulevich data
            onestep: onestep data
        """

        #print("time imputation")
        
        # return none if Inputs not selected
        if n_clicks is None and n_clicks2 is None or option == None or timecourse == None or timecourse == []:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None
        
        # get which table should be imputated
        if method == "Elected":
            indx = 0
            data = elected
        
        elif method == "BASC A":
            indx = 1
            data = basc
        
        elif method == "K-Means":
            indx = 2
            data = kmeans

        elif method == "Onestep":
            indx = 4
            data = onestep
        
        else:
            indx = 3
            data = shmulevich
        
        # result output variable
        result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None]

        # if button is click imputate values to 1s
        if n_clicks != None and option == 2:

            # imputate values
            data = imputate_value_time(data, 1, timecourse)

            # return changes
            result[indx] = data
        
            return tuple(result)
        
         # if button is click imputate values to 0s
        elif n_clicks2 != None and option == 2:

            # imputate values
            data = imputate_value_time(data, 0, timecourse)

            # return changes
            result[indx] = data

            return tuple(result)
