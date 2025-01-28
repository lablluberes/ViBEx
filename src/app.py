from dash import Dash, dash_table, dcc, html, Input, Output, callback, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
import matplotlib

#pretty charts!
import altair as alt
import dash_vega_components as dvc

from scipy import interpolate
matplotlib.use('Agg')

from methods import K_Means, shmulevich, BASC_A, call_C_BASC, call_C_Stepminer, onestep
from interpolation import three_interpolation, interpolationConverge
from network_graphs import create_boolean_network_graph, create_boolean_network_graph_votes, rules_graph, rules_graph_vote
from voting_algos import binarizationVoting, binVoting
from normalize import geneNorm
from ProbabilityPerm import probBin
from generate_matrix_probs import PDF
from displacementMatrixes import getDisplacement
from hamming import hamming_state_by_state, hamming_chain, generate_init_final_comparison
from networks import create_boolean_network, create_boolean_network_votes

from network_rule import createNetwork

import dash_bootstrap_components as dbc 
import base64
import io
import dash
from io import BytesIO
from plotly.subplots import make_subplots

external_stylesheets = [dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#global variables
displacements = pd.read_csv("Displacements.csv")
standard_dev = pd.read_csv("standard_dev.csv")
splineGene = None

df_state_transition_basc = None

# layout of dashboard
app.layout = html.Div([


       html.Div([
    
                     html.Div([
                            
                            html.H1('ViBEx', style={'textAlign': 'center', 'font-family':'Processor', 'font-size':'70px'}), 
                            html.H5('A Visualization Tool for Gene Expression Analysis', style={'textAlign': 'center'}),
                            html.P('ViBEx is a tool fot the analysis and exploration of gene expression binarization. Upload a dataset of gene expression and select one, many or all out of four methods for the computation of a threshold for binarization. Visualize Boolean networks of resulting states.'),
                            html.Br(),
                            html.P("Upload a time-series csv file to start."),

                            dcc.Upload(
                                        id='upload-data',
                                        children=html.Button("Upload Gene Expression File"),
                                        multiple=False,
                                    ),
                            html.P("Dataset will be preprocessed to convert data to [0,1] interval"),
                        ], style={'width':'33%'}),
                    
                    
                    html.Div([
                    
                        dbc.Carousel(
                        items = [
                            {"key": "1", "src": "/assets/table.png"},
                            {"key": "2", "src": "/assets/interp.png"},
                            {"key": "3", "src": "/assets/net.png"},
                        
                        ],
                        
                        controls = False,
                        indicators = False,
                        interval = 2000,
                        className="carousel-fade",
                        ride="carousel",
                        style={'width':'70%', 'margin':'auto'}
                        )
                        
                        
                    ], style={'width':'66%'})
                
                
                ], id='preview-imgs', style={'display': 'flex', 'flexDirection': 'row', 'top': '10%', 'position': 'absolute'}),
        

    html.Div([
        html.Div([
        
                dcc.Store(id='stored-data', storage_type='session'),
              
                html.Div(id='output-data-upload'),
            

                html.Div([
                    html.Div(id='binarize-download', style={'marginRight': '20px', 'marginLeft': '20px'}),
                    html.Div(id='dropdown-methods',  style={'marginRight': '20px', 'marginLeft': '20px'})
                   
                ], style={'display': 'flex', 'flexDirection': 'row'}),

        ] , style={'display': 'flex', 'flexDirection': 'column', 'marginRight': '20px', 'marginLeft': '20px', 'width':'40%'}),
        

        
        html.Div(id='tabs-website', style={'display': 'flex', 'flexDirection': 'column', 'width':'80%'}),
    

    ], style={'display': 'flex', 'flexDirection': 'row'}),


],style={'display': 'flex', 'flexDirection': 'column', 'marginRight': '20px', 'marginLeft': '20px', 'fontFamily': 'Arial, sans-serif'})



# function to parse the contents of thje selected file
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    # decode the content
    decoded = base64.b64decode(content_string)
    
    # if it is a csv then read it 
    if 'csv' in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)

        df_t = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)

        # normalize each row of the dataframe based on this formula x' = (x-min)/(max-min) and save it to the dataframe
        #for i in range(len(df)):
        #    vect = df.iloc[i].values
            
        #    norm = (vect - min(vect))/ (max(vect)-min(vect))
            
        #    df.iloc[i] = norm.round(decimals=4)

        df = geneNorm(df)
        df_t = geneNorm(df_t)
        df_t = df_t.round(5)

        #print(df)

        df_t.insert(0, 'ID', df_t.index + 1)
            
        # return a new html div that has the file name and the datatable with selectable rows
        return html.Div([
           html.H1('ViBEx', style={'textAlign': 'left', 'font-family':'Processor'}), 
           html.H5('A Visualization Tool for Gene Expression Analysis', style={'textAlign': 'left'}),
           # name of file
           dcc.Upload(
                    id='upload-data',
                    children=html.Button("Upload Gene Expression File"),
                    multiple=False,
                ),
           html.P("Dataset will be preprocessed to convert data to [0,1] interval"),

           html.H5(filename),
           html.P("Select genes from table to binarize:"),
           
           html.Button('Select All', id='select-all-button', n_clicks=0),
           html.Button('Deselect All', id='deselect-all-button', n_clicks=0),
           

           # dash datatable of data with rows that can be selected
           dash_table.DataTable(
                        id='datatable-interactivity',
                        columns=[
                            {"name": str(i), "id": str(i)} for i in df_t.columns
                        ],
                        data=df_t.to_dict('records'),
                        column_selectable="single",
                        row_selectable="multi",
                        selected_columns=[],
                        selected_rows=[],
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                        style_table={'overflowX': 'auto'},
                    ),
            # store the read dataframe
            dcc.Store(id='stored-data', data=df.to_dict('records')),
            html.Hr()

        ])
    
    else:
        return "The file needs to be a csv."

# this callout receives the contents of the file and outputs the component
# output-data-upload
@app.callback([Output('output-data-upload', 'children'),
              Output('preview-imgs', 'style')],
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True)
# function parses and update the output of the selected dataset
def update_output(list_of_contents, list_of_names, list_of_dates):
    list_of_contents = [list_of_contents]
    list_of_names = [list_of_names]
    list_of_dates = [list_of_dates]
    
    # if there is a selected file
    if list_of_contents is not None:
        # parse the content
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children, {'display': 'none'}


# function to parse the contents of thje selected file
def parse_contents2(contents, filename, date):
    content_type, content_string = contents.split(',')

    # decode the content
    decoded = base64.b64decode(content_string)
    
    # if it is a csv then read it 
    if 'csv' in filename:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=0)
            
        # return a new html div that has the file name and the datatable with selectable rows
        return html.Div([
      
            # store the read dataframe
            dcc.Store(id='stored-rules', data=df.to_dict('records')),
            html.Hr()

        ])
    
    else:
        return "The file needs to be a csv."


@app.callback(Output('output-rules-upload', 'children'),
              Input('upload-rules', 'contents'),
              State('upload-rules', 'filename'),
              State('upload-rules', 'last_modified'),
              prevent_initial_call=True)
# function parses and update the output of the selected dataset
def update_output2(list_of_contents, list_of_names, list_of_dates):
    list_of_contents = [list_of_contents]
    list_of_names = [list_of_names]
    list_of_dates = [list_of_dates]

    # if there is a selected file
    if list_of_contents is not None:
        # parse the content
        children = [
            parse_contents2(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


#taken and modified from https://stackoverflow.com/questions/61905396/dash-datatable-with-select-all-checkbox
# for select all and deselect all of datatable
@app.callback(
    Output('datatable-interactivity', 'selected_rows'),
    Output('select-all-button', 'n_clicks'),
    Output('deselect-all-button', 'n_clicks'),
    Input('select-all-button', 'n_clicks'),
    Input('deselect-all-button', 'n_clicks'),
    State('datatable-interactivity', 'data'),
    State('datatable-interactivity', 'selected_rows'),
    prevent_initial_call=True)
def select_all(n_clicks, n_clicks2, data, selected_rows):
    # is there is data do this
    if data is not None:
        # if press select all enumarate all rows
        if n_clicks:
            return [i for i, row in enumerate(data)], 0, 0
        # if deselect all is pressed return empty list (to deselect rows)
        #THIS DOESNT WORK
        elif n_clicks2:
            return [], 0, 0
            
        
# render components (button to download csv with threshold)
@app.callback(
    Output('binarize-download', 'children'),
    Input('stored-data','data'),
    Input('datatable-interactivity', 'selected_rows'),
    prevent_initial_call=True )
def binarize_download(data, selected_rows):
    # if no data return nothing
    if data is None:
        return None
    # if no selected rows return nothing
    elif selected_rows is None or len(selected_rows) == 0:
        return None
    
    # return components of button
    else:  
        return [html.B('Download the threshold of the selected rows to a csv:'), html.Button("Download CSV", id="btn_csv"),
        dcc.Download(id="download-dataframe-csv")]

# render the tabs of binarization, interpolation and network 
@app.callback(
        Output('tabs-website', 'children'),
        Input('stored-data', 'data'),
        prevent_initial_call=True
)
def tabs_website(data):
    # if no data return none
    if data is None:
        return None
    
    # return tabs components
    return [ html.Div(id='select-gene-binarize', style={"width": "33%", 'marginRight': '20px', 'marginLeft': '20px', 'padding':10}), 
            
					dcc.Tabs([
                      dcc.Tab(label='Binarization', children=[
                            html.Div([
                                        html.P("Select rows from table and methods from dropdown to binarize genes:"),
										
										#dcc.Tabs([
										
											#dcc.Tab(label='One iteration', children=[
											#	html.Div(id='heatmap-binarize')										
											#]),
											
											#dcc.Tab(label='Four iterations', children=[
												html.Div(id='voting-output')										
											#])
																			
										#]),
										
									])
								]),							

                      dcc.Tab(label='Displacement', children=[
                          html.Div([
                                #html.P("Select rows from table and methods from dropdown to binarize genes:"),
                                html.Div(id='section-threshold'),

                                html.Div([
                                
                                    html.Div(id='threshold-tabs', style={"width": "100%"})


                                ], style={'display': 'flex', 'flexDirection': 'row'}),

                            ]),

                      ]),
					  
					  dcc.Tab(label='Statistics', children=[
                          html.Div([
						  
                                html.P("Select rows from table and methods from dropdown to binarize genes:"),
                                html.Div(id='statistics-page')

                            ]),

                      ]),

                      dcc.Tab(label='Network', children=[
                           html.Div([

                                    #html.P("Select rows from table and methods from dropdown to binarize genes:"),
                                    html.Div(id='net-tabs')
                                    
                                ], style={'display': 'flex', 'flexDirection': 'column', 'flex':1, 'width':'100%'})
                      ])
        ], style={'display': 'flex', 'flexDirection': 'row'}), html.Div(id='process-thr')]

# process the click of the download button
# gets the threshold of the data and downsloads as a csv
@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    Input('stored-data','data'), 
    Input('datatable-interactivity', 'selected_rows'),
    prevent_initial_call=True,
)
def download_csv(n_clicks, data, selected_rows):
    # no data return none
    if data is None:
        return None
    
    # get data
    df = pd.DataFrame(data)

    # if no clicks return none 
    if n_clicks is None:
        return None
    
    selected_rows.sort()
    
    # get the selected genes values
    genes = df.iloc[selected_rows].values
    rows = df.shape[0]
    
    # column names and creating dataframe
    col_names = {'basc_thr':[], 'kmeans_thr':[], 'onestep_thr':[], 'shmulevich_thr':[]}
    final_df = pd.DataFrame(col_names)

    
    # get threshold of selected rows and save to dataframe
    for i in range(len(selected_rows)):
            k_means = K_Means(genes[i])
            basc_a = BASC_A(genes[i])
            one_step = onestep(genes[i])
            shmulevich_ = shmulevich(genes[i])
            
            new_row = {'basc_thr':basc_a, 'kmeans_thr':k_means, 'onestep_thr':one_step, 'shmulevich_thr': shmulevich_}
            final_df.loc[len(final_df)] = new_row

    # send the dataframe and download it as thr.csv
    return dcc.send_data_frame(final_df.to_csv, "thr.csv")

# return dropdown component of binarization methods 
@app.callback(
    Output('dropdown-methods', 'children'),
    Input('datatable-interactivity', 'selected_rows'),
    prevent_initial_call=True)
def display_selected_data(selected_rows):
    # if no selected rows return none
    if not selected_rows:
        return None
    
    # return components of dropdown
    return  [html.B('Select binarization method(s) to calculate thresholds and binarize genes:'),
             html.Button('Select All', id='select-all-dropdown'), 
            dcc.Dropdown(
                ['BASC A', 'K-Means', 'Onestep', 'Shmulevich'],
                placeholder="Select binarization method",
                id="dropdown-method",
                multi=True,
                #persistence = True,
                #persistence_type = 'memory',
                searchable=False)]

@app.callback(
    Output('dropdown-method', 'value'),
    [Input('select-all-dropdown', 'n_clicks')]
)
def select_all(n_clicks):
    # if select all is not pressed do not update dash
    if n_clicks is None:
        return dash.no_update
    # if pressed select all the list of the dropdown
    else:
        return ['BASC A', 'K-Means', 'Onestep', 'Shmulevich']

# return component that has interpolation section description
@app.callback(
        Output('section-threshold', 'children'),
        Input('dropdown-selected-rows', 'value'),
        Input('dropdown-method', 'value'), 
        prevent_initial_call=True
)
def header(row, methods):
    # return none if values are none
    if row is None:
        return None
    if methods is None:
        return None
    
    # return components of section threshold
    return [html.Hr(),html.P("Spline approximation of gene expression and threshold displacement for every algorithm. The voting table shows the binarization using selected algorithms and the consensus binarization.", style={'textAlign': 'center'}),
            html.Br(), html.P("*Values that are too close to the threshold will be considered undecided with a (?) on the table.")]

    #update global variable interpolation
    #_, splineGene = three_interpolation(row.values,'K-Means',4)

# returns a dropdown of the selected rows of the datatable 
@app.callback(
    Output('select-gene-binarize', 'children'),
    Input('dropdown-method', 'value'),
    Input('datatable-interactivity', 'selected_rows'),
    Input('stored-data','data'),     
    prevent_initial_call=True)
def select_gene_binarize(selected_method, selected_rows, data):
    # return none if values are none
    if selected_method is None:
        return None

    if selected_rows is None:
        return None
    
    selected_rows.sort()

    # return dropdown of the select gene
    return [html.B('Select gene to visualize and binarize:'), dcc.Dropdown(
        options=[{'label': 'Gene ' + str(row+1), 'value': row} for row in selected_rows], 
        value = selected_rows[0],
        placeholder="Select rows",
        id="dropdown-selected-rows")]
    

# returns a dropdown to select the number of iterations to interpolate
@app.callback(
    Output('range-table', 'children'),
    Input('dropdown-selected-rows', 'value'),
    Input('dropdown-method', 'value'), 
    Input('stored-data','data'),
    prevent_initial_call=True)
def range_table(selected_row, selected_method, data):
    # return none if values are none
    if selected_row is None:
        return None
    if selected_method is None:
        return None
    if data is None:
        return None
    
    # get dataframe 
    df = pd.DataFrame(data)
    
    # get selected gene
    selected = df.iloc[selected_row]
    
    gene = selected.values
    # return dropdown of number of interpolations
    generange = max(gene) - min(gene)
    #minus 1 cos zero index
    rangeNum = math.ceil(generange*10)-1
    disp = displacements[['range','k-means','BASC_A', 'onestep', 'shmulevich']]
    disp.reset_index(drop=True, inplace=True)
    
    
    return  [html.B('Estimated displacement for range of gene.'), 
            dash_table.DataTable(
            data=disp.astype(dtype='float32').astype('str').to_dict('records'),
            page_size= 10,
            style_data_conditional=[{
            "if": {"row_index": rangeNum},
            "backgroundColor": "#cce0ff",
            "fontWeight": "bold"
            }],
            )]


@app.callback(
    Output('process-thr', 'children'),
    Input('dropdown-method', 'value'),
    Input('datatable-interactivity', 'selected_rows'),
    Input('stored-data','data'),
    prevent_initial_call=True)
def save_thr(selected_method, selected_rows, data):

    if selected_method is None:
        return None
    if selected_rows is None:
        return None
    if data is None:
        return None

    df1 = pd.DataFrame(data)

    thr_k = {}
    thr_b = {}
    thr_o = {}
    thr_s = {}

    splineDict = {}

    for row in selected_rows:
        selected = df1.iloc[row]
        gene = selected.values

        _, splineGene = three_interpolation(gene,'K-Means',4)

        splineDict[row] = splineGene


    for method in selected_method:

        for row in selected_rows:
            #selected = df1.iloc[row]
            #gene = selected.values

            #_, splineGene = three_interpolation(gene,method,4)

            #splineDict[row] = splineGene

            splineGene = splineDict[row]

            if(method == 'BASC A'):
                thr = call_C_BASC(splineGene)

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

    #print(thr_k)

    return [dcc.Store(id='thr_k', data=thr_k), dcc.Store(id='thr_o', data=thr_o), 
            dcc.Store(id='thr_b', data=thr_b), dcc.Store(id='thr_s', data=thr_s),
            dcc.Store(id='BASC A-datatable-network', data=[]), dcc.Store(id='K-Means-datatable-network', data=[]),
            dcc.Store(id='Onestep-datatable-network', data=[]), dcc.Store(id='Shmulevich-datatable-network', data=[]),
            dcc.Store(id='rule_network_dict', data=[]), dcc.Store(id='Elected States-datatable-network', data=[]),
            dcc.Store(id='spline-genes', data=splineDict)]



          

# returns a tab component with the threshold and interpolation displacement tabs and graphs
@app.callback(
    Output('threshold-tabs', 'children'),
    Input('dropdown-method', 'value'),
    Input('dropdown-selected-rows', 'value'), 
    Input('stored-data','data'),
    Input('thr_k','data'),
    Input('thr_o','data'),
    Input('thr_s','data'),
    Input('thr_b', 'data'),
    Input('spline-genes', 'data'),
    prevent_initial_call=True)

def threshold_tabs(selected_method, selected_gene, data, thr_k, thr_o, thr_s, thr_b, spline_genes):

    # return none if values are none
    if selected_method is None:
        return None
    if selected_gene is None:
        return None
    if data is None:
        return None
        
    selected_row = selected_gene
    #graph 1
    
    # get dataframe 
    df1 = pd.DataFrame(data)
    
    # get selected gene
    selected = df1.iloc[selected_gene]
    
    gene = selected.values
    sizeGene = len(gene)
    
    ogGene = pd.DataFrame({'x':np.arange(0,sizeGene),'y':gene, 'label': [f'Gene {str(selected_gene+1)}']* sizeGene})
    
    #_, splineGene = three_interpolation(gene,'K-Means',4)
    splineGene = spline_genes[str(selected_gene)]
    
    gene_iter = splineGene 
    index = 0
    
    size_new = len(splineGene)

    dataset_gene = pd.DataFrame({'x':np.linspace(0,sizeGene-1,size_new),'y':gene_iter, 'label': [f'Gene {str(selected_gene+1)} Spline']* size_new})
        
    data1 = alt.Chart(
            dataset_gene
        ).mark_line().encode(
                x=alt.X('x',title='Timeseries'),
                y=alt.Y('y').scale(zero=False),
                color='label'
        ).interactive()
        
    
    ogChart = alt.Chart(
        ogGene
    ).mark_line(point=True).encode(
                x=alt.X('x'),
                y=alt.Y('y').scale(zero=False),
                tooltip=['y','label'],
                color='label'
    ).interactive()


    thr_basc = 0
    thr_kmeans = 0
    thr_onestep = 0
    thr_shmu = 0
    
    for method in selected_method:

        if(method == 'BASC A'):
             

            #thr_basc = BASC_A(splineGene)
            thr_basc = thr_b[str(selected_gene)]
            #thr_a, gene_iter = three_interpolation(gene, method, 4)
            
            datas = pd.DataFrame({'x':np.linspace(0,sizeGene-1,size_new),'y':np.full(size_new, thr_basc), 'label': ["BASC A"]* size_new})
            
            lines = alt.Chart(datas).mark_line(strokeDash=[2,1],color='red').encode(
                    x=alt.X('x'),
                    y=alt.Y('y').scale(zero=False),
                    tooltip=['y','label'],
                    color='label'
                    ).interactive()
              
            data1 = data1 + lines
            #data1.add_trace(go.Scatter(x=np.arange(1,size_new+1), y=np.full(size_new, thr_a[-1]), line=dict(dash=type_lines[index]),
            #                        mode="lines", name="BASC A Threshold"))

        elif(method == 'Onestep'):
         
            #thr_onestep = onestep(splineGene)
         
            thr_onestep = thr_o[str(selected_gene)]
            
            datas = pd.DataFrame({'x':np.linspace(0,sizeGene-1,size_new),'y':np.full(size_new, thr_onestep),'label': ["Onestep"]* size_new})
            
            lines = alt.Chart(datas).mark_line(strokeDash=[8,8], color='purple').encode(
                    x=alt.X('x'),
                    y=alt.Y('y').scale(zero=False),
                    tooltip=['y','label'],
                    color='label'
                    ).interactive()
              
            data1 = data1 + lines
            
            #data1.add_trace(go.Scatter(x=np.arange(1,size_new+1), y=np.full(size_new, thr_a[-1]), line=dict(dash=type_lines[index]),
            #                        mode="lines", name="Onestep Threshold"))


        elif(method == 'Shmulevich'):
         
            #thr_shmu = shmulevich(splineGene)
            thr_shmu = thr_s[str(selected_gene)]
            #thr_a, gene_iter = three_interpolation(gene, method, 4)
            
            datas = pd.DataFrame({'x':np.linspace(0,sizeGene-1,size_new),'y':np.full(size_new, thr_shmu), 'label': ["Shmulevich"]* size_new})
            
            lines = alt.Chart(datas).mark_line(strokeDash=[4,2],color='orange').encode(
                    x=alt.X('x'),
                    y=alt.Y('y').scale(zero=False),
                    tooltip=['y','label'],
                    color='label'
                    ).interactive()
              
            data1 = data1 + lines
            
            #data1.add_trace(go.Scatter(x=np.arange(1,size_new+1), y=np.full(size_new, thr_a[-1]), line=dict(dash=type_lines[index]),
            #                        mode="lines", name="Shmulevich Threshold"))


        elif(method == 'K-Means'):
      
            #thr_kmeans = K_Means(splineGene)
            thr_kmeans = thr_k[str(selected_gene)]
            #thr_a, gene_iter = three_interpolation(gene, method, 4)
            
            datas = pd.DataFrame({'x':np.linspace(0,sizeGene-1,size_new),'y':np.full(size_new, thr_kmeans), 'label': ["K-Means"]* size_new})
            
            lines = alt.Chart(datas).mark_line(strokeDash=[8,4], color='green').encode(
                    x=alt.X('x'),
                    y=alt.Y('y').scale(zero=False),
                    tooltip=['y','label'],
                    color='label'
                    ).interactive()
              
            data1 = data1 + lines
            
            #data1.add_trace(go.Scatter(x=np.arange(1,size_new+1), y=np.full(size_new, thr_a[-1]), line=dict(dash=type_lines[index]),
            #                        mode="lines", name="K-Means Threshold"))
            
        index += 1

    data1 = data1 + ogChart
    #add legend and title to plot
    data1 = data1.properties(
        title=f'Threshold for Gene {str(selected_gene+1)}',
        width=300,
        height=350
    ).configure_axis(grid=False)
	
    
    
    #graph 2
    rangeIndex = math.ceil((max(gene)-min(gene))*10) - 1
    disps = getDisplacement(selected_method,gene)
    
    
    # if tolerance is not None:
        
        # # get data
    df = pd.DataFrame(data)

        # # set the subplot grid layout
    if len(selected_method) == 1:
        row_n = 1
        col_n = 1
    elif len(selected_method) == 2:
        row_n = 1
        col_n = 2
    else:
        row_n = 2
        col_n = 2
        
        # # create sunplot layout
        # #fig = make_subplots(rows=row_n, cols=col_n, shared_xaxes=False, shared_yaxes=False, subplot_titles=(["Displacement " + m for m in selected_method]))
	#
    #iter_row = 1

    # # types of lines
    type_lines = ["dash", "dot", "dashdot", "longdash"]

    index = 0
        
    # # go through each method, interpolate and create plots
    
    # #create dataset for altair use
    # #2d dataset
    # #create labels dataframe
    
    dataset_gene = pd.DataFrame()
    n = len(gene)
    
    for method in selected_method:

        # # get genes
        selected = df.iloc[selected_row]
        gene = selected.values
        sizeGene = len(gene)
        
        #_, splineGene = three_interpolation(gene,method,4)
        
        #get min and max
        
        if method == 'K-Means':
            #thr = K_Means(splineGene)
            thr = thr_kmeans
            d = disps['k-means']
        elif method == 'BASC A':
            #thr = BASC_A(splineGene)
            thr = thr_basc
            d = disps['BASC_A']
        elif method == 'Onestep':
            #thr = onestep(splineGene)
            thr = thr_onestep
            d = disps['onestep']
        else:
            #thr = shmulevich(splineGene)
            thr = thr_shmu
            d = disps['shmulevich']
            
        thrMin = thr - d.iloc[0]
        thrMax = thr + d.iloc[0]

        if thrMax > max(gene):
            thrMax = max(gene)
        
        if thrMin < min(gene):
            thrMin = min(gene)
        
        # #assign vars
        x = np.arange(0,sizeGene)
        y = gene
        methods_data = [method] * n
        min_data = [thrMin] * n
        max_data = [thrMax] * n
        thr_data = [thr] * n
        
        # #create dataset
        dataset = {'x':x,'y':y,'mn':min_data,'mx':max_data,'thr':thr_data,'label':methods_data}
        
        # #append dict to list
        
        dataset_gene = pd.concat([dataset_gene, pd.DataFrame(dataset)])


    # #altair create chart
    # #gene line
    
    if col_n == 2 and row_n == 2:
        wd = 200
        hg = 200
    elif col_n == 2:
        wd = 200
        hg = 350
    else:
        wd = 300
        hg = 350
    
    
    
    
    gene_chart = alt.Chart().mark_line(point=True,strokeWidth=1.5).encode(
            x=alt.X('x:Q',title='', axis=alt.Axis(format=",.0f")),
            y=alt.Y('y:Q',title='displ, thr').scale(zero=False),
            tooltip=['y'],
    ).properties(
    width=wd,
    height=hg
    )
    
    # #thresholdline 
    
    lines = alt.Chart().mark_line(strokeWidth=1).encode(
                x='x',
                y=alt.Y('thr:Q'),
                tooltip=['thr'], 
                color='label'
                ).properties(
    width=wd,
    height=hg
    )
                    
    
    # #shading rectangles
                              
    displacement_chart = alt.Chart().mark_area(opacity=0.2).encode(                          
                    x ='x:Q',
                    y ='mn:Q',
                    y2 ='mx:Q',
                    color='label:N',
                    tooltip=['mx','mn']
                    ).properties(
    width=wd,
    height=hg
    )
    
    # #combine all with facet 
    
    #fig = displacement_chart
    
    fig = alt.layer(gene_chart, displacement_chart, data=dataset_gene).facet(facet='label:N',columns=col_n).configure_headerFacet(title=None).configure_axis(grid=False)
    #fig.encoding.y.title = 'displ'
	

    # # return the components if the number of interpolations and selected gene are not empty
    #fig = alt.layer(gene_chart, displacement_chart, lines, data=dataset_gene).facet(facet='label:N',columns=col_n

        # return [ dcc.Tabs([
                        # dcc.Tab(label='Thresholds', children=[

                            # html.P("Thresholds for each algorithm on selected gene."),
                            # dvc.Vega(
                                # id="altair0",
                                # opt={"renderer": "svg", "actions": False},
                                # spec=data1.to_dict(),
                            # ),
                    # ]),

                        # dcc.Tab(label='Interpolation Thresholds', children=[
                            
                            # html.P("Graph of thresholds over interpolation for selected algorithms."),
                            # dvc.Vega(
                                # id="altair0",
                                # opt={"renderer": "svg", "actions": False},
                                # spec=fig.to_dict(),
                            # ),
                    # ])
                # ])             
                        
                # ]
    
    # return only the selected gene plot with threshold if number of interpolation is not selected
    if(selected_row is not None):

        return [ dcc.Tabs([
                        dcc.Tab(label='Thresholds', children=[

                            html.P("Threshold for each algorithm on selected gene."),
                            dvc.Vega(
                                id="altair0",
                                opt={"renderer": "svg", "actions": False},
                                spec=data1.to_dict(),
                            )
                    ]),
                    dcc.Tab(label='Displacements', children=[
                            
                            
                            dvc.Vega(
                                id="altair0",
                                opt={"renderer": "svg", "actions": False},
                                spec=fig.to_dict(),
                            ),
                    ])
                
                ])                   
                ]
    
    # return nothing
    else:
        return None
    


# returns the tabs of networks graphs per algoritms and final vote 
@app.callback(
    Output('net-tabs', 'children'),
    Input('dropdown-method', 'value'), 
    Input('stored-data','data'),
    Input('datatable-interactivity', 'selected_rows'),
    Input('thr_k','data'),
    Input('thr_o','data'),
    Input('thr_s','data'),
    Input('thr_b', 'data'),
    #Input('dropdown-tolerance', 'value'),
    #[Input({'type': 'dropdown-rule', 'index': dash.dependencies.ALL}, 'value')],
    #[Input('stored-rules', 'data')],
    prevent_initial_call=True)
def net_tabs(selected_method, data, selected_rows, thr_k, thr_o, thr_s, thr_b, tolerance=4):
    #if len(values) == 0 or None in values:
    #    return None

    # if these values are none return none to the dashboard
    if selected_method is None:
        return None
    if data is None:
        return None
    if selected_rows is None:
        return None
    
    selected_rows.sort()

    #get the plot, and network of the final vote plot
    elected_state_network = create_boolean_network_votes(selected_rows, data, selected_method, displacements, thr_k, thr_o, thr_s, thr_b)

    dcc.Store(id='Elected States-datatable-network', data=elected_state_network)

    transition = []

    for method in selected_method:

        network = create_boolean_network(selected_rows, method, data, displacements, thr_k, thr_o, thr_s, thr_b)

        transition.append(transition_table(network, method))

        #network_plots.append(
        #        html.Div(
        #                children=[
        #                        html.B(method),
        #                        html.Iframe(
        #                            srcDoc=fig2.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
        #                            width="500px", height="500px",
        #                        )
        #                    ], style={'display': 'flex', 'flexDirection': 'column'}

        #                )
        #)

    if len(selected_method) > 2:
 
        #network_plots = html.Div([html.Div(network_plots[:2]), html.Div(network_plots[2:])], style={'display': 'flex', 'flexDirection': 'row'})

        transition_df = html.Div([html.Div(transition[:2]), html.Div(transition[2:])], style={'display': 'flex', 'flexDirection': 'row'})

    else:
        transition_df = html.Div(transition[:2])

        #network_plots = html.Div([html.Div(network_plots)], style={'display': 'flex', 'flexDirection': 'row'})


     # component of final transition table
    final_transition_df = transition_table(elected_state_network, "Elected States")

    #html.Div(
    #    children=[
    #        html.Iframe(
    #            srcDoc=fig2, # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
    #            style={"height": "25%", "width": "25%"},)])
    

    # return components and tabs 
    return [ dcc.Tabs([
                    
                    dcc.Tab(label='Networks', children=[

                        html.P("Networks of methods"),
                        html.Div(id='methods-networks')

                        #html.Div([
                        #    html.P("Networks of methods"),
                            #html.Div(id='graph_rules', src=fig2, style={'height':'100%', 'width':'100%'}),
                        #    html.Div(network_plots),

                        #    html.Div([
                        #        html.B('Network of Elected States'),
                        #        html.Iframe(
                        #                srcDoc=fig.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                        #                width="500px", height="500px")
                        #    ], style={'display': 'flex', 'flexDirection': 'column'}),
                            
                
                        #], style={'display': 'flex', 'flexDirection': 'column'})
                    ]),
                        
                        dcc.Tab(label='Network State Table', children=[
                            html.Br(),

                            html.Div([transition_df, final_transition_df], style={'display': 'flex', 'flexDirection': 'row'}),
                            
                            
                        ]),

                     dcc.Tab(label='Upload Transition', children=[

                            html.P("Upload transition rules to create network"),
                            dcc.Upload(
                                        id='upload-rules',
                                        children=html.Button("Upload Rules"),
                                        multiple=False,
                                    ),
                            
                            html.Div(id='output-rules-upload'),
                            html.Div(id='generate-network')
                   
                          
                    ]),


                    #dcc.Tab(label='Analysis', children=[

                    #        html.P("Upload transition rules to see network analysis"),
                        
                    #        html.Div(id='analysis-output')
                   
                          
                    #]),

                ])             
                        
    ]

@app.callback(
    Output('methods-networks', 'children'),
    #Input('datatable-interactivity', 'selected_rows'),
    Input('dropdown-method', 'value'), 
    #Input('stored-data','data'),
    #Input('thr_b','data'),
    #Input('thr_k','data'),
    #Input('thr_s','data'),
    #Input('thr_o','data'),
    Input('BASC A-datatable-network', 'data'),
    Input('K-Means-datatable-network', 'data'),
    Input('Onestep-datatable-network', 'data'),
    Input('Shmulevich-datatable-network', 'data'),
    Input('Elected States-datatable-network', 'data'),
    prevent_initial_call=False)
def create_bool(methods, basc, kmeans, onestep, shmulevich, elected_network):


    #print("aqui", methods, basc)
    if methods is None:
            return "blah"
    
    network_plots = []

    for method in methods:

        if method == "BASC A":
            data = pd.DataFrame(basc)
        elif method == 'K-Means':
            data = pd.DataFrame(kmeans) 
        elif method == 'Onestep':
            data = pd.DataFrame(onestep)
        elif method == 'Shmulevich':
            data = pd.DataFrame(shmulevich)
        

        fig2, _ = create_boolean_network_graph(data)

        #transition.append(transition_table(network, method))

        network_plots.append(
                    html.Div(
                            children=[
                                    html.B(method),
                                    html.Iframe(
                                        srcDoc=fig2.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                        width="500px", height="500px",
                                    )
                                ], style={'display': 'flex', 'flexDirection': 'column'}

                            )
            )


    if len(methods) > 2:
 
        network_plots = html.Div([html.Div(network_plots[:2]), html.Div(network_plots[2:])], style={'display': 'flex', 'flexDirection': 'row'})
    

    else:

        network_plots = html.Div([html.Div(network_plots)], style={'display': 'flex', 'flexDirection': 'row'})


    fig, _ = create_boolean_network_graph_votes(elected_network)

    return    html.Div([
                            html.P("Networks of methods"),
                            #html.Div(id='graph_rules', src=fig2, style={'height':'100%', 'width':'100%'}),
                            html.Div(network_plots),

                            html.Div([
                                html.B('Network of Elected States'),
                                html.Iframe(
                                        srcDoc=fig.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                        width="500px", height="500px")
                            ], style={'display': 'flex', 'flexDirection': 'column'}),
                            
                
                ], style={'display': 'flex', 'flexDirection': 'column'})

@app.callback(
    Output('save-basc-states', 'children'),
    Input('BASC A-datatable-network', 'data'),
    prevent_initial_call=True)
def save_basc_states(basc):

    dcc.Store(id='BASC A-datatable-network', data=pd.DataFrame(basc))

@app.callback(
    Output('save-kmeans-states', 'children'),
    Input('K-Means-datatable-network', 'data'),
    prevent_initial_call=True)
def save_kmeans_states(kmeans):

    dcc.Store(id='K-Means-datatable-network', data=pd.DataFrame(kmeans))


@app.callback(
    Output('save-onestep-states', 'children'),
    Input('Onestep-datatable-network', 'data'),
    prevent_initial_call=True)
def save_onestep_states(onestep):

    dcc.Store(id='Onestep-datatable-network', data=pd.DataFrame(onestep))


@app.callback(
    Output('save-shmulevich-states', 'children'),
    Input('Shmulevich-datatable-network', 'data'),
    prevent_initial_call=True)
def save_shmulevich_states(shmulevich):

    dcc.Store(id='Shmulevich-datatable-network', data=pd.DataFrame(shmulevich))

@app.callback(
    Output('save-elected-states', 'children'),
    Input('Elected States-datatable-network', 'data'),
    prevent_initial_call=True)
def save_elected_states(states_network):

    dcc.Store(id='Elected States-datatable-network', data=pd.DataFrame(states_network))

#@app.callback(
#    Output('save-rules', 'children'),
#    Input('stored-rules', 'data'),
#    prevent_initial_call=True)
#def save_elected_states(rules):

#    print(rules)

#    dcc.Store(id='stored-rules', data=rules)

    
@app.callback(
    Output('generate-network', 'children'),
    Input('datatable-interactivity', 'selected_rows'),
    Input('dropdown-method', 'value'), 
    Input('stored-data','data'),
    Input('stored-rules','data'),
    Input('thr_b','data'),
    Input('thr_k','data'),
    Input('thr_s','data'),
    Input('thr_o','data'),
    prevent_initial_call=True)
def rules_network(rows, methods, data, rules, thr_b, thr_k, thr_s, thr_o):

    if rows is None and methods is None and data is None and rules is None:
        return None
    
    #print(rules)
    
    df = pd.DataFrame(rules)
    #df.columns = df.iloc[0]
    #dfa = df[1:]
    
    net, dict_net = createNetwork(df)

    #print(df)

    return  html.Div([
                    #html.B("Table of Rules"),
                    #dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], editable=True, id="stored-rules"),
                    html.B("Network Based on Rules"),
                    dcc.Store(id='rule_network_dict', data=dict_net),
                    html.Iframe(
                                    srcDoc=net.generate_html(), # here https://stackoverflow.com/questions/68269257/local-html-file-wont-load-properly-into-dash-application
                                    width="500px",
                                    height="500px"
                    )
                ], style={'display': 'flex', 'flexDirection': 'column'})
                    

@app.callback(
    Output('analysis-output', 'children'),
    Input('dropdown-method', 'value'), 
    Input('BASC A-datatable-network', 'data'),
    Input('K-Means-datatable-network', 'data'),
    Input('Onestep-datatable-network', 'data'),
    Input('Shmulevich-datatable-network', 'data'),
    Input('rule_network_dict', 'data'),
    Input('Elected States-datatable-network', 'data'),
    prevent_initial_call=False)   
def generate_analysis(methods, basc, kmeans, onestep, shmulevich, rule_network, elected_network):

    if methods is None or len(elected_network) == 0 or len(rule_network) == 0:
        return None
    
    df = pd.DataFrame()

    data_algos = pd.DataFrame()

    #print(rule_network, kmeans)

    #return [dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]),
    #        dash_table.DataTable(data_algos.to_dict('records'), [{"name": i, "id": i} for i in data_algos.columns])]

    for method in methods:

        if method == "BASC A":
            data = turn_df_to_array(basc)
            df_analysis = hamming_state_by_state(rule_network, data, method)

            df_bin = pd.DataFrame({method:data})
            data_algos = pd.concat([data_algos, df_bin], axis=1)

        elif method == 'K-Means':
            data = turn_df_to_array(kmeans) 
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

    
    df_init_final = generate_init_final_comparison(data_algos, rule_network)

    df_chain_elected, cond = hamming_chain(rule_network, turn_df_to_array(elected_network))

    if cond == False:

        chain_hamming = html.P("Cannot analyze network because initial state does not exist in Boolean Function Network")

    else:

        chain_hamming = dash_table.DataTable(df_chain_elected.to_dict('records'), [{"name": i, "id": i} for i in df_chain_elected.columns])


    return [dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]),
           chain_hamming,
           dash_table.DataTable(df_init_final.to_dict('records'), [{"name": i, "id": i} for i in df_init_final.columns])]


def turn_df_to_array(df):

    array_net = []

    df = pd.DataFrame(df)

    for index, row in df.iterrows():
        r = row.values
        
        result = ''.join(map(str, r))
        
        array_net.append(result)

    return array_net

# returns a datatable with the voting table with the selected methods         
@app.callback(
    Output('voting-output', 'children'),
    Input('dropdown-selected-rows', 'value'),
    Input('dropdown-method', 'value'), 
    Input('stored-data','data'),
    Input('thr_b','data'),
    Input('thr_k','data'),
    Input('thr_s','data'),
    Input('thr_o','data'),
    prevent_initial_call=True)
def vote_table(row, selected_method, data, thr_b, thr_k, thr_s, thr_o):
    
    # if they are none return nothing to the dashboard
    if row is None or selected_method is None or data is None:
        return None
    
    # get dataframe
    df = pd.DataFrame(data)
    
    # get selected gene
    selected = df.iloc[row]
    gene = selected.values
       
    selected_range = max(gene) - min(gene)
    disps = getDisplacement(selected_method,gene)
    
    range_displacement_index = math.ceil((max(gene)-min(gene))*10) - 1
    #ranges is a pandas series object
    #ranges = displacements.iloc[range_displacement_index]

    #_, geneSpline = three_interpolation(gene, 'K-Means', 4)
     
    t = []
    d = []

    vote_binary = []
    
    # go through each method and interpolate n times given by the user
    for method in selected_method:
        if(method == 'BASC A'):
            # get threshold of orignal gene
            t.append(thr_b[str(row)])
            #t.append(BASC_A(geneSpline))

            # get list of thresholds by the interpolations
            #t_b, _ = interpolationConverge(gene, 'BASC A', tolerance)
            
            # add displacement 
            d.append(disps['BASC_A'].iloc[0])

            # get vote of method
            #vote_binary.append(binVoting(gene, [BASC_A(gene)], [max(t_b) - min(t_b)]))

            
        elif(method == 'K-Means'):
            # get threshold of orignal gene
            t.append(thr_k[str(row)])
            #t.append(K_Means(geneSpline))

             # get list of thresholds by the interpolations
            #t_k, _ = interpolationConverge(gene, 'K-Means', tolerance)
            
             # add displacement 
            #d.append(max(t_k) - min(t_k))

            d.append(disps['k-means'].iloc[0])
            # get vote of method
            #vote_binary.append(binVoting(gene, [K_Means(gene)], [max(t_k) - min(t_k)]))
            
            
        elif(method == 'Onestep'):
            # get threshold of orignal gene
            t.append(thr_o[str(row)])
            #t.append(onestep(geneSpline))

            # get list of thresholds by the interpolations
            #t_o, _ = interpolationConverge(gene, 'Onestep', tolerance)
            
            # add displacement 
            #d.append(max(t_o) - min(t_o))

            d.append(disps['onestep'].iloc[0])
            # get vote of method
            #vote_binary.append(binVoting(gene, [onestep(gene)], [max(t_o) - min(t_o)]))
            
        else:
            # get threshold of orignal gene
            t.append(thr_s[str(row)])
            #t.append(shmulevich(geneSpline))

            # get list of thresholds by the interpolations
            #t_s, _ = interpolationConverge(gene, 'Shmulevich', tolerance)
            
            d.append(disps['shmulevich'].iloc[0])
            # add displacement 
            #d.append(max(t_s) - min(t_s))

            # get vote of method
            #vote_binary.append(binVoting(gene, [shmulevich(gene)], [max(t_s) - min(t_s)]))
   
    # find the voting table of that gene 
    votes = binarizationVoting(gene, t, d)
    
    # save votes
    #votes = [vote_binary]

    #hamming, size_vect = HammingDistance(votes)

    #hamming_vect = [[hamming]]

    #ham_col = ['Hamming Distance']

    # add final vote of all algos
    #votes.append(binVoting(gene, t, d))
    
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


    #ham_df = pd.DataFrame(data=hamming_vect, index=ham_col)
    #ham_df.reset_index(inplace=True)


    # return components and table 
    return [ html.Div(style={'height': '5%'}), html.B('Voting Table of Gene ' + str(row+1)), 
            dash_table.DataTable(vote_df.to_dict('records'), [{"name": i, "id": i} for i in vote_df.columns],
            style_data = {'borderBottom': '5px solid white'},
            style_cell={'minWidth': '50px', 'maxWidth': '50px'},
            style_data_conditional=[
               {
                   'if': {
                       'filter_query': '{{{col}}} = "?"'.format(col=col),
                       'column_id': col,
                       'row_index': 'odd'
                   },
                   #'backgroundColor': 'rgb(220, 220, 220)'
                   'backgroundColor': 'rgb(255, 255, 192, 0.3)',
                   #'color': 'rgb(255, 255, 192, 0.3)',
               } for col in vote_df.columns
            ] +
            [
               {
                   'if': {
                       'filter_query': '{{{col}}} = "?"'.format(col=col),
                       'column_id': col,
                       'row_index': 'even'
                   },
                   #'color': 'rgb(255, 255, 192, 0.5)',
                   'backgroundColor': 'rgb(255, 255, 192, 0.3)',
               } for col in vote_df.columns
            ] +
            
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 1'.format(col=col),
                        'column_id': col,
                        'row_index': 'odd'
                    },
                    #'backgroundColor': 'rgb(220, 220, 220)',
                    #'color': 'rgb(13, 45, 27)',
                    'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                } for col in vote_df.columns
            ] +
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 0'.format(col=col),
                        'column_id': col,
                        'row_index': 'odd'
                    },
                    #'backgroundColor': 'rgb(220, 220, 220)',
                    #'color': 'rgb(55, 15, 15)',
                    'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                } for col in vote_df.columns
            ] +
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 0'.format(col=col),
                        'column_id': col,
                        'row_index': 'even'
                    },
                    #'color': 'rgb(55, 15, 15)',
                    'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                } for col in vote_df.columns
            ] +
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 1'.format(col=col),
                        'column_id': col,
                        'row_index': 'even'
                    },
                    #'color': 'rgb(13, 45, 27)',
                    'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                } for col in vote_df.columns
            ],
            style_table={'height': '300px', 'overflowY': 'auto', 'overflowX':'auto'}
            ), 
            
            #dash_table.DataTable(ham_df.to_dict('records'), [{"name": i, "id": i} for i in ham_df.columns])
            ]



# returns datatable with the transition table of each method
# this is for the networks of each method
def transition_table(final, method):
     # if no final network return none
    if final is None:
        return None
    
    tables = []

    label = method + '-datatable-network'
    
    # create datatable component of final transition table
    table = dash_table.DataTable(final.to_dict('records'), [{"name": i, "id": i} for i in final.columns],
    editable=True, id=label,
    #dropdown={
    #        i: {
    #            'options': [{'label': "0", 'value': "0"}, {'label': "1", 'value': "1"}, {'label': "?", 'value': "?"}]
    #        } for i in final.columns
    #        },
    style_data = {'borderBottom': '5px solid white'},
    style_data_conditional=[
               {
                   'if': {
                       'filter_query': '{{{col}}} = "?"'.format(col=col),
                       'column_id': col,
                       'row_index': 'odd'
                   },
                     #'backgroundColor': 'rgb(220, 220, 220)',
                     'backgroundColor': 'rgb(255, 255, 192, 0.3)',
               } for col in final.columns
            ] +
            [
               {
                   'if': {
                       'filter_query': '{{{col}}} = "?"'.format(col=col),
                       'column_id': col,
                       'row_index': 'even'
                   },
                  'backgroundColor': 'rgb(255, 255, 192, 0.3)',
               } for col in final.columns
            ] +
            
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 1'.format(col=col),
                        'column_id': col,
                        'row_index': 'odd'
                    },
                    #'backgroundColor': 'rgb(220, 220, 220)',
                    # 'color': 'rgb(13, 45, 27)',
                   'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                } for col in final.columns
            ] +
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 0'.format(col=col),
                        'column_id': col,
                        'row_index': 'odd'
                    },
                     #'color': 'rgb(55, 15, 15)',
                     #'backgroundColor': 'rgb(220, 220, 220)',
                     'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                } for col in final.columns
            ] +
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 0'.format(col=col),
                        'column_id': col,
                        'row_index': 'even'
                    },
                    #'color': 'rgb(55, 15, 15)',
                    'backgroundColor': 'rgb(191, 102, 99, 0.3)',
                } for col in final.columns
            ] +
            [
                {
                    'if': {
                        'filter_query': '{{{col}}} = 1'.format(col=col),
                        'column_id': col,
                        'row_index': 'even'
                    },
                     #'color': 'rgb(13, 45, 27)',
                     'backgroundColor': 'rgb(113, 209, 129, 0.3)',
                } for col in final.columns
            ] + [
            {
                'if': {
                'column_id': 'Hamming',
                    },
                    'backgroundColor': 'white',
            }],
            style_table={'height': '300px', 'overflowY': 'auto'})
    
    tables.append(html.Label(method))
    tables.append(table)
        
    # return table 
    return html.Div(tables, style={'margin': '20px'})


@app.callback(
    Output('statistics-page', 'children'),
    Input('dropdown-method', 'value'),
    Input('dropdown-selected-rows', 'value'), 
    Input('stored-data','data'),
    Input('thr_k','data'),
    Input('thr_o','data'),
    Input('thr_s','data'),
    Input('thr_b', 'data'),
    prevent_initial_call=True)
def statistics_page(selected_method, selected_gene, data, thr_k, thr_o, thr_s, thr_b):

    # return none if values are none
    if selected_method is None:
            return None
    if selected_gene is None:
            return None
    if data is None:
            return None

            
    #create dataframe to access gene
    df = pd.DataFrame(data)
    selected = df.iloc[selected_gene]
    gene = selected.values
    sizeGene = len(gene)
    ogGene = pd.DataFrame({'x':np.arange(0,sizeGene),'y':gene, 'label': [f'Gene {str(selected_gene+1)}']* sizeGene})

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


if __name__ == '__main__':
    app.run_server(debug=False)