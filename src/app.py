import dash
from dash import dcc, html, Input, Output, ClientsideFunction, dash_table, State
import numpy as np
import pandas as pd
import io
import base64
import dash_bootstrap_components as dbc

# import gene normalization, interpolation, and thr methods functions
from binarization.normalize import geneNorm 
from binarization.interpolation import interpolation
from threshold_methods.methods import call_C_BASC, BASC_A, call_C_Stepminer, onestep, K_Means, shmulevich, call_C_shmulevich, call_C_kmeans, call_C_Onestep

######### Import each tab callbacks and components (importing each tab component) ########
# imports every component and callbacks about value imputation (Network tab)
from imputation_callback.imputation_callback import get_imputation_callbacks

# imports componetents and callbacks about networks, state table, and inference (Nerwork tab)
from network_state_inference_callback.network_state_inference_callback import get_network_inf_callbacks 

# imports componets and callbacks from Statistics tab
from statistics_callback.statistics_callback import get_stats_callback

# import componets and callbacks from Binarization, and Displacement tabs
from binary_disp_callback.binary_disp_callback import get_bin_disp_callback


# read displacement and standard dev files
displacements = pd.read_csv("./displacements/Displacements.csv")
standard_dev = pd.read_csv("./statistics_methods/standard_dev.csv")

# Create dash app object
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ]
)

# give title to app
app.title = "ViBEx: A Visualization Tool for Gene Expression Analysis"

# set up server and callbacks exceptions
server = app.server
app.config.suppress_callback_exceptions = True


# function with description componets about app (left side)
def description_card():
  
    """
     description_card returns left side panel of the app information and components about ViBEx.
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

            # upload button to import gene expression files
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

# function that returns components about thr selections 
def generate_control_card():

    """
      generate_control_card returns threshold methods dropdown, download button 
    """
    
    return html.Div(
        id="control-card",
        children=[
            html.Br(),
            html.P("Select threshold computation methods:"),
            # select all methods button
            html.Button('Select all', id='methods-all'),

            # dropdown selectable for threshold methods
            dcc.Dropdown(
                ['BASC A', 'K-Means', 'Onestep', 'Shmulevich'],
                placeholder="Select binarization method",
                id="dropdown-method",
                multi=True,
                #persistence = True,
                #persistence_type = 'memory',
                searchable=False),
            
            # button to download thresholds
            html.Br(),
            html.B('Download the threshold of the selected rows to a csv:'), 
            html.Button("Download CSV", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
            html.Br(),

            # save variables in storage as empty (so no callback error occur)
            dcc.Store(id='thr_k', data={}), 
            dcc.Store(id='thr_o', data={}),
            dcc.Store(id='thr_b', data={}), 
            dcc.Store(id='thr_s', data={}),
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

            # returns imputation buttons as hidden (to avoid callback errors)
            hidden_buttons()
            
        ],
        
    )

# function returns hidden buttons from value imputation. This helps remove callback errors.
def hidden_buttons():

    """
       hidden_buttons returns imputation button hidden to prevent callback errors
    """

    return html.Div([html.Button('Statistics', id='stat-impu-button', style={'display': 'none'}),
           html.Button('Reset Imputations', id='reset-imputation', style={'display': 'none'}),

            html.Button('Imputate 1', id='all-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='all-to-0', style={'display': 'none'}),
            html.Button('Imputate 1', id='gene-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='gene-to-0', style={'display': 'none'}),
            html.Button('Imputate 1', id='time-to-1', style={'display': 'none'}),
            html.Button('Imputate 0', id='time-to-0', style={'display': 'none'}),
            html.Button('Imputate MissForest', id='missforest-button', style={'display':'none'}),
            html.Button('Imputate', id='other-impu-button', style={'display':'none'}),
        
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

#### Callback - Download threshold CSV
# process the click of the download button
# gets the threshold of the data and downsloads as a csv
# Inputs: 
@app.callback(
    Output("download-dataframe-csv", "data"),
    Output("btn_csv", "n_clicks"),
    Input("btn_csv", "n_clicks"),
    Input('datatable-interactivity','data'), 
    Input('datatable-interactivity', 'selected_rows'),
    prevent_initial_call=True,
)
def download_csv(n_clicks, data, selected_rows):
    
    """
       download_csv is generated by a callback. It processes the selected genes, and thr methods and downloads as csv.

       n_clicks: download button click
       data: uploaded gene matrix
       selected_rows: selected genes 
    """

    # no data return none
    if data is None:
        return None, None
    
    # no selected rows return None
    if selected_rows == [] or selected_rows is None:

        return None, None
    
    # if no clicks return none 
    if n_clicks is None:
        return None, None
    
    # turn gene data to dataframe
    df = pd.DataFrame(data)

    # extract labels and then remove them from dataframe
    labels = df['Gene ID']
    df = df.loc[:, df.columns!='Gene ID']
    
    # sort selected genes (in order they appear on dataset)
    selected_rows.sort()
    
    # get the selected genes values
    genes = df.iloc[selected_rows].values
    labels = labels.iloc[selected_rows].values
    rows = df.shape[0]
    
    # column names and creating dataframe
    col_names = {'Gene ID':[],'basc_thr':[], 'kmeans_thr':[], 'onestep_thr':[], 'shmulevich_thr':[]}
    final_df = pd.DataFrame(col_names)


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

#### Callback - save BASC A data to storage 
@app.callback(
    Output('BASC A-table', 'data'),
    Input('BASC A-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_basc(data):
    
    """
     save_basc makes sure to listen to changes on the BASC A table and saves the changes to storage
     This helps to save BASC A binarization after value imputation. 

     data: basc data
    """

    # if data is empty return empty dataset
    if data == None or data == [] or data == {}:
        return {}
    
    # return dataset to save it  
    return data

#### Callback - save KMeans data to storage 
@app.callback(
    Output('K-Means-table', 'data'),
    Input('K-Means-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_kmeans(data):

    """
     save_kmeans makes sure to listen to changes on the Kmeans table and saves the changes to storage
     This helps to save Kmeans binarization after value imputation. 

     data: kmeans data
    """
    
    # if data is empty return empty dataset
    if data == None or data == [] or data == {}:
        return {}

    # return dataset to save it  
    return data

#### Callback - save Onestep data to storage 
@app.callback(
    Output('Onestep-table', 'data'),
    Input('Onestep-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_onestep(data):

    """
     save_onestep makes sure to listen to changes on the Onestep table and saves the changes to storage
     This helps to save onestep binarization after value imputation. 

     data: onestep data
    """

    # if data is empty return empty dataset
    if data == None or data == [] or data == {} or len(data) == 0:
        return {}
    
    # return dataset to save it  
    return data

#### Callback - save Shmulevich data to storage 
@app.callback(
    Output('Shmulevich-table', 'data'),
    Input('Shmulevich-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_shmulevich(data):

    """
     save_shmulevich makes sure to listen to changes on the Shmulevich table and saves the changes to storage
     This helps to save shmulevich binarization after value imputation. 

     data: shmulevich data
    """

    # if data is empty return empty dataset
    if data == None or data == [] or data == {}:
        return {}

    # return dataset to save it   
    return data

#### Callback - save Elected data to storage 
@app.callback(
    Output('Elected-table', 'data'),
    Input('Elected-table-dropdown', 'data'),
    prevent_initial_call=True)
def save_elected(data):

    """
     save_elected makes sure to listen to changes on the Elected table and saves the changes to storage
     This helps to save Elected binarization after value imputation. 

     data: elected data
    """

    # if data is empty return empty dataset
    if data == None or data == [] or data == {}:
        return {}
    
    # return dataset to save it      
    return data

# network_nav returns the tabs inside network tab
def network_nav():
    """
     network_nav returns the tabs inside network tab
    """
    
    # return tabs
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
                        #html.P("There are three options of imputation values: Global imputation, gene imputation, and time course based imputation."),
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
            dcc.Loading(
                    children=[html.Div(id="generate-networks")],
            type="circle"),
            
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

                html.Button("Download metrics automatic", id='download-metrics'),
                html.Div(id='download-metrics-output'),
                dcc.Download(id="download-metrics-excel"),

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


                dcc.Loading(
                    children=[html.Div(id='inference_plots')],
                type="circle"),

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
                
                dcc.Loading(
                    children=[html.Div(id='output-rules-upload')],
                type="circle"),

                dcc.Loading(
                    children=[html.Div(id='generate-network-rules')],
                type="circle"),
                               
            ])
        ]),

        dcc.Tab(label='Analysis', children=[
                    

            dcc.Loading(
                       children=[html.Div(id='analysis-output')],
            type="circle"),

        ]),
    ])


# returns tab navigation
def tabs_nav():

    """
     tabs_nav returns the main navigation bar (Binarization, Disp, Statistics, and Network)
    """

    # return tabs 
    return dcc.Tabs([
                dcc.Tab(label='Binarization', children=[

                    dcc.Loading(
                       children=[
                                html.Div(style={"height": "20px"}),
                                dbc.Card(
                                    dbc.CardBody([html.Div(id="binarization-output")]),
                                    className="mb-3",
                                ),
                       ], type="circle")
                    
                ]),
                 dcc.Tab(label='Displacements', children=[
                    dcc.Loading(
                       children=[
                            html.Div(id='displacements-output')
                    ], type="circle")
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

#### This is the layout setup for ViBEx
app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        #html.Div(
        #    id="banner",
        #    className="banner",
        #    children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        #),

        # Left column (information about app and where matrix appears with dropdown methods)
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), html.Div(id = 'output-data-upload')],
            style={'overflowY': 'auto', 'maxHeight': '500px'}
        ),
        # Right column (nav bar of the application and where content appears)
        html.Div(
            id="right-column",
            className="eight columns",
            children=[

                html.Div(id='app-content-tabs')
                
            ], style={'overflowX': 'auto', 'maxHeight': '500px'}
        )
    ],
)

#### Callback - displays app content
@app.callback(
        Output('app-content-tabs', 'children'),
        Input('upload-data', 'contents'),
        prevent_initial_call=False
)
def content_tabs(data):

    """
       content_tabs shows the app content (nav bar or stock images when csv not uploaded)

       data: uploaded gene matrix
    """

    # display images if no csv has been uploaded
    if data is None or data == {}:
 
        # create image carousel
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

        # return div
        return html.Div(
                        carousel, 
                        style={
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'center',    
                            'paddingTop': '5vh',   
                        })
    
    # return nav bar and gene dropdown if dataset is uploaded
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
                

def parse_contents(contents, filename, date):

    """
        parse_contents receives the contents of the gene matrix and process it. Then it returns the table for the matrix

        contents: file content
        filename: name of file
        date: date file
    """

    # split content
    content_type, content_string = contents.split(',')

    # decode content
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

    # normalize each row of the dataframe 
    df_t = geneNorm(df_labels.loc[ : , df_labels.columns!=0].copy())
   
    # insert name of genes as first column
    df_t.insert(0, 'Gene ID', df_labels[0])

    # returns div with components
    return html.Div(
        id='process-data',
        children=[
            
            # name of file, buttons to select all and deselect all
            html.H5(filename),
            html.Button('Select all', id='table-all'),
            html.Button('Deselect all', id='table-deselect'),

            # interactiive table of the gene matrix (normalized)
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

            # generate methods dropdown
            generate_control_card()
        ])

#### Callback - procress the uploaded dataset
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True)
def update_output(list_of_contents, list_of_names, list_of_dates):

    """
       update_ouput receives the dataset uploaded and process it

       list_of_contents: content of file
       list_of_names: name of file
       list_of_dates: date of file
    """
    # extract info
    list_of_contents = [list_of_contents]
    list_of_names = [list_of_names]
    list_of_dates = [list_of_dates]

    # parse content and return resulting components
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    


# function to parse the contents of the uploaded rules
def parse_contents_rules(contents, filename, date):

    """
       parse_contents_rules manages uploaded rules 
    """

    # split content 
    content_type, content_string = contents.split(',')

    # decode the content
    decoded = base64.b64decode(content_string)
    
    # if it is a csv then read it 
    if 'csv' in filename:

        # read data of rules
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=0)

        for index, row in df.iterrows():
            if pd.isna(row['Rule']):
                df.loc[index, 'Rule'] = ''
            elif not row['Rule'].strip():
                df.loc[index, 'Rule'] = ''

        # save rules in storage
        return dcc.Store(id='rule_network_dict', data=df.to_dict('records'))
    
    else:
        return "The file needs to be a csv."
        

#### Callback - process the uploaded rules
@app.callback(Output('output-rules-upload', 'children'),
              Input('upload-rules', 'contents'),
              State('upload-rules', 'filename'),
              State('upload-rules', 'last_modified'),
              prevent_initial_call=True)
# function parses and update the output of the selected dataset
def update_output_rules(list_of_contents, list_of_names, list_of_dates):

    """
       update_ouput_rules receives the dataset uploaded and process it

       list_of_contents: content of file
       list_of_names: name of file
       list_of_dates: date of file
    """
    
     # extract info
    list_of_contents = [list_of_contents]
    list_of_names = [list_of_names]
    list_of_dates = [list_of_dates]

    # if there is a uploaded file then parse it 
    if list_of_contents is not None:
        # parse the content
        children = [
            parse_contents_rules(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


#### Callback - dropdown to select gene to visualize
@app.callback(Output('dropdown-gene-select', 'children'),
              Input('datatable-interactivity', 'selected_rows'),
              Input('datatable-interactivity', 'data'),
              prevent_initial_call=True)
def dropdown_gene_select(rows, data):

    """
       dropdown_gene_select: based on selected rows of datatable generate a dropdown method to select gene to visualize binarizations, displacenents, and statistics.

       rows: selected genes
       data: data from genes
    """

    # if no rows or datasets are selecred then show dropdown method empty
    if rows == [] or data == None or rows == None:
         return html.Div(style={"height": "20px"}), dbc.Card(
                        dbc.CardBody([html.B('Select gene to visualize and binarize:'), dcc.Dropdown(
                            options=[], 
                            value = None,
                            placeholder="Select gene",
                            id="dropdown-gene")]),
                        className="mb-3",
                    ),
    
    # read dataset genes
    df1 = pd.DataFrame(data)

    # extract labels of genes
    labels = df1['Gene ID']

    # sort selected genes 
    rows.sort()
    
    # returns dropdown to select which gene to display. the first selected gene is preselected
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


#### Callback - computes the threshold values based on selected genes and thr methods
@app.callback(Output('process-tabs-thr', 'children'),
              Input('datatable-interactivity', 'selected_rows'),
              Input('datatable-interactivity', 'data'),
              Input('dropdown-method', 'value'),
              prevent_initial_call=True)
def process_thr(selected_rows, data, selected_method):

    """
      process_thr computes the threshold values based on selected genes and thr methods

      selected_rows: selected genes
      data: dataset of genes
      selected_method: threshold methods selected
    """

    # if no method, gene, or data is selected or uploaded then reset variables to empty
    if selected_method is None or selected_rows is None or data is None or selected_method == []:
        return html.Div([
            html.P("Select genes, methods or upload dataset."),
            dcc.Store(id='Elected-table', data={}),
                dcc.Store(id='K-Means-table', data={}),
                dcc.Store(id='Shmulevich-table', data={}),
                dcc.Store(id='BASC A-table', data={}),
                dcc.Store(id='Onestep-table', data={}),

                dcc.Store(id='Elected-data', data={}),
                dcc.Store(id='K-Means-data', data={}),
                dcc.Store(id='Shmulevich-data', data={}),
                dcc.Store(id='BASC A-data', data={}),
                dcc.Store(id='Onestep-data', data={}),

                dcc.Store(id='thr_k', data={}), 
                dcc.Store(id='thr_o', data={}),
                dcc.Store(id='thr_b', data={}), 
                dcc.Store(id='thr_s', data={}),
                dcc.Store(id='spline-genes', data={}), 
            ])
    
    #start_time = time.time()

    #print(selected_method)

    # read saved dataset of genes
    df1 = pd.DataFrame(data)
    # remove labels of genes
    df1 = df1.loc[:, df1.columns!='Gene ID']

    # dictionaries for each threshold method
    thr_k = {}
    thr_b = {}
    thr_o = {}
    thr_s = {}

    # dictionary for spline of genes
    splineDict = {}

    # sort selected genes
    selected_rows.sort()

    # iterate each selected gene and interpolate
    for row in selected_rows:

        # get gene from dataset
        selected = df1.iloc[row]

        # extract values
        gene = selected.values

        # interpolate gene 
        splineGene = interpolation(gene)

        # save gene spline
        splineDict[row] = splineGene

    #print(splineDict)

    # iterate selected methods
    for method in selected_method:

        # iterate each selected gene
        for row in selected_rows:

            # extract spline of gene
            splineGene = splineDict[row]

            # get basc threshold 
            if(method == 'BASC A'):

                thr = call_C_BASC(splineGene.copy())

                # save thr in dict
                thr_b[row] = thr

            # get onestep threshold 
            elif(method == 'Onestep'):
                thr = call_C_Stepminer(splineGene)

                # save thr in dict
                thr_o[row] = thr

            # get shmulevich threshold 
            elif(method == 'Shmulevich'):
                #thr = shmulevich(splineGene)
                thr = call_C_shmulevich(splineGene)

                # save thr in dict
                thr_s[row] = thr

            # get kmeans threshold 
            elif(method == 'K-Means'):
                #thr = K_Means(splineGene)
                thr = call_C_kmeans(splineGene)

                # save thr in dict
                thr_k[row] = thr

    #end_time = time.time()

    #print(f"time taken to compute thr for {selected_method}:",end_time-start_time)
    #print("basc", thr_b)
    #print("kmeans", thr_k)
    #print("onestep", thr_o)
    # saves variables in storage 
    return html.Div(
            children=[
                
                # save variables in storage empty
                dcc.Store(id='Elected-table', data={}),
                dcc.Store(id='K-Means-table', data={}),
                dcc.Store(id='Shmulevich-table', data={}),
                dcc.Store(id='BASC A-table', data={}),
                dcc.Store(id='Onestep-table', data={}),

                dcc.Store(id='Elected-data', data={}),
                dcc.Store(id='K-Means-data', data={}),
                dcc.Store(id='Shmulevich-data', data={}),
                dcc.Store(id='BASC A-data', data={}),
                dcc.Store(id='Onestep-data', data={}),

                # save thr dictionaries
                dcc.Store(id='thr_k', data=thr_k), 
                dcc.Store(id='thr_o', data=thr_o),
                dcc.Store(id='thr_b', data=thr_b), 
                dcc.Store(id='thr_s', data=thr_s),
                dcc.Store(id='spline-genes', data=splineDict), 
            ])

# get components and callbacks for Binarization, Displacement tabs
get_bin_disp_callback(app)

# get components and callbacks for Statistics tab
get_stats_callback(app)

# get components and callbacks for valuen imputation dropdowns and buttons
get_imputation_callbacks(app)

# get components and callbacks for Networks, inference, and analysis (Network tab)
get_network_inf_callbacks(app)

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)