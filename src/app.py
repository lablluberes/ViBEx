import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output, ClientsideFunction
from dash import dcc, html, Input, Output, ClientsideFunction, dash_table, State
import numpy as np
import pandas as pd
import seaborn as sns
import datetime
import pathlib
import io
import base64
import dash_bootstrap_components as dbc
import math
from collections import OrderedDict
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#pretty charts!
import altair as alt
import dash_vega_components as dvc

from normalize import geneNorm 
from interpolation import interpolation
from methods import call_C_BASC, BASC_A, call_C_Stepminer, onestep, K_Means, shmulevich
from voting_algos import election_strings
from displacementMatrixes import getDisplacement

from networks import create_boolean_network, create_boolean_network_votes
from network_graphs import create_boolean_network_graph, create_boolean_network_graph_votes
from network_rule import createNetwork

from logicgep import LogicGep
from mibni.Mibni import Mibni
from bestfit.BinInfer import run_code
from bitarray import bitarray
from metrics import Metrics, Metrics_BN

from hamming import hamming_state_by_state, hamming_chain, generate_init_final_comparison, extract_path

from ProbabilityPerm import probBin

from stringProbabilistic import probabilistic
from imputation_ml import imputate_missforest

displacements = pd.read_csv("Displacements.csv")
standard_dev = pd.read_csv("standard_dev.csv")

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ]
)
app.title = "ViBEx: A Visualization Tool for Gene Expression Analysis"

server = app.server
app.config.suppress_callback_exceptions = True


def turn_df_to_array(df):

    array_net = []

    df = pd.DataFrame(df)

    for index, row in df.iterrows():
        r = row.values
        
        result = ''.join(map(str, r))
        
        array_net.append(result)

    return array_net

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("ViBEx"),
            html.H3("Welcome to ViBEx"),
            html.Div(
                id="intro",
                children=[html.H5('A Visualization Tool for Gene Expression Analysis', style={'textAlign': 'center'}), "ViBEx is a tool for the analysis and exploration of gene expression binarization. Upload a dataset of gene expression and select one, many or all out of four methods for the computation of a threshold for binarization. Visualize Boolean networks of resulting states.",
                          html.P("This tool only accepts CSV files. The files need to be formated in the next manner. The first column are the genes names (they need to be strings). The rest of the columns need to be the gene expressions of the corresponding genes. The dataset cannot have header names, only a matrix of gene expression with first column as gene names."),
                          html.P("Dataset will be preprocessed to convert data to [0,1] interval")],
            ),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Selected File:')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),

        ],
    )

def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Br(),
            html.P("Select threshold computation methods:"),
            html.Button('Select all', id='methods-all'),
            dcc.Dropdown(
                ['BASC A', 'K-Means', 'Onestep', 'Shmulevich'],
                placeholder="Select binarization method",
                id="dropdown-method",
                multi=True,
                #persistence = True,
                #persistence_type = 'memory',
                searchable=False),
            
            html.Br(),
            html.B('Download the threshold of the selected rows to a csv:'), 
            html.Button("Download CSV", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
            html.Br(),

            dcc.Store(id='thr_k', data={}), 
            dcc.Store(id='thr_o', data={}),
            dcc.Store(id='thr_b', data={}), 
            dcc.Store(id='thr_s', data=None),
            dcc.Store(id='spline-genes', data={}),
            dcc.Store(id='Elected-table', data={}),
            dcc.Store(id='K-Means-table', data={}),
            dcc.Store(id='Shmulevich-table', data={}),
            dcc.Store(id='BASC A-table', data={}),
            dcc.Store(id='Onestep-table', data={}),
            dcc.Store(id='rule_network_dict', data={}),
            dcc.Store(id='stored-rules', data={}),
            dcc.Store(id='inferred_net_rules', data={}),

            dcc.Store(id='Elected-data', data={}),
            dcc.Store(id='K-Means-data', data={}),
            dcc.Store(id='Shmulevich-data', data={}),
            dcc.Store(id='BASC A-data', data={}),
            dcc.Store(id='Onestep-data', data={}),

            hidden_buttons()
            
        ],
        
    )

def hidden_buttons():

    return html.Div([html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),
           html.Button('Reset Imputations', id='reset-imputation', style={'display': 'none'}),

            html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
            html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
            html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
            html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
            
        
            dcc.Dropdown(
                    [],
                    placeholder="Select method binarization to use",
                    id="dropdown-state-table-select",
                    multi=False,
                    searchable=False, style={'display':'none'}),

            dcc.Dropdown(
                            [],
                            placeholder="Select method table",
                            id="imputate-method",
                            multi=False,
                            searchable=False, style={'display':'none'}),
            
            dcc.Dropdown(
                            options=[{'label': 'Global Imputation (ex: changes all "?" to either 0 or 1)', 'value':0},
                             {'label': 'Gene Imputation (ex: imputates a value for only one gene)', 'value':1},
                             {'label': 'Time Impuation (ex: imputates values based on time course)', 'value':2},
                             {'label': 'Framework Statistics Algorithm', 'value':3}],
                            placeholder="Select option",
                            id="imputate-option",
                            multi=False,
                            searchable=False, style={'display':'none'}),
            
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
                style={'display': 'none'})])

# process the click of the download button
# gets the threshold of the data and downsloads as a csv
@app.callback(
    Output("download-dataframe-csv", "data"),
    Output("btn_csv", "n_clicks"),
    Input("btn_csv", "n_clicks"),
    Input('datatable-interactivity','data'), 
    Input('datatable-interactivity', 'selected_rows'),
    prevent_initial_call=True,
)
def download_csv(n_clicks, data, selected_rows):
    # no data return none
    if data is None:
        return None, None
    
    if selected_rows == [] or selected_rows is None:

        return None, None
    
      # if no clicks return none 
    if n_clicks is None:
        return None, None
    
    # get data
    df = pd.DataFrame(data)
    labels = df['Gene ID']
    df = df.loc[:, df.columns!='Gene ID']
    
    selected_rows.sort()
    
    # get the selected genes values
    genes = df.iloc[selected_rows].values
    labels = labels.iloc[selected_rows].values
    rows = df.shape[0]
    
    # column names and creating dataframe
    col_names = {'Gene ID':[],'basc_thr':[], 'kmeans_thr':[], 'onestep_thr':[], 'shmulevich_thr':[]}
    final_df = pd.DataFrame(col_names)

    #print(genes, labels)
    # get threshold of selected rows and save to dataframe
    for i in range(len(selected_rows)):
            k_means = K_Means(genes[i])
            basc_a = BASC_A(genes[i])
            one_step = onestep(genes[i])
            shmulevich_ = shmulevich(genes[i])

            label = labels[i]
            
            new_row = {'Gene ID':label, 'basc_thr':basc_a, 'kmeans_thr':k_means, 'onestep_thr':one_step, 'shmulevich_thr': shmulevich_}
            final_df.loc[len(final_df)] = new_row

    # send the dataframe and download it as thr.csv
    return dcc.send_data_frame(final_df.to_csv, "thr.csv"), None

@app.callback(
    Output('BASC A-table', 'data'),
    Input('BASC A-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_basc(data):

    if data == None or data == [] or data == {}:
        return {}
        
    return data

@app.callback(
    Output('K-Means-table', 'data'),
    Input('K-Means-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_kmeans(data):

    if data == None or data == [] or data == {}:
        return {}
        
    return data

@app.callback(
    Output('Onestep-table', 'data'),
    Input('Onestep-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_onestep(data):

    if data == None or data == [] or data == {}:
        return {}
        
    return data

@app.callback(
    Output('Shmulevich-table', 'data'),
    Input('Shmulevich-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_shmulevich(data):

    if data == None or data == [] or data == {}:
        return {}
        
    return data

@app.callback(
    Output('Elected-table', 'data'),
    Input('Elected-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_elected(data):

    if data == None or data == [] or data == {}:
        return {}
    
    #print(data)
        
    return data

def network_nav():
    
    return dcc.Tabs([

        dcc.Tab(label='Binarization State Table', children=[

            dash_table.DataTable(
                    id='Elected-table-dropdown',
                    columns=[
                        {'name': 'Gene', 'id': 'gene'},
                        {'name': 'Value', 'id': 'value'}
                    ],
                    data=[], style_table={'display': 'none'}),

            dash_table.DataTable(
                    id='BASC A-table-dropdown',
                    columns=[
                        {'name': 'Gene', 'id': 'gene'},
                        {'name': 'Value', 'id': 'value'}
                    ],
                    data=[], style_table={'display': 'none'}),

            dash_table.DataTable(
                    id='K-Means-table-dropdown',
                    columns=[
                        {'name': 'Gene', 'id': 'gene'},
                        {'name': 'Value', 'id': 'value'}
                    ],
                    data=[], style_table={'display': 'none'}),
    
            dash_table.DataTable(
                    id='Onestep-table-dropdown',
                    columns=[
                        {'name': 'Gene', 'id': 'gene'},
                        {'name': 'Value', 'id': 'value'}
                    ],
                    data=[], style_table={'display': 'none'}),

            dash_table.DataTable(
                    id='Shmulevich-table-dropdown',
                    columns=[
                        {'name': 'Gene', 'id': 'gene'},
                        {'name': 'Value', 'id': 'value'}
                    ],
                    data=[], style_table={'display': 'none'}),

            html.Div(style={"height": "20px"}),
            dbc.Card(
                    dbc.CardBody([
                        html.P("This section includes the Binarization State tables based on each selected threshold method and elected methodlogy."),
                        html.P("Each row are a different binarized time course state of the original gene expression."),
                        html.P("The next dropdown allows the imputation of values on undecided states."),
                        html.P("There are three options of imputation values: Global imputation, gene imputation, and time course based imputation."),
                        html.P("This can also be done by the arrow dropdown in each field of each table."),
                    ]),
                className="mb-3",
            ),

            html.Div(style={"height": "20px"}),
            dbc.Card(
                    dbc.CardBody([
                        html.Div(id="imputate-dropdowns"),
                    ]),
                className="mb-3",
            ),

            html.Div(id='network-state-table-output'),

        ]),

        dcc.Tab(label='Binarization Path Network', children=[
            html.Div(id="generate-networks")
        ]),

        dcc.Tab(label='Inference Boolean Network', children=[

            html.Div([
                
                html.Div(style={"height": "20px"}),
                dbc.Card(
                        dbc.CardBody([
                            html.P("This tab allows to infer the Boolean Functions of the set of selected genes."),
                            html.P("The Boolean Network based on the Boolean Functions infered are drawn."),
                            html.P("First, selected the inference method from a dropdown these are: Bestfit, LogicGep, and MIBNI."),
                            html.P("In addition, selected which binarization to use (based on Binarization state tables). Make sure that the table in the 'Binarization State Tab' have no '?' values."),
                        ]),
                    className="mb-3"),

                html.Div(style={"height": "20px"}),
                dbc.Card(
                        dbc.CardBody([
                            html.Div([
                                html.B('Select an inference method to infer Boolean Functions and Network:'),
                                    dcc.Dropdown(
                                        ['MIBNI', 'LogicGep', 'Bestfit'],
                                        placeholder="Select inference method",
                                        id="inference-method",
                                        multi=False,
                                        searchable=False),
                                    html.Div(id='generate-state-dropdown'),
                            ], style={"width": "33%", 'marginTop': '20px', 'marginBottom': '20px'}),
                            html.Button("Infer Boolean Network and Functions", id="btn_inference"),
                            html.Br(),
                        ]),
                    className="mb-3"),
               
                html.Div(id='inference_plots')

            ])

        ]),

        dcc.Tab(label='Upload Boolean Functions', children=[

            html.Div(children = [
                
                html.Div(style={"height": "20px"}),
                dbc.Card(
                    dbc.CardBody([
                            html.P("This tab provides the ability to upload a Boolean Function file representing a GRN."),
                            html.P("The file needs to be a CSV with two columns: Gene (gene names), Rule (corresponding boolean function). The rules need to be Python style boolean expressions."),
                            html.P("This means using 'and', 'or', 'not', '^'(xor)."),
                            html.P("In addition, selecting a binarization method from the dropdown will create a comparison table of the path taken based on the first state of the binarization."),
                            html.P("Upload transition rules to create network"),
                        ]),
                className="mb-3"),

                dcc.Upload(
                    id='upload-rules',
                    children=html.Button("Upload Rules"),
                    multiple=False,
                ),

                html.Div(style={"height": "20px"}),
                
                html.Div(id='output-rules-upload'),
              
                html.Div(id='generate-network-rules')
               
                                
            ])

        ]),

        dcc.Tab(label='Analysis', children=[
                        
            html.Div(id='analysis-output')

        ]),
    ])

@app.callback(
    Output('generate-state-dropdown', 'children'),
    Input('dropdown-method', 'value'),
    prevent_initial_call=True)
def generate_dropdown(methods):

    if methods == [] or methods == None:

        return html.B("Select the binarization method to infer the network:"), dcc.Dropdown(
                    [],
                    placeholder="Select method binarization to use",
                    id="dropdown-state-table-select",
                    multi=False,
                    searchable=False)
    
    else:

        return html.B("Select the binarization method to infer the network:"), dcc.Dropdown(
                    methods+['Elected'],
                    placeholder="Select method binarization to use",
                    id="dropdown-state-table-select",
                    multi=False,
                    searchable=False),


def tabs_nav():

    return dcc.Tabs([
                dcc.Tab(label='Binarization', children=[
                    html.Div(style={"height": "20px"}),
                    dbc.Card(
                        dbc.CardBody([html.Div(id="binarization-output")]),
                        className="mb-3",
                    ),
                    
                ]),
                 dcc.Tab(label='Displacements', children=[
                    html.Div(id='displacements-output')
                ]),
                dcc.Tab(label='Statistics', children=[

                    dcc.Loading(
                       children=[html.Div(id='statistics-output')],
                    type="circle"),
                
                ]),
                dcc.Tab(label='Networks', children=[
                    network_nav()
                ]),
            ])

app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        #html.Div(
        #    id="banner",
        #    className="banner",
        #    children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        #),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), html.Div(id = 'output-data-upload')],
            style={'overflowY': 'auto', 'maxHeight': '500px'}
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[

                html.Div(id='app-content-tabs')
                
            ], style={'overflowX': 'auto', 'maxHeight': '500px'}
        )
    ],
)

@app.callback(
        Output('app-content-tabs', 'children'),
        Input('upload-data', 'contents'),
        prevent_initial_call=False
)
def content_tabs(data):

    #print("fuera if")
    if data is None or data == {}:
        #print("dentro if")
        carousel = dbc.Carousel(
            items=[
                {"key": "1", "src": "/assets/table.png"},
                {"key": "2", "src": "/assets/thr.png"},
                {"key": "3", "src": "/assets/bn.png"},
                {"key": "4", "src": "/assets/inference.png"},
            ],
            controls=False,
            indicators=False,
            interval=2000,
            #className="carousel-fade",
            #ride="carousel",
            style={'width':'90%', 'margin':'auto'}
        )

        return html.Div(
                        carousel, 
                        style={
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'center',    
                            'paddingTop': '5vh',   
                        })
    
    return html.Div(id='dropdown-gene-select', children=[
                    dcc.Dropdown(
                        id="dropdown-gene",
                        options=[],  # Initially empty
                        value=None,
                        placeholder="Select gene"
                    )
                ]), dcc.Loading(
                    children=[html.Div(id='process-tabs-thr')],
                    type="circle",
                ), tabs_nav()
                #html.Div(id='process-tabs-thr'),
                

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df_labels = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), header=None)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df_labels = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # normalize each row of the dataframe based on this formula x' = (x-min)/(max-min) and save it to the dataframe

    df_t = geneNorm(df_labels.loc[ : , df_labels.columns!=0].copy())
    #df_t = df_t.round(5)

    #print(df)

    df_t.insert(0, 'Gene ID', df_labels[0])

    return html.Div(
        id='process-data',
        children=[

            html.H5(filename),
            html.Button('Select all', id='table-all'),
            html.Button('Deselect all', id='table-deselect'),
            dash_table.DataTable(
                            id='datatable-interactivity',
                            columns=[
                               {"name": str(i), "id": str(i), "type": "numeric", "format": dash_table.Format.Format(precision=4)}
                                if df_t[i].dtype in [np.float64, np.float32, float] else
                                {"name": str(i), "id": str(i)}
                                for i in df_t.columns
                            ],
                            data=df_t.to_dict('records'),
                            column_selectable="single",
                            row_selectable="multi",
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            style_table={'overflowX': 'auto', 'maxWidth': '500px'},
                            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
            ),
            generate_control_card()
        ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True)
def update_output(list_of_contents, list_of_names, list_of_dates):
    list_of_contents = [list_of_contents]
    list_of_names = [list_of_names]
    list_of_dates = [list_of_dates]

    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    


# function to parse the contents of thje selected file
def parse_contents_rules(contents, filename, date):
    content_type, content_string = contents.split(',')

    # decode the content
    decoded = base64.b64decode(content_string)
    
    # if it is a csv then read it 
    if 'csv' in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=0)

        return dcc.Store(id='rule_network_dict', data=df.to_dict('records'))
    
    else:
        return "The file needs to be a csv."
    

@app.callback(Output('generate-network-rules', 'children'),
              Input('rule_network_dict', 'data'),
              Input('inferred_net_rules', 'data'),
              prevent_initial_call=True)
def generate_net_rules(rules, inferred_rules):
    if rules == {} or rules is None:
        return None
    
    df = pd.DataFrame(rules)

    net, dict_net = createNetwork(df)

    #print(dict_net)

    if len(net.nodes) > 1000:
        return html.Div([

                        html.Div(style={"height": "20px"}),
                        dbc.Card(
                            dbc.CardBody([
                                    html.B("Table of Uploaded Boolean Functions"),
                                    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="stored-rules"),
                                    html.Br(),
                                ]),
                        className="mb-3"),

                        html.P("Cannot display Boolean Network because it has too many nodes"),

                        output_metrics(inferred_rules, rules),
                        #output_metricsBN(dict_net, get_inferred_network_dict(inferred_rules))
                
                    ], style={'display': 'flex', 'flexDirection': 'column'})

    return  html.Div([

                        html.Div(style={"height": "20px"}),
                        dbc.Card(
                            dbc.CardBody([
                                    html.B("Table of Uploaded Boolean Functions"),
                                    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], id="stored-rules"),
                                    html.Br(),
                                ]),
                        className="mb-3"),

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

                            show_inferred_network(inferred_rules)

                        ], style={'display': 'flex', 'flexDirection': 'row'}),

                        output_metrics(inferred_rules, rules),
                        #output_metricsBN(dict_net, get_inferred_network_dict(inferred_rules))
                
                    ], style={'display': 'flex', 'flexDirection': 'column'})
    

def show_inferred_network(net_rules):

    if net_rules == {} or net_rules is None:
        return None
    
    df_infer_rules = pd.DataFrame(net_rules)

    net, dict_net = createNetwork(df_infer_rules)

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

    
    return comp

def get_inferred_network_dict(net_rules):

    if net_rules == {} or net_rules is None:
        return None
    
    df_infer_rules = pd.DataFrame(net_rules)

    _, dict_net = createNetwork(df_infer_rules)

    #print("aqui", dict_net)

    return dict_net


def output_metrics(net_rules, rules):

    if net_rules == {} or net_rules is None or rules is None or rules == {}:
        return None
    
    df_infer_rules = pd.DataFrame(net_rules)
    df_uploaded_rules = pd.DataFrame(rules)

    metrics = Metrics(df_uploaded_rules, df_infer_rules)

    metrics = pd.DataFrame(metrics)

    return dbc.Card(
                    dbc.CardBody([
                        html.P("The next section shows a metrics table comparing the performance of the inferred Boolean Functions with the Ground Truth Functions."),
                        dash_table.DataTable(metrics.to_dict('records'), [{"name": str(i), "id": str(i)} for i in metrics.columns])
                ]),
        className="mb-3")

def output_metricsBN(dict_net, dict_inferred):

    if dict_net is None or dict_inferred is None:
        return None
    
    metrics = Metrics_BN(dict_net, dict_inferred)

    metrics = pd.DataFrame(metrics)

    return dbc.Card(
                    dbc.CardBody([
                        html.P("The next section shows a metrics table comparing the performance of the inferred Boolean Network with the Ground Truth Boolean Network."),
                        dash_table.DataTable(metrics.to_dict('records'), [{"name": str(i), "id": str(i)} for i in metrics.columns])
                ]),
        className="mb-3")
        

@app.callback(Output('output-rules-upload', 'children'),
              Input('upload-rules', 'contents'),
              State('upload-rules', 'filename'),
              State('upload-rules', 'last_modified'),
              prevent_initial_call=True)
# function parses and update the output of the selected dataset
def update_output_rules(list_of_contents, list_of_names, list_of_dates):
    list_of_contents = [list_of_contents]
    list_of_names = [list_of_names]
    list_of_dates = [list_of_dates]

    # if there is a selected file
    if list_of_contents is not None:
        # parse the content
        children = [
            parse_contents_rules(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(Output('dropdown-gene-select', 'children'),
              Input('datatable-interactivity', 'selected_rows'),
              Input('datatable-interactivity', 'data'),
              prevent_initial_call=True)
def dropdown_gene_select(rows, data):
    if rows == [] or data == None or rows == None:
         return html.Div(style={"height": "20px"}), dbc.Card(
                        dbc.CardBody([html.B('Select gene to visualize and binarize:'), dcc.Dropdown(
                            options=[], 
                            value = None,
                            placeholder="Select gene",
                            id="dropdown-gene")]),
                        className="mb-3",
                    ),
    
    df1 = pd.DataFrame(data)
    labels = df1['Gene ID']

    rows.sort()
    
    return html.Div(style={"height": "20px"}), dbc.Card(
            dbc.CardBody([html.B('Select gene to visualize and binarize:'), dcc.Dropdown(
                    options=[{'label': labels[row], 'value': row} for row in rows], 
                    value = rows[0],
                    persistence = True,
                    persistence_type = 'memory',
                    placeholder="Select gene",
                    id="dropdown-gene")]),
                className="mb-3",
            ),


@app.callback(Output('process-tabs-thr', 'children'),
              Input('datatable-interactivity', 'selected_rows'),
              Input('datatable-interactivity', 'data'),
              Input('dropdown-method', 'value'),
              prevent_initial_call=True)
def process_thr(selected_rows, data, selected_method):

    if selected_method is None or selected_rows is None or data is None:
        return "Select genes, methods or upload dataset."

    df1 = pd.DataFrame(data)
    df1 = df1.loc[:, df1.columns!='Gene ID']

    thr_k = {}
    thr_b = {}
    thr_o = {}
    thr_s = {}

    splineDict = {}

    selected_rows.sort()

    for row in selected_rows:
        selected = df1.iloc[row]

        gene = selected.values

        splineGene = interpolation(gene)

        splineDict[row] = splineGene


    for method in selected_method:

        for row in selected_rows:

            splineGene = splineDict[row]

            if(method == 'BASC A'):
                thr = call_C_BASC(splineGene.copy())

                thr_b[row] = thr

            elif(method == 'Onestep'):
                thr = call_C_Stepminer(splineGene)

                thr_o[row] = thr

            elif(method == 'Shmulevich'):
                thr = shmulevich(splineGene)

                thr_s[row] = thr

            elif(method == 'K-Means'):
                thr = K_Means(splineGene)

                thr_k[row] = thr
    
    return html.Div(
            children=[
                dcc.Store(id='thr_k', data=thr_k), 
                dcc.Store(id='thr_o', data=thr_o),
                dcc.Store(id='thr_b', data=thr_b), 
                dcc.Store(id='thr_s', data=thr_s),
                dcc.Store(id='spline-genes', data=splineDict), 
            ])

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

def make_grid_disp(methods, gene, data, thr_k, thr_o, thr_s, thr_b, disps):
    
    #methods = ['BASC A', 'K-Means', 'Onestep']
    
    fig = make_subplots(rows=2, cols=2, subplot_titles=["Displacement of " + m for m in methods])
    
    y = list(data[gene].values())
    label = y[-1]
    y.pop(-1)
    
    row = 1
    col = 1
    
    legend = True

    fillcolor = ['#dae5ef', '#ffdddd', '#ddf5dd', '#ffe7d2']
    
    
    for i in range(len(methods)):
        
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
        
        minY = thr - dis
        maxY = thr + dis
        
        if minY <= min(y):
            minY = min(y)
            
        if maxY >= max(y):
            maxY = max(y)
            
        if i >= 1:
            legend = False
        
        x = np.arange(len(y))
        
        fig.add_trace(
            go.Scatter(x=x, y=y, name=label, showlegend=legend, line_color='blue'),
            row=row, col=col
        )
        
        x_dis = [0, 0, len(y)-1, len(y)-1, 0]
        y_dis = [minY, maxY, maxY, minY, minY]
        
        fig.add_trace(
            go.Scatter(x=x_dis, y=y_dis, fill="toself", mode='none', name=methods[i], hoverinfo="skip", fillcolor=fillcolor[i], opacity=0.7), row=row, col=col
        )

        #fillcolor=fillcolor[i], opacity=0.8

        fig.update_xaxes(
        range=[0, len(y)-1])
        
        fig.update_yaxes(
            range=[min(y), max(y)+0.01])
        
        #fig.add_trace(fig.add_hrect(y0=minY, y1=maxY, line_width=0, fillcolor="red", opacity=0.2),
        #              row=row, col=col)
    
        
        if col == 2:
            row += 1
            col = 1
        else:
            col += 1
        
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey')
        
    fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey')
        
    fig.update_layout(height=800, width=800, plot_bgcolor='white')
    
    return fig
    

def make_plot(methods, gene, data, thr_k, thr_o, thr_s, thr_b, splineGenes):
    
    fig = go.Figure()

    fillcolor = ['#dae5ef', '#ffdddd', '#ddf5dd', '#ffe7d2']
    fillcolor = ['red', 'blue', 'green', 'orange']
    
    ySpline = splineGenes[str(gene)]
    y = list(data[gene].values())
    label = y[-1]
    y.pop(-1)
    
    x = np.arange(len(y))
        
    fig.add_trace(
            go.Scatter(x=x, y=y, name=label, showlegend=True, line_color='blue')
    )
    
    xSpline = np.linspace(0, len(y)-1, len(ySpline))
    
    fig.add_trace(
            go.Scatter(x=xSpline, y=ySpline, name=label+" Spline", showlegend=True, line_color='red')
    )
    
    dash = ['dot', 'dash', 'longdash', 'dashdot']
    index= 0 
    
    for m in methods:
        
        if m == "BASC A":
            thr = thr_b[str(gene)]
            
        elif m == "Onestep":
            thr = thr_o[str(gene)]
            
        elif m == "K-Means":
            thr = thr_k[str(gene)]
            
        else:
            thr = thr_s[str(gene)]
            
        yThr = np.full(len(y), thr)
        
        fig.add_trace(
            go.Scatter(x=x, y=yThr, name=m, showlegend=True, line=dict(dash=dash[index], color=fillcolor[index]))
            
        )
        index += 1
        
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        range=[0, len(y)-1])
        
    fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            range=[min(y), max(y)+0.01])
        
    fig.update_layout(height=800, width=800, plot_bgcolor='white', title="Threshold for "+label,
                     xaxis_title="Time Series", yaxis_title="Expression Level")
        
    
    return fig    

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
    if gene == [] or methods == None or methods == [] or gene == None:
        return "Select genes or threshold methods to binarize."
    
    cond = verify_thr_is_in_dict(gene, methods, thr_k, thr_b, thr_o, thr_s)

    if cond:
        return None
    
    gene_selected = list(data[(gene)].values())
    gene_selected.pop(-1)
    
    
    disps = getDisplacement(methods,gene_selected)

    #print(thr_s)

    return [ html.Div(style={"height": "20px"}), dbc.Card(
                dbc.CardBody([
                    html.Hr(),html.P("Spline approximation of gene expression and threshold displacement for every algorithm. The voting table shows the binarization using selected algorithms and the consensus binarization.", style={'textAlign': 'center'}),
                    html.Br(), html.P("*Values that are too close to the threshold will be considered undecided with a (?) on the table."),
                ]),
                className="mb-3",
            ),
        
            #make_displacement_graphs(methods, gene, data, thr_k, thr_o, thr_s, thr_b, spline_genes)
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

    if gene == [] or methods == None or methods == [] or gene == None:
        return "Select genes or threshold methods to binarize."
    
    cond = verify_thr_is_in_dict(gene, methods, thr_k, thr_b, thr_o, thr_s)

    if cond:
        return None
    
    return vote_table(gene, methods, data, thr_b, thr_k, thr_s, thr_o)


def vote_table(row, selected_method, data, thr_b, thr_k, thr_s, thr_o):
    
    # if they are none return nothing to the dashboard
    if row is None or selected_method is None or data is None:
        return None
    
    # get dataframe
    df = pd.DataFrame(data)
    labels = df['Gene ID']
    df = df.loc[:, df.columns!='Gene ID']

    # get selected gene
    selected = df.iloc[row]
    gene = selected.values
       
    disps = getDisplacement(selected_method,gene)

    #print(disps)
    
    t = []
    d = []

    # go through each method and interpolate n times given by the user
    for method in selected_method:
        if(method == 'BASC A'):
            # get threshold of orignal gene
            t.append(thr_b[str(row)])
        
            d.append(disps['BASC_A'].iloc[0])
 
        elif(method == 'K-Means'):
            # get threshold of orignal gene
            t.append(thr_k[str(row)])
           
            d.append(disps['k-means'].iloc[0])
       
        elif(method == 'Onestep'):
            # get threshold of orignal gene
            t.append(thr_o[str(row)])
        
            d.append(disps['onestep'].iloc[0])
            
        else:
            # get threshold of orignal gene
            t.append(thr_s[str(row)])
            
            d.append(disps['shmulevich'].iloc[0])
   
    #print(gene, t, d)
    # find the voting table of that gene 
    votes = election_strings(gene, t, d)
    
    rows_data = []
    
    # append rows of the datatable
    for line in votes[0]:
        rows_data.append(line)
        
    # append final vote row
    rows_data.append(votes[1])

    
    # append final label
    selected_method.append("Elected")
    
    # create dataframe of voting table 
    vote_df = pd.DataFrame(data=rows_data, index=selected_method)
    vote_df.reset_index(inplace=True)
   
    # return components and table 
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

    xx = np.arange(0,sizeGene)
    #dict of thresholds and labels for graph display
    thr_dict = {'label':[],'y':[],'x':[]}

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
    probden = pd.read_csv("cdf_"+str(rangeIndex+1)+".csv")
    disps = getDisplacement(selected_method,gene)

    for method in selected_method:
        if method == 'K-Means':
        #if thr_k is not None:
                
                #get binarized gene string
                count = 0
                bin = ""
                d = disps['k-means']
                for g in gene:
                    if g > thr_k + d.iloc[0]:
                        bin += '1'
                    elif g < thr_k - d.iloc[0]:
                        bin += '0'
                    else:
                        bin += '?'
                        count += 1

                #generate dataframe with all possible strings and their probabilities
                #probBin function 
                probDF = probBin(gene,d.iloc[0],sizeGene,'k-means',probden)

                #extract probability of selected string
                #from dataframe probBin
                binProb = probDF.loc[probDF['string']==bin]['prob'].iloc[0]
                
                #append selected val
                prob_dict['label'].append('k-means')
                prob_dict['string'].append(bin)
                prob_dict['prob'].append(binProb)
                prob_dict['res'].append((len(gene)-count)/len(gene))
                prob_dict['mean'].append(1/(3**sizeGene))
                prob_dict['sd'].append(standard_dev['k-means'].iloc[0])
                
                #append highest string prob and its prob
                probDF = probDF.sort_values(by=['prob'])
                prob_dict['highest'].append(probDF['string'].iloc[-1])
                prob_dict['highestprob'].append(probDF['prob'].iloc[-1])
            
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
                probDF = probBin(gene,d.iloc[0],sizeGene,'onestep',probden)

                #extract probability of selected string
                #from dataframe probBin
                binProb = probDF.loc[probDF['string']==bin]['prob'].iloc[0]
                
                #append selected val
                prob_dict['label'].append('onestep')
                prob_dict['string'].append(bin)
                prob_dict['prob'].append(binProb)
                prob_dict['res'].append((len(gene)-count)/len(gene))
                prob_dict['sd'].append(standard_dev['onestep'].iloc[0])
                prob_dict['mean'].append(1/(3**sizeGene))

                #append highest string prob and its prob
                probDF = probDF.sort_values(by=['prob'])
                prob_dict['highest'].append(probDF['string'].iloc[-1])
                prob_dict['highestprob'].append(probDF['prob'].iloc[-1])

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
                
                probDF = probBin(gene,d.iloc[0],sizeGene,'shmulevich',probden)
                
                #extract probability of selected string
                binProb = probDF.loc[probDF['string']==bin]['prob'].iloc[0]


                prob_dict['mean'].append(1/(3**sizeGene))
                prob_dict['label'].append('shmulevich')
                prob_dict['string'].append(bin)
                prob_dict['prob'].append(binProb)
                prob_dict['res'].append((len(gene)-count)/len(gene))
                prob_dict['sd'].append(standard_dev['shmulevich'].iloc[0])
                
                
                #extract highest probability and add to dict
                probDF = probDF.sort_values(by=['prob'])
                prob_dict['highest'].append(probDF['string'].iloc[-1])
                prob_dict['highestprob'].append(probDF['prob'].iloc[-1])

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
                
                probDF = probBin(gene,d.iloc[0],sizeGene,'BASC_A',probden)
                
                #extract probability of selected string
                binProb = probDF.loc[probDF['string']==bin]['prob'].iloc[0]
                
                prob_dict['mean'].append(1/(3**sizeGene))
                prob_dict['label'].append('BASC_A')
                prob_dict['string'].append(bin)
                prob_dict['prob'].append(binProb)
                prob_dict['res'].append((len(gene)-count)/len(gene))
                prob_dict['sd'].append(standard_dev['BASC_A'].iloc[0])
                
                #extract highest probability and add to dict
                probDF = probDF.sort_values(by=['prob'])
                prob_dict['highest'].append(probDF['string'].iloc[-1])
                prob_dict['highestprob'].append(probDF['prob'].iloc[-1])
            
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

def state_transition_table(df, method):

    return html.Div(
        
        style={'padding': 5, 'display':'flex', 'flexDirection':'column', 'textAlign':'center'},
        children=[
         dcc.Store(id=f"{method}-data", data=df.to_dict('records')),
         html.B(method +" Binarization States"),
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

     # if these values are none return none to the dashboard
    if selected_method is None or selected_method == []:
        return None
    if data is None or data == []:
        return None
    if selected_rows is None or selected_rows == []:
        return None
    
    cond = verify_thr_is_in_dict2(selected_rows, selected_method, thr_k, thr_b, thr_o, thr_s)

    if cond:
        return None
    
    selected_rows.sort()

    df = pd.DataFrame(data)
    labels = df['Gene ID']
    df = df.loc[:, df.columns!='Gene ID']

    #get the plot, and network of the final vote plot
    elected_state_network = create_boolean_network_votes(selected_rows, df, selected_method, displacements, thr_k, thr_o, thr_s, thr_b, labels)

    transition = []

    for method in selected_method:

        network = create_boolean_network(selected_rows, method, df, displacements, thr_k, thr_o, thr_s, thr_b, labels)

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


    if len(selected_method) > 2:
 
        transition_df = html.Div([html.Div(transition[:2]), html.Div(transition[2:])], style={'display': 'flex', 'flexDirection': 'row'})

    else:
        transition_df = html.Div(transition[:2])

     # component of final transition table
    final_transition_df = html.Div(children = [
                html.Div(style={"height": "20px"}),
                dbc.Card(
                        dbc.CardBody([
                            state_transition_table(elected_state_network, "Elected")
                        ]),
                    className="mb-3")
                ], style={"marginRight": "20px"})
    
    

    # return components and tabs 

    return  html.Div(children = [transition_df, final_transition_df], style={'display': 'flex', 'flexDirection': 'row'})


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

    if methods == [] or methods == None:
        return "Select threshold methods to show Boolean Network."
    if rows == [] or rows == None:
        return "Select genes from table to show Boolean Network."

    network_plots = []

    rows.sort()

    #print(kmeans)

    for method in methods:

        if method == "BASC A":
            data = pd.DataFrame(basca)
        elif method == 'K-Means':
            data = pd.DataFrame(kmeans) 
        elif method == 'Onestep':
            data = pd.DataFrame(onestep)
        elif method == 'Shmulevich':
            data = pd.DataFrame(shmulevich)
        

        fig2, _, legend = create_boolean_network_graph(data)

        #transition.append(transition_table(network, method))
        legend_comps = []
        for a in legend:
            comp = html.P(f"{str(a)} = {str(legend[a])}")
            legend_comps.append(comp)

        if legend_comps != []:

            legend_comps.insert(0, html.P("Letters are for edges where there are many loops"))


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


    if len(methods) > 2:
 
        network_plots = html.Div([html.Div(network_plots[:2]), html.Div(network_plots[2:])], style={'display': 'flex', 'flexDirection': 'row'})
    

    else:

        network_plots = html.Div([html.Div(network_plots)], style={'display': 'flex', 'flexDirection': 'row'})


    fig, _, legend_votes = create_boolean_network_graph_votes(elected)

    legend_comps_vote = []
    for a in legend_votes:
            comp = html.P(f"{str(a)} = {str(legend_votes[a])}")
            legend_comps_vote.append(comp)

    if legend_comps_vote != []:

            legend_comps_vote.insert(0, html.P("Letters are for edges where there are many loops"))


    return    html.Div([
                            html.Div(style={"height": "20px"}),
                            dbc.Card(
                                dbc.CardBody([
                                    html.P("This section provides the Boolean Network of the Binarization by each selected method and elected method."),
                                    html.P("Each number in the edges are the time series steps until the final state. The table representation of these networks are in 'Binarization State Table',"),
                                ]),
                                className="mb-3",
                            ),
                            
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
    
    #print(rule_network)
    if methods is None or methods == [] or rule_network == {} or rule_network is None:
        return "Upload transition rules to see network analysis or selected genes or methods"

    df = pd.DataFrame()

    data_algos = pd.DataFrame()

    rule_network = pd.DataFrame(rule_network)

    _, rule_network = createNetwork(rule_network)

    for method in methods:

        if method == "BASC A":
            data = turn_df_to_array(basc)
            df_analysis = hamming_state_by_state(rule_network, data, method)

            df_bin = pd.DataFrame({method:data})
            data_algos = pd.concat([data_algos, df_bin], axis=1)

        elif method == 'K-Means':
            data = turn_df_to_array(kmeans) 
            #print(data, rule_network)
            df_analysis = hamming_state_by_state(rule_network, data, method)

            df_bin = pd.DataFrame({method:data})
            data_algos = pd.concat([data_algos, df_bin], axis=1)

        elif method == 'Onestep':
            data = turn_df_to_array(onestep)
            df_analysis = hamming_state_by_state(rule_network, data, method)

            df_bin = pd.DataFrame({method:data})
            data_algos = pd.concat([data_algos, df_bin], axis=1)

        elif method == 'Shmulevich':
            data = turn_df_to_array(shmulevich)
            df_analysis = hamming_state_by_state(rule_network, data, method)

            df_bin = pd.DataFrame({method:data})
            data_algos = pd.concat([data_algos, df_bin], axis=1)

        df = pd.concat([df, df_analysis], axis=1)

    df_bin = pd.DataFrame({'Elected':turn_df_to_array(elected_network)})
    data_algos = pd.concat([data_algos, df_bin], axis=1)
    
    df_init_final = generate_init_final_comparison(data_algos, rule_network)

    df_chain_elected, cond = hamming_chain(rule_network, turn_df_to_array(elected_network))

    if cond == False:

        chain_hamming = html.P("Cannot analyze network because initial state does not exist in Boolean Function Network")

    else:

        chain_hamming = dash_table.DataTable(df_chain_elected.to_dict('records'), [{"name": i, "id": i} for i in df_chain_elected.columns], style_table={'overflowY': 'auto'})


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

    #for state in path:

    for node in net.nodes:

        if node['label'] in path:
            node['color']= 'yellow'

    return net

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

    #print(n_clicks)

    if n_clicks is None:
        return None, None
    
    selected_rows.sort()
    
    #print(inference_method)
    if inference_method is None or inference_method == []:
        return None, None
    if methods is None or methods == []:
        return "Select a threshold method to infer rules.", None
    

    if bin_method is None or bin_method == []:
        return "Select a binarization method to infer the network.", None
    
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
    
    if (df_binary == '?').any().any():
        return f"Make sure that the state table of {bin_method} has no '?' values.", None
    
    dict_data = {}
    df_data = pd.DataFrame(data)

    labels = df_data['Gene ID']

    df_data = df_data.loc[:, df_data.columns!='Gene ID']

    for row in selected_rows:
        dict_data[labels[row]] = df_data.iloc[row]

    df_data = pd.DataFrame(dict_data)

    #print(df_data)
    #print(df_binary)

    df_data = df_data.apply(pd.to_numeric)
    df_binary = df_binary.apply(pd.to_numeric)

    df_data.index = df_data.index.astype(int)
    df_binary.index = df_binary.index.astype(int)

    if inference_method == "LogicGep":

        df_infer_rules = LogicGep(df_binary, df_data)

    elif inference_method == 'MIBNI':

        mibni = Mibni(10, df_binary, "dynamics.tsv")
        result = mibni.run()

        rules_infered = {'Gene':[],
                         'Rule':[]}
        for r in result:

            rul = r.split(" = ")
            rules_infered['Gene'].append(rul[0])
            rules_infered['Rule'].append(rul[1])

        df_infer_rules = pd.DataFrame(rules_infered)
        
    else:
    
        #data_converted = {key: [int(b[key]) for b in bin_dict] for key in bin_dict[0]}

        #for elt in data_converted:
        #    arr = bitarray(data_converted[elt])
        #    data_converted[elt] = arr
        
        #print("antes")
        result = run_code(df_binary)
        #print("aqui")
        #print(result)
        
        #genes_names = df_binary.columns

        #rules = {'Gene':[],
        #         'Rule':[]}
        
        #r = []

        #for g in genes_names:
            
        #    r.append(result[g])

        #rules['Gene'] = genes_names
        #rules['Rule'] = r

        if result is None:

            return html.P("Best fit was not able to infer all Boolean Functions. Try again, user other binarizations or imputate different values."), None

        df_infer_rules = pd.DataFrame(result)

    net, dict_net = createNetwork(df_infer_rules)

    #df_net_table = pd.DataFrame(dict_net.items(), columns=['t', 't+1'])

    #print(df_binary.iloc[0].values, dict_net, len(df_binary), df_binary.columns)

    state = df_binary.iloc[0].values

    state = ''.join(str(s) for s in state)

    path, net = extract_path(state, dict_net, len(df_binary), list(df_binary.columns), net)

    #net = states_in_graph(net, state, len(df_binary))

    if len(net.nodes) > 1000:

        return html.Div([

            dcc.Store(id='inferred_net_rules', data=df_infer_rules.to_dict('records')), 
            dbc.Card(
                    dbc.CardBody([
                            html.B("Table of Inferred Boolean Functions"),
                            dash_table.DataTable(df_infer_rules.to_dict('records'), [{"name": i, "id": i} for i in df_infer_rules.columns]),
                            html.Br(),
                        ]),
            className="mb-3"),

            html.P("Cannot display Boolean Network because it has too many nodes"),


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

    return  html.Div([

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
                                    html.B("Network Based on Inferred Boolean Functions"),
                                    html.P("Grey nodes are attractors, and green nodes are the extracted path based on first state of the selected method"),
                                
                                    html.Iframe(
                                                    srcDoc=net.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                                    width="500px",
                                                    height="500px"
                                    ),
                                
                                ], style={'display': 'flex', 'flexDirection': 'column', 'marginRight':'20px'}),
                                ]),
                        className="mb-3"),

            ], style={'display': 'flex', 'flexDirection': 'row', 'overflowY': 'auto'}),


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

    if rows is None and methods is None and data is None and rules is None or methods == [] or rules == [] or rows == []:
        return None 
    
    if rules == {}:
        return None
    
    rows.sort()

    net, _ = createNetwork(pd.DataFrame(rules)) 

    if len(net.nodes)  > 1000:

        return html.P("Cannot generate Boolean Network because its too big.")

    return html.Div([
                    html.B("Network Based on Uploaded Boolean Functions"),
                    html.Iframe(
                        srcDoc=net.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                        width="500px",
                        height="500px"
                    ),
            ], style={'display': 'flex', 'flexDirection': 'column'})

@app.callback(
    Output('dropdown-method', 'value'),
    Input('methods-all', 'n_clicks'),
    prevent_initial_call=True
)
def select_all_methods(n_clicks):
    if n_clicks is None:
        return None
    
    return ['BASC A', 'K-Means', 'Onestep', 'Shmulevich']

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
    if data is None:
        return None
    if n_clicks is None and n_clicks2 is None:
        return None
    
    if n_clicks != None:

        array = np.arange(0, len(data))

        return array, None, None
    
    elif n_clicks2 != None:
        
        return [], None, None


@app.callback(
    Output("imputate-dropdowns", 'children'),
    Input('dropdown-method', 'value'), 
    prevent_initial_call=True)
def imputate_dropdowns(methods):

    if methods is None or methods == []:
         methods = []
    #    return None

    return html.Div(children = [
        
        html.B('Select method state table to imputate values:'),
                        dcc.Dropdown(
                            methods+['Elected'],
                            placeholder="Select method table",
                            id="imputate-method",
                            multi=False,
                            searchable=False),
        
        html.B('Select an option to imputate values:'),
                        dcc.Dropdown(
                            options=[{'label': 'Global Imputation (ex: changes all "?" to either 0 or 1)', 'value':0},
                             {'label': 'Gene Imputation (ex: imputates a value for only one gene)', 'value':1},
                             {'label': 'Time Impuation (ex: imputates values based on time course)', 'value':2},
                             {'label': 'MissForest (Random Forest) Imputation', 'value':4},
                             {'label': 'Framework Statistics Algorithm', 'value':3}],
                            placeholder="Select option",
                            id="imputate-option",
                            multi=False,
                            searchable=False),
        
        
        html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),

        html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
        
        html.Div(id='dropdown-imputate-options'),

        html.Button('Reset Imputations', id='reset-imputation'),

        #html.Div(id='reset-comp'),

        
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

        #html.Button('Imputate 1', id='all-to-1'), html.Button('Imputate 0', id='all-to-0')
    ])


@app.callback(
    Output('Elected-table-dropdown', 'data', allow_duplicate=True),
    Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
    Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
    Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
    Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
    Output('reset-imputation', 'n_clicks'),
    Input('reset-imputation', 'n_clicks'),
    Input('Elected-data', 'data'),
    Input('K-Means-data', 'data'),
    Input('Shmulevich-data', 'data'),
    Input('BASC A-data', 'data'),
    Input('Onestep-data', 'data'),
    Input('imputate-method', 'value'),
    prevent_initial_call=True
)
def reset_table(n_clicks, elected, kmeans, shmulevich, basc, onestep, table):

    if n_clicks is None or table is None or table == []:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None
    
    result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None]


    #print(n_clicks, table)

    #print(basc)
    
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


@app.callback(
    Output("dropdown-imputate-options", 'children'),
    Input('imputate-option', 'value'),
    Input('datatable-interactivity', 'selected_rows'),
    Input('datatable-interactivity','data'),
    prevent_initial_call=True)
def imputate_options(option, rows, data):

    if option is None or option == []:
        return None
    
    rows.sort()

    if option == 0:

        return html.Div([
        html.Button('Imputate 1', id='all-to-1'),
        html.Button('Imputate 0', id='all-to-0'),

        html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
        html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
        

    
        html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
        html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),

        html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),

        html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
        

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

    elif option == 1:

        df = pd.DataFrame(data)
        df = df['Gene ID']

        labels = df[rows]

        return html.Div(children = [
            html.B('Select a gene to imputate values:'),
            dcc.Dropdown(
                labels,
                placeholder="Select gene",
                id="imputate-gene",
                multi=True,
                searchable=False),
            html.Button('Imputate 1', id='gene-to-1'), html.Button('Imputate 0', id='gene-to-0'),

        
        html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
        html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),

    
        html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
        html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),

        html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),

        html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
    
        dcc.Dropdown(
                [],
                placeholder="Select time courses",
                id="imputate-time",
                multi=True,
                searchable=False,
                style={'display': 'none'}),
        ])

    elif option == 2:

        df = pd.DataFrame(data)

        df = len(df['Gene ID'])

        options = [{'label':"Time " + str(i), 'value': i} for i in np.arange(0, df)]

        #print(options)

        return html.Div(children = [
            html.B('Select an time courses to imputate values:'),
            dcc.Dropdown(
                options,
                placeholder="Select time courses",
                id="imputate-time",
                multi=True,
                searchable=False),
            html.Button('Imputate 1', id='time-to-1'), html.Button('Imputate 0', id='time-to-0'),

        html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
        html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
   
        html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
        html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),

        html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),

        html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),
        
        dcc.Dropdown(
            [],
            placeholder="Select gene",
            id="imputate-gene",
            multi=True,
            searchable=False,
            style={'display': 'none'}),

     
        ])
    
    elif option == 3:

        return html.Div([

            html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
            
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

    elif option == 4:

        return html.Div([
            html.Button('Imputate MissForest', id='missforest-button'),

            html.Button('Imputate Strings based on Statistics', id='stat-impu-button', style={'display': 'none'}),

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
    
    else:
        return None
        

def imputate_value_all(data, value):

    df = pd.DataFrame(data)

    df.replace("?", value, inplace=True)

    return df.to_dict('records')


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
    
    if n_clicks is None and n_clicks2 is None or option == None or method == [] or method is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None
    
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
    
    result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None]
    
    if n_clicks != None and option == 0:

        data = imputate_value_all(data, 1)

        result[indx] = data

        #print(result)
      
        return tuple(result)
    
    elif n_clicks2 != None and option == 0:

        data = imputate_value_all(data, 0)

        result[indx] = data

        return tuple(result)


def imputate_value_gene(df, value, genes):

    df = pd.DataFrame(df)

    for g in genes:

        df[g] = df[g].replace("?", value)

    #print(df)

    return df.to_dict('records')

@app.callback(
    Output('BASC A-table-dropdown', 'data', allow_duplicate=True),
    Output('K-Means-table-dropdown', 'data', allow_duplicate=True),
    Output('Shmulevich-table-dropdown', 'data', allow_duplicate=True),
    Output('Onestep-table-dropdown', 'data', allow_duplicate=True),
    Output('stat-impu-button', 'n_clicks'),

    Input('stat-impu-button', 'n_clicks'),
    Input('imputate-method', 'value'),
    Input('datatable-interactivity','data'),
    Input('datatable-interactivity', 'selected_rows'),
    prevent_initial_call=True)
def imputate_based_statistics(n_clicks, method, dataset, rows):
    
    if n_clicks is None or method == [] or method is None or method == "Elected":
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, None
    
    result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, None]

    if n_clicks != None:

        data = pd.DataFrame(dataset)

        rows.sort()

        labels = data['Gene ID']

        data = data.loc[:, data.columns!='Gene ID']

        genes = data.iloc[rows].values.astype(float)

        labels = [labels[i] for i in rows]

        string_dict = {} 

        for i in range(len(genes)):

            disps = getDisplacement([method], genes[i])

            if(method == 'BASC A'):
               
                d = disps['BASC_A'].iloc[0]
    
            elif(method == 'K-Means'):
             
                d = disps['k-means'].iloc[0]
        
            elif(method == 'Onestep'):
              
                d = disps['onestep'].iloc[0]
                
            else:
                d = disps['shmulevich'].iloc[0]

            Z = probabilistic(np.array(genes[i]), [method], d)

            string_high_P = max(Z, key=Z.get)

            array_high_P = [e for e in string_high_P]

            string_dict[labels[i]] = array_high_P

        #print(string_dict)

        df = pd.DataFrame(string_dict)
        
        if(method == 'BASC A'):
            result[0] = df.to_dict('records')
        
    
        elif(method == 'K-Means'):
            result[1] = df.to_dict('records')
    
        
        elif(method == 'Onestep'):
            result[3] = df.to_dict('records')
             
        else:
            result[2] = df.to_dict('records')
        
        return tuple(result)

            #bin_array = bin_strings[labels[i]].tolist()

            #bin_s = ""

            #for e in bin_array:

            #    bin_s += str(e)
            


            #high_P = Z[string_high_P]

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
    
    if n_clicks is None or method == [] or method is None or method == []:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, None
    
    result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None]

    if n_clicks != None:
        
        if(method == 'Elected'):

            result[0] = imputate_missforest(elected)
        
        
        if(method == 'BASC A'):
            result[1] = imputate_missforest(basc)
        
    
        elif(method == 'K-Means'):
            result[2] = imputate_missforest(kmeans)
    
        
        elif(method == 'Onestep'):
            result[4] = imputate_missforest(onestep)
             
        else:
            result[3] = imputate_missforest(shmule)
        
        return tuple(result)


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
    
    if n_clicks is None and n_clicks2 is None or option == None or genes == None or genes == []:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None
    
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
    
    result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None]

    if n_clicks != None and option == 1:

        data = imputate_value_gene(data, 1, genes)

        result[indx] = data
      
        return tuple(result)
    
    elif n_clicks2 != None and option == 1:

        data = imputate_value_gene(data, 0, genes)

        result[indx] = data

        return tuple(result)



def imputate_value_time(df, value, timeCourse):
    df = pd.DataFrame(df)

    for time in timeCourse:

        df.iloc[time] = df.iloc[time].replace("?", value)

    return df.to_dict('records')


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
    
    if n_clicks is None and n_clicks2 is None or option == None or timecourse == None or timecourse == []:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None
    
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
    
    result = [dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, None]

    if n_clicks != None and option == 2:

        data = imputate_value_time(data, 1, timecourse)

        result[indx] = data
      
        return tuple(result)
    
    elif n_clicks2 != None and option == 2:

        data = imputate_value_time(data, 0, timecourse)

        result[indx] = data

        return tuple(result)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)