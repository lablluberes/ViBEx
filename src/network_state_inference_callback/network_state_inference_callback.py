##############################################
#
# This file contains the callback components for Network, State Tables, and Inference
#
##############################################
from dash import dcc, html, Input, Output, ClientsideFunction, dash_table, State
import dash
import pandas as pd
import numpy as np
import time
import dash_bootstrap_components as dbc


from networks.networks import create_boolean_network, create_boolean_network_votes
from networks.network_graphs import create_boolean_network_graph, create_boolean_network_graph_votes, create_GRN_plot
from networks.network_rule import createNetwork

from inference_methods.logicgep import LogicGep
from inference_methods.mibni.Mibni import Mibni
from inference_methods.bestfit.BinInfer import run_code
from inference_methods.bestfit_mod import run_bestfit

from networks.hamming import hamming_state_by_state, hamming_chain, generate_init_final_comparison, extract_path
from networks.metrics import Metrics, dynamic_accuracy, Metrics_directed

# read displacement csv
displacements = pd.read_csv("./displacements/Displacements.csv")

# function to return components 
def get_network_inf_callbacks(app):

    #### Callback - generates network based on rules (Upload Boolean Functions tab)
    @app.callback(Output('generate-network-rules', 'children'),
              Input('rule_network_dict', 'data'),
              Input('inferred_net_rules', 'data'),
              prevent_initial_call=True)
    def generate_net_rules(rules, inferred_rules):
        """
            generate_net_rules - generates network based on rules (Upload Boolean Functions tab)

            rules: uploaded rules
            inferred_rules: rules inferred 
        """

        # return nothing if rules are not uploaded
        if rules == {} or rules is None:
            return None
        
        # read uploaded rules
        df = pd.DataFrame(rules)

        # create network plot of uploaded rules 
        net, dict_net = createNetwork(df)
        
        grn_network_uploaded = create_GRN_plot(df)
        
        #print(inferred_rules)

        #print(dict_net)

        # if Boolean Network has more than 1,000 nodes dont display network
        if len(net.nodes) > 2500:
            return html.Div([

                            html.Div(style={"height": "20px"}),
                            # rules displayed
                            dbc.Card(
                                dbc.CardBody([
                                        html.B("Table of Uploaded Boolean Functions"),
                                        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="stored-rules"),
                                        html.Br(),
                                    ]),
                            className="mb-3"),

                            html.P("Cannot display Boolean Network because it has too many nodes"),

                            # metrics for performance of infer rules and uploaded rules
                            output_metrics(rules, inferred_rules),
                           
                            
                            html.Div([

                                    dbc.Card(
                                        dbc.CardBody([
                                                html.Div([
                                                html.B("Uploaded Boolean Functions Gene Regulatory Network"),
                                            
                                                html.Iframe(
                                                                srcDoc=grn_network_uploaded.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                                width="500px",
                                                                height="500px"
                                                ),
                                            
                                            ], style={'display': 'flex', 'flexDirection': 'column'}),
                                            ]),
                                    className="mb-3"),
                                    
                              

                        ], style={'display': 'flex', 'flexDirection': 'row', 'overflowY': 'auto'}),
                    
                        ], style={'display': 'flex', 'flexDirection': 'column'})

        # return network tab components this includes network plots and metrics 
        return  html.Div([

                            html.Div(style={"height": "20px"}),
                            # rules displayed
                            dbc.Card(
                                dbc.CardBody([
                                        html.B("Table of Uploaded Boolean Functions"),
                                        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="stored-rules"),
                                        html.Br(),
                                    ]),
                            className="mb-3"),
                            
                            # perform metrics for inferred rules and uploaded rules
                            output_metrics(rules, inferred_rules),
                            
                            html.Div([

                                        dbc.Card(
                                            dbc.CardBody([
                                                    html.Div([
                                                    html.B("Uploaded Boolean Functions Gene Regulatory Network"),
                                                
                                                    html.Iframe(
                                                                    srcDoc=grn_network_uploaded.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                                    width="500px",
                                                                    height="500px"
                                                    ),
                                                
                                                ], style={'display': 'flex', 'flexDirection': 'column'}),
                                                ]),
                                        className="mb-3"),
                                        
                                        show_inferred_grn(inferred_rules)

                            ], style={'display': 'flex', 'flexDirection': 'row'}),

                       

                            # display Uploaded rules Boolean Network
                            html.Div([

                                dbc.Card(
                                    dbc.CardBody([
                                            html.Div([
                                            html.P('Grey nodes are the attractors in the Boolean Network.'),
                                            html.B("Network Based on Uploaded Boolean Functions"),
                                            html.Iframe(
                                                            srcDoc=net.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                            width="500px",
                                                            height="500px"
                                            ),
                                        ], style={'display': 'flex', 'flexDirection': 'column'}),
                                        ]),
                                className="mb-3"),


                                # show inferred Boolean Network 
                                show_inferred_network(inferred_rules)

                            ], style={'display': 'flex', 'flexDirection': 'row'}),

                            # perform metrics for inferred rules and uploaded rules
                            #output_metrics(inferred_rules, rules),
                       
                    
                        ], style={'display': 'flex', 'flexDirection': 'column'})
    

     #### Callback - Generates a dropdown to select which binarization to use to infer BN
    @app.callback(
        Output('generate-state-dropdown', 'children'),
        Input('dropdown-method', 'value'),
        prevent_initial_call=True)
    def generate_dropdown(methods):
        """
            generate_dropdown - creates dropdown to select which binarization to infer BN

            methods: selected thr methods 
        """

        # if no methods selected return empty dropdown
        if methods == [] or methods == None:

            return html.B("Select the binarization method to infer the network:"), dcc.Dropdown(
                        [],
                        placeholder="Select method binarization to use",
                        id="dropdown-state-table-select",
                        multi=False,
                        searchable=False)
        
        else:
            
            # returns dropdown of which binarization to use 
            return html.B("Select the binarization method to infer the network:"), dcc.Dropdown(
                        methods+['Elected'],
                        placeholder="Select method binarization to use",
                        id="dropdown-state-table-select",
                        multi=False,
                        searchable=False),
        

    def show_inferred_network(net_rules):
        """
            show_inferred_network - function returns BN of inferred rules 

            net_rules: inferred boolean functions
        """

        # return nothing if rules are not available
        if net_rules == {} or net_rules is None:
            return None
        
        # read inferred rules
        df_infer_rules = pd.DataFrame(net_rules)

        # generate network of inferred rules
        net, dict_net = createNetwork(df_infer_rules)
        
        # create component with network 
        comp = dbc.Card(
                    dbc.CardBody([
                            html.Div([
                            html.P('Grey nodes are the attractors in the Boolean Network.'),
                            html.B("Network Based on Inferred Boolean Functions"),
                            html.Iframe(
                                    srcDoc=net.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                    width="500px",
                                    height="500px"
                            ),
                        ], style={'display': 'flex', 'flexDirection': 'column'}),
                    ]),
            className="mb-3")

        # return component
        return comp
    
    def show_inferred_grn(net_rules):
        
        if net_rules == {} or net_rules is None:
            return None
        
        df = pd.DataFrame(net_rules)
     
        result = create_GRN_plot(df)
        
        comp = dbc.Card(
                    dbc.CardBody([
                                html.Div([
                                    html.B("Inferred Boolean Functions Gene Regulatory Network"),
                                            
                                    html.Iframe(
                                        srcDoc=result.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                        width="500px",
                                        height="500px"
                                    ),
                                            
                                ], style={'display': 'flex', 'flexDirection': 'column'}),
                    ]),
                className="mb-3")
        
        return comp

    def get_inferred_network_dict(net_rules):
        """
            get_inferred_network_dict - returns inferred network as dictionary example: {0000: 1111, ...}

            net_rules: rules of inferred network
        """

        # return nothing if no input
        if net_rules == {} or net_rules is None:
            return None
        
        # read rules
        df_infer_rules = pd.DataFrame(net_rules)

        # generate dictionary
        _, dict_net = createNetwork(df_infer_rules)

        #print("aqui", dict_net)

        # return dictionary
        return dict_net


    def output_metrics(uploaded, inferred):
        """
            output_metrics - performance metrics of inferred rules and uploaded rules

            inferred: inferred rules
            uploaded: uploaded rules
        """

        # if no input return None
        if inferred == {} or inferred is None or uploaded is None or uploaded == {}:
            return None
        
        # if both rules dont have same number of rules send message
        if len(inferred) != len(uploaded):
            return "To be able to show performance metrics of both inferred and uploaded Boolean Functions they need to have the same number of rules."
        
        # read inferred rules
        df_infer_rules = pd.DataFrame(inferred)

        # read uploaded rules
        df_uploaded_rules = pd.DataFrame(uploaded)

        # get metrics evaluation of rules
        metrics = Metrics(df_uploaded_rules, df_infer_rules)
        #metrics_dir = Metrics_directed(df_uploaded_rules, df_infer_rules)
        metrics = pd.DataFrame(metrics)
        #metrics_dir = pd.DataFrame(metrics_dir)

        # return table with metrics evaluation
        return html.Div([
            
            dbc.Card(
                        dbc.CardBody([
                            html.P("The next section shows a metrics table comparing the performance of the inferred Boolean Functions with the Ground Truth Functions."),
                            html.P("(This was done turning the Boolean Function into undirected matrices.)"),
                            dash_table.DataTable(metrics.to_dict('records'), [{"name": str(i), "id": str(i)} for i in metrics.columns])
                    ]),
            className="mb-3"),

            #dbc.Card(
            #            dbc.CardBody([
            #                html.P("The next section shows a metrics table comparing the performance of the inferred Boolean Functions with the Ground Truth Functions."),
            #                html.P("(This was done turning the Boolean Function into directed matrices.)"),
            #                dash_table.DataTable(metrics_dir.to_dict('records'), [{"name": str(i), "id": str(i)} for i in metrics_dir.columns])
            #        ]),
            #className="mb-3")
            
            ])

    def turn_df_to_array(df):
        """
            turn_df_to_array - turns a data of binrization into an array

            df: dataframe of binarization
        """

        array_net = []

        # read data
        df = pd.DataFrame(df)

        # iterate df rows and join them and save on array
        for index, row in df.iterrows():
            r = row.values
            
            result = ''.join(map(str, r))
            
            array_net.append(result)

        return array_net

    def state_transition_table(df, method):
        """
            state_transition_table - returns a table representing binarizations of a thr method. 

            df: data binarized
            method: thr method used to binarize 
        """

        # returns table component. Table allows dropdown on each field to change values to 1s, 0s, or ?
        return html.Div(
            
            style={'padding': 5, 'display':'flex', 'flexDirection':'column', 'textAlign':'center'},
            children=[

            # save in storage the original table
            dcc.Store(id=f"{method}-data", data=df.to_dict('records')),
            html.B(method +" Binarization States"),

            # table allows colors depending on value green 1s, red 0s, and yellow ?
            dash_table.DataTable(
                        id=method+'-table-dropdown',
                        data=df.to_dict('records'),
                        columns=[
                        
                        {'id': col, 'name': col, 'presentation': 'dropdown'} for col in df.columns
                        ],
                        editable=True,
                        dropdown={
                            col:{
                                'options':[
                                    {'label': '1', 'value': 1},
                                    {'label': '0', 'value': 0},
                                    {'label': '?', 'value': '?'}
                                ]
                            }
                            for col in df.columns
                        },
                        style_data = {'borderBottom': '5px solid white'},
                        style_table={'maxHeight': '500px', 'overflowY': 'auto', 'maxWidth': '500px', 'overflowY': 'auto'},
                        style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{{{col}}} = "?"'.format(col=col),
                                        'column_id': col,
                                        'row_index': 'odd'
                                    },
                                        'backgroundColor': 'rgb(255, 255, 192, 0.3)',
                                } for col in df.columns
                                ] +
                                [
                                {
                                    'if': {
                                        'filter_query': '{{{col}}} = "?"'.format(col=col),
                                        'column_id': col,
                                        'row_index': 'even'
                                    },
                                    'backgroundColor': 'rgb(255, 255, 192, 0.3)',
                                } for col in df.columns
                                ] +
                                
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 1'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'odd'
                                        },
                                    'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                                    } for col in df.columns
                                ] +
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 0'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'odd'
                                        },
                                        'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                                    } for col in df.columns
                                ] +
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 0'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'even'
                                        },
                                        'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                                    } for col in df.columns
                                ] +
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 1'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'even'
                                        },
                                        'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                                    } for col in df.columns
                                ] + [
                                {
                                    'if': {
                                    'column_id': 'Hamming',
                                        },
                                        'backgroundColor': 'white',
                                }],
                    )
        ])


    def state_transition_table2(df):
        """
            state_transition_table2 - returns a table representing binarizations. Used for extracted path

            df: data binarized
        """

        # return table with data
        return dash_table.DataTable(
                        id='table-dropdown',
                        data=df.to_dict('records'),
                        columns=[
                        
                        {'id': col, 'name': col} for col in df.columns
                        ],
                        style_data = {'borderBottom': '5px solid white'},
                        style_table={'maxHeight': '500px', 'overflowY': 'auto', 'maxWidth': '500px', 'overflowY': 'auto'},
                        style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{{{col}}} = "?"'.format(col=col),
                                        'column_id': col,
                                        'row_index': 'odd'
                                    },
                                        'backgroundColor': 'rgb(255, 255, 192, 0.3)',
                                } for col in df.columns
                                ] +
                                [
                                {
                                    'if': {
                                        'filter_query': '{{{col}}} = "?"'.format(col=col),
                                        'column_id': col,
                                        'row_index': 'even'
                                    },
                                    'backgroundColor': 'rgb(255, 255, 192, 0.3)',
                                } for col in df.columns
                                ] +
                                
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 1'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'odd'
                                        },
                                    'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                                    } for col in df.columns
                                ] +
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 0'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'odd'
                                        },
                                        'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                                    } for col in df.columns
                                ] +
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 0'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'even'
                                        },
                                        'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                                    } for col in df.columns
                                ] +
                                [
                                    {
                                        'if': {
                                            'filter_query': '{{{col}}} = 1'.format(col=col),
                                            'column_id': col,
                                            'row_index': 'even'
                                        },
                                        'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                                    } for col in df.columns
                                ] + [
                                {
                                    'if': {
                                    'column_id': 'Hamming',
                                        },
                                        'backgroundColor': 'white',
                                }],
                    )


    def verify_thr_is_in_dict2(genes, methods, thr_k, thr_b, thr_o, thr_s):
        """
            verify_thr_is_in_dict2 - verifies that thr are saved based on selected methods, and genes

            genes: selected genes
            methods: selected methods
            thr_k: threshold kmeans
            thr_b: threshold basca
            thr_o: threshold onestep
            thr_s: threshold shmulevich
        """

        # iterate over selected genes and methods to verify thr computation was finished
        for gene in genes:
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

    #### Callback - Ouputs the state table transitions of the binarizations by each method
    @app.callback(
        Output('network-state-table-output', 'children'),
        Input('dropdown-method', 'value'), 
        Input('datatable-interactivity','data'),
        Input('datatable-interactivity', 'selected_rows'),
        Input('thr_k','data'),
        Input('thr_o','data'),
        Input('thr_s','data'),
        Input('thr_b', 'data'), 
        prevent_initial_call=True)
    def nets_state_tables(selected_method, data, selected_rows, thr_k, thr_o, thr_s, thr_b):
        """
            nets_state_tables - Ouputs the state table transitions of the binarizations by each method

            selected_methods: thr methods selected
            data: dataset of genes
            selected_rows: selected genes
            thr_k: threshold kmeans
            thr_b: threshold basca
            thr_o: threshold onestep
            thr_s: threshold shmulevich
        """

        # if these values are none return none to the dashboard
        if selected_method is None or selected_method == []:
            return None
        if data is None or data == []:
            return None
        if selected_rows is None or selected_rows == []:
            return None
        
        # verify thr have been computed for selected genes 
        cond = verify_thr_is_in_dict2(selected_rows, selected_method, thr_k, thr_b, thr_o, thr_s)

        # if not computed then wait 
        if cond:
            return None
        
        # sort selected genes
        selected_rows.sort()

        # read gene expression dataset
        df = pd.DataFrame(data)

        # extract gene names 
        labels = df['Gene ID']
        df = df.loc[:, df.columns!='Gene ID']

        #get elected state table (binarization)
        elected_state_network = create_boolean_network_votes(selected_rows, df, selected_method, displacements, thr_k, thr_o, thr_s, thr_b, labels)

        transition = []

        # iterate for each selected thr method
        for method in selected_method:
            
            # get the methods state table (binarization)
            network = create_boolean_network(selected_rows, method, df, displacements, thr_k, thr_o, thr_s, thr_b, labels)

            # append state table to component 
            transition.append(
                html.Div(children = [
                    html.Div(style={"height": "20px"}),
                    dbc.Card(
                            dbc.CardBody([
                                state_transition_table(network, method)
                            ]),
                        className="mb-3")
                    ], style={"marginRight": "20px"})
                )

        # if more than two methods were selected organize in grid 
        if len(selected_method) > 2:
    
            transition_df = html.Div([html.Div(transition[:2]), html.Div(transition[2:])], style={'display': 'flex', 'flexDirection': 'row'})

        else:
            transition_df = html.Div(transition[:2])

        # component of elected transition table
        final_transition_df = html.Div(children = [
                    html.Div(style={"height": "20px"}),
                    dbc.Card(
                            dbc.CardBody([
                                state_transition_table(elected_state_network, "Elected")
                            ]),
                        className="mb-3")
                    ], style={"marginRight": "20px"})
        
        # get the methods no selected (to prevent callback error)
        all_methods = list(set(['BASC A', 'K-Means', 'Shmulevich', 'Onestep']) - set(selected_method))

        components_tables = []

        # create empty tables for not selected methods (to prevent error callback)
        for m in all_methods:
            components_tables.append(dash_table.DataTable(
                        id=f'{m}-table-dropdown',
                        columns=[
                            {'name': 'Gene', 'id': 'gene'},
                            {'name': 'Value', 'id': 'value'}
                        ],
                        data=[], style_table={'display': 'none'}),)

        # return components
        return  html.Div(children = [transition_df, final_transition_df], style={'display': 'flex', 'flexDirection': 'row'}), html.Div(components_tables)

    #### Callback - generates Boolean network path based on binarization
    @app.callback(
        Output("generate-networks", 'children'),
        Input('Elected-table', 'data'),
        Input('K-Means-table', 'data'),
        Input('Shmulevich-table', 'data'),
        Input('BASC A-table', 'data'),
        Input('Onestep-table', 'data'),
        Input('dropdown-method', 'value'),
        Input('datatable-interactivity', 'selected_rows'),
        prevent_initial_call=True)
    def generate_networks(elected, kmeans, shmulevich, basca, onestep, methods, rows):
        """
            generate_networks - generates Boolean network path based on binarization

            elected: elected binarization
            kmeans: kmeans binarization
            shmulevich: shmulevich binarization
            basca: basca binarization
            onestep: onestep binarization
            methods: selected thr methods
            rows: selected genes from table
        """

        # return message if no methods or genes selected
        if methods == [] or methods == None:
            return "Select threshold methods to show Boolean Network."
        if rows == [] or rows == None:
            return "Select genes from table to show Boolean Network."

        network_plots = []

        # sort selected genes
        rows.sort()

        #print(kmeans)

        # iterate over selected methods and generate plot 
        for method in methods:
            
            # convert binarizations to dataframe
            if method == "BASC A":
                data = pd.DataFrame(basca)
            elif method == 'K-Means':
                data = pd.DataFrame(kmeans) 
            elif method == 'Onestep':
                data = pd.DataFrame(onestep)
            elif method == 'Shmulevich':
                data = pd.DataFrame(shmulevich)
            

            # create a plot of the binarization 
            fig2, _, legend = create_boolean_network_graph(data)

            #transition.append(transition_table(network, method))

            # append edges were there are more than 2 iterations. its for a legend 
            legend_comps = []
            for a in legend:
                comp = html.P(f"{str(a)} = {str(legend[a])}")
                legend_comps.append(comp)

            # if there are letters in edges add information that is a legend 
            if legend_comps != []:

                legend_comps.insert(0, html.P("Letters are for edges where there are many loops"))

            # creates components for current plot of network
            network_plots.append(
                        html.Div(
                                children=[

                                        dbc.Card(
                                            dbc.CardBody([
                                                html.B(f"Network of {method} States Binarization", style={'textAlign': 'center'}),
                                                html.Div(legend_comps),
                                                html.Iframe(
                                                    srcDoc=fig2.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                    width="500px", height="500px",
                                                )
                                            ], style={'display': 'flex', 'flexDirection': 'column'}),
                                            className="mb-3",
                                        ),
                                
                                    ], style={'display': 'flex', 'flexDirection': 'column', "marginRight": "20px"}

                                )
                )

        # make plots in a grid if more than 2 methods selected
        if len(methods) > 2:
    
            network_plots = html.Div([html.Div(network_plots[:2]), html.Div(network_plots[2:])], style={'display': 'flex', 'flexDirection': 'row'})
        

        else:

            network_plots = html.Div([html.Div(network_plots)], style={'display': 'flex', 'flexDirection': 'row'})


        # create plot of elected binarizations
        fig, _, legend_votes = create_boolean_network_graph_votes(elected)

        # add legend based on elected edges with letters
        legend_comps_vote = []
        for a in legend_votes:
                comp = html.P(f"{str(a)} = {str(legend_votes[a])}")
                legend_comps_vote.append(comp)

        # add information about the letters 
        if legend_comps_vote != []:

                legend_comps_vote.insert(0, html.P("Letters are for edges where there are many loops"))

        geneNames = pd.DataFrame(elected).columns

        geneString = []

        for i in range(len(geneNames)):

            geneString.append(html.P(f"{i+1} = {geneNames[i]}"))


        # returns all plots and components 
        return    html.Div([
                                html.Div(style={"height": "20px"}),
                                dbc.Card(
                                    dbc.CardBody([
                                        html.P("This section provides the Boolean Network of the Binarization by each selected method and elected method."),
                                        html.P("Each number in the edges are the time series steps until the final state. The table representation of these networks are in 'Binarization State Table',"),
                                    ]),
                                    className="mb-3",
                                ),
                                #dbc.Card(
                                #    dbc.CardBody(
                                #        geneString
                                #    ),
                                #    className="mb-3",
                                #),
                                
                                #html.Div(id='graph_rules', src=fig2, style={'height':'100%', 'width':'100%'}),
                                html.Div(network_plots),

                                html.Div([

                                    dbc.Card(
                                            dbc.CardBody([
                                                html.Div([
                                        
                                                    html.B('Network of Elected States Binarization', style={'textAlign': 'center'}),
                                                    html.Div(legend_comps_vote),
                                                    html.Iframe(
                                                            srcDoc=fig.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                            width="500px", height="500px"),
                                                    
                                                ], style={'display': 'flex', 'flexDirection': 'column'}),
                                            ], style={'display': 'flex', 'flexDirection': 'column'}),
                                            className="mb-3",
                                    ),

                                    html.Div([
                                        html.Div(id='generate-network-dict')
                                    ], style={'display': 'flex', 'flexDirection': 'column'})
                                ], style={'display': 'flex', 'flexDirection': 'row'})
                                
                                
                    ], style={'display': 'flex', 'flexDirection': 'column'})


    #### Callback - generates hamming analysis tab based on uploaded functions and binarizations 
    @app.callback(
        Output('analysis-output', 'children'),
        Input('dropdown-method', 'value'), 
        Input('BASC A-table', 'data'),
        Input('K-Means-table', 'data'),
        Input('Onestep-table', 'data'),
        Input('Shmulevich-table', 'data'),
        Input('rule_network_dict', 'data'),
        Input('Elected-table', 'data'),
        prevent_initial_call=True)   
    def generate_analysis(methods, basc, kmeans, onestep, shmulevich, rule_network, elected_network):
        """
            generate_analysis - generates hamming analysis tab based on uploaded functions and binarizations 
            
            methods: selected thr methods
            elected_network: elected binarization
            kmeans: kmeans binarization
            shmulevich: shmulevich binarization
            basca: basca binarization
            onestep: onestep binarization
            rule_network: network based on uploaded rules
            
            
        """
        
        #print(rule_network)

        # send message that functions need to be uploaded to be able to analyze them
        if methods is None or methods == [] or rule_network == {} or rule_network is None:
            return "Upload transition rules to see network analysis or selected genes or methods"
        
        
        # if uploaded functions dont have the same number of genes as the binarizations (selected genes) then send message
        if len(elected_network[0]) != len(rule_network):
            return "The amount of genes need to be the same for the Uploaded Boolean Functions, and selected genes."


        df = pd.DataFrame()

        data_algos = pd.DataFrame()
        
        # read uploaded rules
        rule_network = pd.DataFrame(rule_network)

        # get network of all possible states based on rules 
        _, rule_network = createNetwork(rule_network)

        # iterate chosen methods 
        for method in methods:
            
            # for each selected method do Hamming state by state analysis
            if method == "BASC A":

                # turn dataframe into a array
                data = turn_df_to_array(basc)

                # get hamming state by state of basc and uploaded functions (this extracts a path from uploaded functions based on first state of basc)
                df_analysis = hamming_state_by_state(rule_network, data, method)

                # add basc data to dataframe
                df_bin = pd.DataFrame({method:data})

                # add Hamming state by state analysis
                data_algos = pd.concat([data_algos, df_bin], axis=1)

            elif method == 'K-Means':
                # turn dataframe into a array
                data = turn_df_to_array(kmeans) 
               
                # get hamming state by state of kmeans and uploaded functions (this extracts a path from uploaded functions based on first state of kmeans)
                df_analysis = hamming_state_by_state(rule_network, data, method)

                # add kmeans data to dataframe
                df_bin = pd.DataFrame({method:data})

                # add Hamming state by state analysis
                data_algos = pd.concat([data_algos, df_bin], axis=1)

            elif method == 'Onestep':
                # turn dataframe into a array
                data = turn_df_to_array(onestep)

                # get hamming state by state of onestep and uploaded functions (this extracts a path from uploaded functions based on first state of onestep)
                df_analysis = hamming_state_by_state(rule_network, data, method)

                # add onestep data to dataframe
                df_bin = pd.DataFrame({method:data})

                # add Hamming state by state analysis
                data_algos = pd.concat([data_algos, df_bin], axis=1)

            elif method == 'Shmulevich':
                # turn dataframe into a array
                data = turn_df_to_array(shmulevich)

                # get hamming state by state of shmulevich and uploaded functions (this extracts a path from uploaded functions based on first state of shmulevich)
                df_analysis = hamming_state_by_state(rule_network, data, method)

                # add shmulevich data to dataframe
                df_bin = pd.DataFrame({method:data})

                # add Hamming state by state analysis
                data_algos = pd.concat([data_algos, df_bin], axis=1)

            # concadanate analysis in one table 
            df = pd.concat([df, df_analysis], axis=1)
        
        # get a dataframe with the elected binarization path
        df_bin = pd.DataFrame({'Elected':turn_df_to_array(elected_network)})

        # concadenate dataframes
        data_algos = pd.concat([data_algos, df_bin], axis=1)
        
        # Generate a initial final analysis comparison using Hamming of the uploaded functions and methods binarizations
        df_init_final = generate_init_final_comparison(data_algos, rule_network)

        # based on uploaded functions, and elected binarization create a Hamming chain analysis
        df_chain_elected, cond = hamming_chain(rule_network, turn_df_to_array(elected_network))

        # initial state has undecided values so chain analysis cant be done
        if cond == False:

            chain_hamming = html.P("Cannot analyze network because initial state does not exist in Boolean Function Network")

        # create chain analysis table 
        else:
            
            chain_hamming = dash_table.DataTable(df_chain_elected.to_dict('records'), [{"name": i, "id": i} for i in df_chain_elected.columns], style_table={'overflowY': 'auto'})


        # return analysis as tables in ViBEx
        return [

            dbc.Card(
                dbc.CardBody([
                    html.P("The following table analyzes the state by state transition based on the Boolen Functions chain."),
                    html.B("State by State Analysis"),
                    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], style_table={'overflowY': 'auto'}),
                ]),
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody([
                    html.P("The next table analyses the elected binarization path to the one extracted from the Boolean Functions."),
                    html.B("Chain Analysis"),
                    chain_hamming,
                ]),
                className="mb-3",
            ),

            dbc.Card(
                dbc.CardBody([
                    html.P("The followng analysis compares the initial and final states of each binarization methods with the ones from the Boolean Functions."),
                    html.P("In addition, the number of different values in the intermediate states are given."),
                    html.P("Furthermore, a similarity and transition match scores are given."),
                    html.B("Initial and Final State Analysis"),
                    dash_table.DataTable(df_init_final.to_dict('records'), [{"name": i, "id": i} for i in df_init_final.columns], style_table={'overflowY': 'auto'})
                ]),
                className="mb-3",
            )]


    def states_in_graph(net, path, n):
        """
            states_in_graph - colors yellow the extracted states from the uploaded BN

            net: uploaded network
            path: path generated
            n: length of path
        """

        #for state in path:

        for node in net.nodes:

            if node['label'] in path:
                node['color']= 'yellow'

        return net

    #### Callback - generates BN inference, and outputs plots 
    @app.callback(
        Output('inference_plots', 'children'),
        Output('btn_inference', 'n_clicks'),
        Input('btn_inference', 'n_clicks'),
        Input('datatable-interactivity','data'), 
        Input('datatable-interactivity', 'selected_rows'),
        Input('Elected-table', 'data'),
        Input('K-Means-table', 'data'),
        Input('Shmulevich-table', 'data'),
        Input('BASC A-table', 'data'),
        Input('Onestep-table', 'data'),
        Input('dropdown-method', 'value'),
        Input('inference-method', 'value'),
        Input('dropdown-state-table-select', 'value'),
        prevent_initial_call=True,
    )
    def inference(n_clicks, data, selected_rows, elected_binarizations, kmeans_binarizations, 
                shmulevich_binarizations, basca_binarizations, onestep_binarizations, 
                methods, inference_method, bin_method):
        """
            inference - generates BN inference, and outputs plots 

            n_clicks: button to infer network
            data: gene expr dataset 
            selected_rows: genes selected
            elected_binarizations: elected binarization
            kmeans_binarizations: kmeans binarization
            shmulevich_binarizations: shmulevich binarization
            basca_binarizations: basc binarization
            onestep_binarizations: onestep binarization
            methods: thr method selected
            inference_method: inference method selected
            bin_method: binarization table to use to infer BN
        """
        # if button not pressed return none
        if n_clicks is None:
            return [None, dcc.Store(id='inferred_net_rules', data={}), ], None
        
        # sort selected genes
        selected_rows.sort()
        
        # if no thr and inference methods selected show message or None
        if inference_method is None or inference_method == []:
            return None, None
        if methods is None or methods == []:
            return "Select a threshold method to infer rules.", None
        
        # if no binarization selected show message
        if bin_method is None or bin_method == []:
            return "Select a binarization method to infer the network.", None
        
        # get a dataframe based on the selected binarization used to inference 
        if bin_method == "Elected":
            bin_dict = elected_binarizations
            df_binary = pd.DataFrame(elected_binarizations)

        elif bin_method == "BASC A":
            bin_dict = basca_binarizations
            df_binary = pd.DataFrame(basca_binarizations)

        elif bin_method == "Onestep":
            bin_dict = onestep_binarizations
            df_binary = pd.DataFrame(onestep_binarizations)

        elif bin_method == "K-Means":
            bin_dict = kmeans_binarizations
            df_binary = pd.DataFrame(kmeans_binarizations)

        else:
            bin_dict = shmulevich_binarizations
            df_binary = pd.DataFrame(shmulevich_binarizations)
        
        # make sure binarization selected has no undecided state
        if (df_binary == '?').any().any():
            return f"Make sure that the state table of {bin_method} has no '?' values.", None
        
        dict_data = {}

        # read gene exp
        df_data = pd.DataFrame(data)

        # get labels of genes
        labels = df_data['Gene ID']

        df_data = df_data.loc[:, df_data.columns!='Gene ID']

        # get selected genes from dataset
        for row in selected_rows:
            dict_data[labels[row]] = df_data.iloc[row]

        df_data = pd.DataFrame(dict_data)

        #print(df_data)
        #print(df_binary)

        # make sure dataset is numeric
        df_data = df_data.apply(pd.to_numeric)
        df_binary = df_binary.apply(pd.to_numeric)

        # make sure indexes are ints
        df_data.index = df_data.index.astype(int)
        df_binary.index = df_binary.index.astype(int)

        start_time = time.time()

        # logic for selected inference method
        if inference_method == "LogicGep":
            
            # infer rules using LogicGep
            df_infer_rules = LogicGep(df_binary, df_data)

        elif inference_method == 'MIBNI':
            
            # infer rules using Mibni
            mibni = Mibni(10, df_binary, "dynamics.tsv")
            result = mibni.run()

            # save infered boolean functions in dataframe
            rules_infered = {'Gene':[],
                            'Rule':[]}
            for r in result:

                rul = r.split(" = ")
                rules_infered['Gene'].append(rul[0])
                rules_infered['Rule'].append(rul[1])

            df_infer_rules = pd.DataFrame(rules_infered)
            
        else:
            # infer rules using Bestfit
            result, expr = run_bestfit(df_binary.T, len(list(df_binary.columns)))
            
            #print(len(list(df_binary.columns)))
            #print(df_binary)
            
            #print(result)
            
            if len(result) != len(list(df_binary.columns)):
                result = None
                
            # if result is None means bestfit was not able to infer all rules. show message
            if result is None:

                return html.P("Best fit was not able to infer all Boolean Functions. Try again, user other binarizations or imputate different values."), None

            # save rules
            data = {'Gene': [], 'Rule': []}
            
            data['Rule'] = expr
            data['Gene'] = list(df_binary.columns)
            
            df_infer_rules = pd.DataFrame(data)

        end_time = time.time()

        #print(df_infer_rules)

        print(f"{inference_method} time taken: {end_time-start_time}")

        # create network based on inferred rules
        net, dict_net = createNetwork(df_infer_rules)

        #print(dict_net)

        # get first state of binarization
        state = df_binary.iloc[0].values
        state = ''.join(str(s) for s in state)

        # extract path from infered BN based on first state
        path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)
        
        
        grn_network = create_GRN_plot(df_infer_rules)

        #print(path, df_binary)

        df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

        if df_dyn_acc == None:
            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
        else:
            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

        # if network has more than 1000 nodes then dont show BN graph
        if len(net.nodes) > 2500:

            return html.Div([
                # save inferred rules 
                dcc.Store(id='inferred_net_rules', data=df_infer_rules.to_dict('records')), 
                dbc.Card(
                        dbc.CardBody([
                                html.B("Table of Inferred Boolean Functions"),
                                dash_table.DataTable(df_infer_rules.to_dict('records'), [{"name": i, "id": i} for i in df_infer_rules.columns]),
                                html.Br(),
                            ]),
                className="mb-3"),
                
                html.Div([

                            dbc.Card(
                                dbc.CardBody([
                                        html.Div([
                                        html.B("Inferred Gene Regulatory Network"),
                                    
                                        html.Iframe(
                                                        srcDoc=grn_network.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                        width="500px",
                                                        height="500px"
                                        ),
                                    
                                    ], style={'display': 'flex', 'flexDirection': 'column'}),
                                    ]),
                            className="mb-3"),

                ], style={'display': 'flex', 'flexDirection': 'row', 'overflowY': 'auto'}),

                html.P("Cannot display Boolean Network because it has too many nodes"),

                dbc.Card(
                        dbc.CardBody([
                            html.P("The next section shows the dynamic accuracy table comparing the performance of the original binarization and the extracted path based on the inferred rules."),
                            html.P("The next tables show both paths taken and which are used for calculating dynamic accuracy."),
                            dash_table.DataTable(df_dyn_acc.to_dict('records'), [{"name": str(i), "id": str(i)} for i in df_dyn_acc.columns], style_cell={'textAlign': 'left'})
                    ]),className="mb-3",  style={"maxWidth": "400px"}),

                dbc.Card(
                    dbc.CardBody([
                        html.P("The first table is the extracted binary path based on first state of second table."),
                        html.P("The second table is the binarization path by the selected threshold method."),
                        html.Div([
                            
                            html.Div([ 
                                html.B("Binary Path State Table based on First State of "+bin_method),
                                state_transition_table2(pd.DataFrame(path))
                            ], style={'display':'flex', 'flexDirection': 'column', 'marginRight':'20px'}),

                            html.Div([ 
                                html.B("Binarization Using " +bin_method),
                                state_transition_table2(df_binary)
                            ], style={'display':'flex', 'flexDirection': 'column'})

                            ], style={'display':'flex', 'flexDirection': 'row'})
                    ]),
                    className="mb-3"),
        
        ], style={'display': 'flex', 'flexDirection': 'column'}), None
        
        # returns the components of the inference tab
        return  html.Div([

                # save inferred rules
                dcc.Store(id='inferred_net_rules', data=df_infer_rules.to_dict('records')), 
                dbc.Card(
                        dbc.CardBody([
                                html.B("Table of Inferred Boolean Functions"),
                                dash_table.DataTable(df_infer_rules.to_dict('records'), [{"name": i, "id": i} for i in df_infer_rules.columns]),
                                html.Br(),
                            ]),
                className="mb-3"),
                
                html.Div([

                            dbc.Card(
                                dbc.CardBody([
                                        html.Div([
                                        html.B("Inferred Gene Regulatory Network"),
                                    
                                        html.Iframe(
                                                        srcDoc=grn_network.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                        width="500px",
                                                        height="500px"
                                        ),
                                    
                                    ], style={'display': 'flex', 'flexDirection': 'column'}),
                                    ]), style={'justify-content': 'center'},
                            className="mb-3"),

                #], style={'display': 'flex', 'flexDirection': 'row', 'overflowY': 'auto'}),

                #html.Div([

                            dbc.Card(
                                dbc.CardBody([
                                        html.Div([
                                        html.B("Network Based on Inferred Boolean Functions"),
                                        html.P("Grey nodes are attractors, and green nodes are"),
                                        html.P("the extracted path based on first state of the selected method"),
                                    
                                        html.Iframe(
                                                        srcDoc=net.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                        width="500px",
                                                        height="500px"
                                        ),
                                    
                                    ], style={'display': 'flex', 'flexDirection': 'column'}),
                                    ]),
                            className="mb-3"),

                ], style={'display': 'flex', 'flexDirection': 'row', 'overflowY': 'auto'}),

                dbc.Card(
                        dbc.CardBody([
                            html.P("The next section shows the dynamic accuracy table comparing the performance of the original binarization and the extracted path based on the inferred rules."),
                            html.P("The next tables show both paths taken and which are used for calculating dynamic accuracy."),
                            dash_table.DataTable(df_dyn_acc.to_dict('records'), [{"name": str(i), "id": str(i)} for i in df_dyn_acc.columns], style_cell={'textAlign': 'left'})
                    ]),className="mb-3",  style={"maxWidth": "400px"}),

                dbc.Card(
                    dbc.CardBody([
                        html.P("The first table is the extracted binary path based on first state of second table."),
                        html.P("The second table is the binarization path by the selected threshold method."),
                        html.Div([
                            
                            html.Div([ 
                                html.B("Binary Path State Table based on First State of "+bin_method),
                                state_transition_table2(pd.DataFrame(path))
                            ], style={'display':'flex', 'flexDirection': 'column', 'marginRight':'20px'}),

                            html.Div([ 
                                html.B("Binarization Using " +bin_method),
                                state_transition_table2(df_binary)
                            ], style={'display':'flex', 'flexDirection': 'column'})

                            ], style={'display':'flex', 'flexDirection': 'row'})
                    ]),
                    className="mb-3"),
        
        ], style={'display': 'flex', 'flexDirection': 'column'}), None

    #### Callback - generates network based on uploaded rules
    @app.callback(
        Output('generate-network-dict', 'children'),
        Input('datatable-interactivity', 'selected_rows'),
        Input('dropdown-method', 'value'), 
        Input('datatable-interactivity','data'),
        Input('stored-rules','data'),
        Input('thr_b','data'),
        Input('thr_k','data'),
        Input('thr_s','data'),
        Input('thr_o','data'),
        prevent_initial_call=True)
    def generate_rule_net_dict(rows, methods, data, rules, thr_b, thr_k, thr_s, thr_o):  
        """
            generate_rule_net_dict - generates network based on uploaded rules

            rows: selected genes
            methods: selected thr methods
            data: gene expr dataset
            rules: uploaded rules
            thr_b: basc thrs
            thr_k: kmeans thrs
            thr_s: shmulevich thrs
            thr_o: onestep thrs
        
        """

        # return none if inputs are not provided
        if rows is None and methods is None and data is None and rules is None or methods == [] or rules == [] or rows == []:
            return None 
        
        if rules == {}:
            return None
        
        # sort selected genes
        rows.sort()
        
        #print(rules)
        
        # generate network based on rules
        net, _ = createNetwork(pd.DataFrame(rules)) 

        # if more than 1000 nodes dont show network
        if len(net.nodes)  > 1000:

            return html.P("Cannot generate Boolean Network because its too big.")

        # return output network
        return html.Div([
                        html.B("Network Based on Uploaded Boolean Functions"),
                        html.Iframe(
                            srcDoc=net.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                            width="500px",
                            height="500px"
                        ),
                ], style={'display': 'flex', 'flexDirection': 'column'})

    #### Callback - processess button selected all thr methods 
    @app.callback(
        Output('dropdown-method', 'value'),
        Input('methods-all', 'n_clicks'),
        prevent_initial_call=True
    )
    def select_all_methods(n_clicks):
        """
            select_all_methods - processess button selected all thr methods 

            n_clicks: button pressed
        
        """

        # button not pressed do nothing
        if n_clicks is None:
            return None
        
        # once pressed make dropdown menu select all thr methods
        return ['BASC A', 'K-Means', 'Onestep', 'Shmulevich']

    #### Callback - processess select all and unselect all buttons of gene expresion matrix
    @app.callback(
        Output('datatable-interactivity', 'selected_rows'),
        Output('table-all', 'n_clicks'),
        Output('table-deselect', 'n_clicks'),
        Input('table-all', 'n_clicks'),
        Input('table-deselect', 'n_clicks'),
        Input('datatable-interactivity', 'data'),
        prevent_initial_call=True
    )
    def select_deselect_table(n_clicks, n_clicks2, data):
        """
            select_deselect_table - processess select all and unselect all buttons of gene expresion matrix

            n_clicks: select all button press
            n_clicks2: deselect all button press
            data: gene expr table
        """

        # if no data or buttons not pressed do nothing 
        if data is None:
            return None
        if n_clicks is None and n_clicks2 is None:
            return None
        
        # if select all button is pressed select all genes from table
        if n_clicks != None:
            
            # select all rows
            array = np.arange(0, len(data))

            # return to table all rows selected
            return array, None, None
        
        # if deselect all is pressed then deselect rows
        elif n_clicks2 != None:
            
            return [], None, None
        
    

    #### Callback - Download threshold CSV
    # process the click of the download button
    # gets the threshold of the data and downsloads as a csv
    # Inputs: 
    @app.callback(
        Output("download-metrics-output", "children"),
        Output("download-metrics", "n_clicks"),
        Output("download-metrics-excel", 'data'),

        Input("download-metrics", "n_clicks"),
        Input('datatable-interactivity','data'), 
        Input('datatable-interactivity', 'selected_rows'),
        Input('dropdown-method', 'value'),
        Input('Elected-table', 'data'),
        Input('K-Means-table', 'data'),
        Input('Shmulevich-table', 'data'),
        Input('BASC A-table', 'data'),
        Input('Onestep-table', 'data'),
        Input('rule_network_dict', 'data'),
        prevent_initial_call=True,
    )
    def download_metrics(n_clicks, data, selected_rows, thr_methods, elected, kmeans, shmulevich, basc, onestep, rules_uploaded):
        
        # if no clicks return none 
        if n_clicks is None:
            return None, None, None
        
        # no data return none
        if data is None:
            return "No dataset has been uploaded.", None, None
        
        # no selected rows return None
        if selected_rows == [] or selected_rows is None:

            return "You neet to select genes", None, None
        
        if thr_methods == [] or thr_methods == None:

            return "You need to select threshold methods", None, None
        
        if rules_uploaded == {} or rules_uploaded is None:
            return "Uploaded Boolean Functions needed to perform metrics.", None, None
        
        
        if len(rules_uploaded) != len(selected_rows):

            return "You need to select the same number of genes as the uploaded rules.", None, None


        dict_data = {}

        # read gene exp
        df_data = pd.DataFrame(data)

        # get labels of genes
        labels = df_data['Gene ID']

        df_data = df_data.loc[:, df_data.columns!='Gene ID']

        # get selected genes from dataset
        for row in selected_rows:
            dict_data[labels[row]] = df_data.iloc[row]

        df_data = pd.DataFrame(dict_data)

        #print(df_data)
        #print(df_binary)

        # make sure dataset is numeric
        df_data = df_data.apply(pd.to_numeric)

        # make sure indexes are ints
        df_data.index = df_data.index.astype(int)

        thr_methods += ['Elected']

        metrics_data = []
        
        inference_methods = ['MIBNI', 'LogicGep', 'Bestfit']
        #= {
        #    'MIBNI':[], 'LogicGep':[], 'Bestfit':[]
        #}

        for m in inference_methods:

            for m_thr in thr_methods:

                print(f"runnng {m} on {m_thr}")

                # get a dataframe based on the selected binarization used to inference 
                if m_thr == "Elected":
                    print(m_thr)
                    bin_dict = elected
                    df_binary = pd.DataFrame(elected)

                elif m_thr == "BASC A":
                    print(m_thr)
                    bin_dict = basc
                    df_binary = pd.DataFrame(basc)

                elif m_thr == "Onestep":
                    print(m_thr)
                    bin_dict = onestep
                    df_binary = pd.DataFrame(onestep)

                elif m_thr == "K-Means":
                    print(m_thr)
                    bin_dict = kmeans
                    df_binary = pd.DataFrame(kmeans)

                else:
                    print(m_thr)
                    bin_dict = shmulevich
                    df_binary = pd.DataFrame(shmulevich)
                
                # make sure binarization selected has no undecided state
                if (df_binary == '?').any().any():
                    string = f"{m_thr} binarization has '?' values cannot download metrics. Either eliminate that binarization or remove '?' values."

                    return string, None, None

                df_binary = df_binary.apply(pd.to_numeric)
                df_binary.index = df_binary.index.astype(int)

                # logic for selected inference method
                if m == "LogicGep":
                    print(m)
                    # infer rules using LogicGep

                    dyn_arr = []
                    acc_arr = []
                    pre_arr = []
                    re_arr = []
                    fscore_arr = []

                    for i in range(15):
                        df_infer_rules = LogicGep(df_binary, df_data)

                        # create network based on inferred rules
                        net, dict_net = createNetwork(df_infer_rules)

                        # get first state of binarization
                        state = df_binary.iloc[0].values
                        state = ''.join(str(s) for s in state)

                        # extract path from infered BN based on first state
                        path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                        print("get dyn and metrics")
                        df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

                        if df_dyn_acc == None:
                            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                        
                        else:
                            df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                        metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)
                        #metrics_dir = Metrics_directed(pd.DataFrame(rules_uploaded), df_infer_rules)

                        metric_dict = {}

                        metric_dict['Method'] = m

                        metric_dict['Binarization'] = m_thr

                        metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                            

                        for metr in metrics:
                            metric_dict[metr] = metrics[metr][0]

                        #for metr in metrics_dir:
                        #    metric_dict[metr+'(Directed Matrix)'] = metrics_dir[metr][0]

                        if metric_dict['Dynamic Accuracy'] != 'Cannot be calculated':
                      
                            dyn_arr.append(metric_dict['Dynamic Accuracy'])

                        acc_arr.append(metric_dict['Accuracy'])
                        pre_arr.append(metric_dict['Precision'])
                        re_arr.append(metric_dict['Recall'])
                        fscore_arr.append(metric_dict['F1-Score'])

                        metrics_data.append(metric_dict)
                    
                    mean_dyn = np.mean(dyn_arr)
                    mean_acc = np.mean(acc_arr)
                    mean_pre = np.mean(pre_arr)
                    mean_re = np.mean(re_arr)
                    mean_f= np.mean(fscore_arr)

                    std_dyn = np.std(dyn_arr, ddof=1)
                    std_acc = np.std(acc_arr, ddof=1)
                    std_pre = np.std(pre_arr, ddof=1)
                    std_re = np.std(re_arr, ddof=1)
                    std_f= np.std(fscore_arr, ddof=1)

                    se_dyn = std_dyn / np.sqrt(len(dyn_arr))
                    se_acc = std_acc / np.sqrt(len(acc_arr))
                    se_pre = std_pre / np.sqrt(len(pre_arr))
                    se_re = std_re / np.sqrt(len(re_arr))
                    se_f= std_f / np.sqrt(len(fscore_arr))

                    mean_row = {'Method': m, 'Binarization':m_thr, 
                                'Dynamic Accuracy': f"Mean: {round(mean_dyn, 2)} STD: {round(std_dyn, 3)} SE: {round(se_dyn, 3)}",
                                'Accuracy': f"Mean: {round(mean_acc, 2)} STD: {round(std_acc, 3)} SE: {round(se_acc, 3)}",
                                'Precision': f"Mean: {round(mean_pre, 2)} STD: {round(std_pre, 3)} SE: {round(se_pre, 3)}",
                                'Recall': f"Mean: {round(mean_re, 2)} STD: {round(std_re, 3)} SE: {round(se_re, 3)}",
                                'F1-Score': f"Mean: {round(mean_f, 2)} STD: {round(std_f, 3)} SE: {round(se_f, 3)}"} 
                    metrics_data.append(mean_row)


                elif m == 'MIBNI':
                    print(m)
                    # infer rules using Mibni
                    mibni = Mibni(10, df_binary, "dynamics.tsv")
                    result = mibni.run()

                    # save infered boolean functions in dataframe
                    rules_infered = {'Gene':[],
                                    'Rule':[]}
                    for r in result:

                        rul = r.split(" = ")
                        rules_infered['Gene'].append(rul[0])
                        rules_infered['Rule'].append(rul[1])

                    df_infer_rules = pd.DataFrame(rules_infered)
                    
                else:
                    print(m)
                    # infer rules using Bestfit
                    result, expr = run_bestfit(df_binary.T, len(list(df_binary.columns)))
                    
                    # save rules
                    data = {'Gene': [], 'Rule': []}
                    
                    data['Rule'] = expr
                    data['Gene'] = list(df_binary.columns)
                    
                    df_infer_rules = pd.DataFrame(data)
                
                if m != "LogicGep":
                    # create network based on inferred rules
                    net, dict_net = createNetwork(df_infer_rules)

                    # get first state of binarization
                    state = df_binary.iloc[0].values
                    state = ''.join(str(s) for s in state)

                    # extract path from infered BN based on first state
                    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

                    print("get dyn and metrics")
                    df_dyn_acc = dynamic_accuracy(pd.DataFrame(path), df_binary)

                    if df_dyn_acc == None:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': ['Cannot be calculated']})
                    
                    else:
                        df_dyn_acc = pd.DataFrame({'Dynamic Accuracy': [df_dyn_acc]})

                    metrics = Metrics(pd.DataFrame(rules_uploaded), df_infer_rules)
                    #metrics_dir = Metrics_directed(pd.DataFrame(rules_uploaded), df_infer_rules)

                    metric_dict = {}

                    metric_dict['Method'] = m

                    metric_dict['Binarization'] = m_thr

                    metric_dict['Dynamic Accuracy'] = list(df_dyn_acc['Dynamic Accuracy'].values)[0]
                        

                    for metr in metrics:
                        metric_dict[metr] = metrics[metr][0]

                    #for metr in metrics_dir:
                    #    metric_dict[metr+'(Directed Matrix)'] = metrics_dir[metr][0]


                    metrics_data.append(metric_dict)
        
        
        #return None
        #print(metrics_data)
        metrics_df = pd.DataFrame(metrics_data)

        return "Metrics completed. File has been downloaded.", None, dcc.send_data_frame(metrics_df.to_csv, "metrics_vibex.csv")
    