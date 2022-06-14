from dash import dash, Dash, html, dcc, Input, Output, dash_table, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import random
import base64
import datetime
import io

from layouts.layout_navbar import LayoutNavbar


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = 'Forecast Dashboard'

########## HTML ##########
index_page = html.Div([
    dcc.Link('Go to Home', href='/home'),
    html.Br(),
    dcc.Link('Go to History', href='/history'),
    html.Br(),
    dcc.Link('Go to Data', href='/data')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

navbar_creator = LayoutNavbar()
navbar = navbar_creator.create()

##### DATA #####

df = pd.read_csv('data/Bakery.csv', index_col=0)
def dt(x):
    return str(x).split(' ')[0]
df['date'] = df.date.apply(dt)

### Components - Output ###
pred_bread = dcc.Graph(config={'displayModeBar': False})
pred_coffee = dcc.Graph(config={'displayModeBar': False})
pred_cake = dcc.Graph(config={'displayModeBar': False})


history_cb = dcc.Checklist(
    [' Historical View'],
    id="history_cb"
)

# within layout
load_interval = dcc.Interval(
    id="load_interval", 
    n_intervals=0, 
    max_intervals=0,
    interval=1
)


###################################################
##################### LAYOUT ######################
###################################################

################## LAYOUT - HOME ##################
home_layout = html.Div([
    navbar,
    html.Div([],id="hidden-div", style={"display":"none"}),

    html.Div([
        dbc.Row([
            dbc.Col([html.H5('Filter')]),
            dbc.Col([html.H5('92%', style={'float': 'right', 'color': 'green'}), html.H5('Aktuelle Genauigkeit:  \t', style={'float': 'right'})])
        ]),
        dbc.Row([
            dbc.Col([history_cb])
        ]),

        html.Hr(),

        dbc.Row([
            dbc.Col([
                html.H5('Bread: 32', style={'margin-bottom': '0px'}),
                pred_bread
            ]),
            dbc.Col([
                html.H5('Coffee: 54', style={'margin-bottom': '0px'}),
                pred_coffee
            ]),
            dbc.Col([
                html.H5('Cake: 12', style={'margin-bottom': '0px'}),
                pred_cake
            ])
        ]) 
    ], style={'margin': '20px'})
])





###################################################
#################### FUNCTIONS ####################
###################################################

################### HOME ##########################
@app.callback(Output(pred_bread, 'figure'),
              Output(pred_coffee, 'figure'),
              Output(pred_cake, 'figure'),
              Input(history_cb, 'value'))
def pred_graph(history):

    dfb = df.query('Items == "Bread"')
    dfb = pd.DataFrame(dfb.groupby('date').size()).reset_index()
    dfb = dfb.rename({0: 'true_values'}, axis=1)
    for i in range(len(dfb)):
        d = random.randint(-5, 5)
        dfb.loc[i, 'prediction'] = dfb.loc[i, 'true_values'] + d

    dfb = dfb[-10:]

    if history:
        fig = make_subplots(vertical_spacing = 0.005, rows=2, cols=1,
                        row_width=[0.3, 0.7])
    else:
        fig = make_subplots(rows=1, cols=1)

    bar_color = 'rgb(19, 216, 242)'
    prob_dist_color = 'rgb(63, 92, 196)'
    if history:
        figx = go.Bar(name='True Sales', x=dfb.date, y=dfb.true_values)
        fig.update_layout(xaxis={'side': 'top'})
        figy = go.Bar(name='Prediction', x=dfb.date, y=dfb.prediction, marker=dict(color=bar_color))
    figz = go.Scatter(y=[0,1,2,4,6,7,6,4,3,2,1], mode="lines", line_color=prob_dist_color)

    #fig.update_layout(autosize=False,height=300)
    if history:
        fig.add_trace(figx, row=1, col=1)
        fig.add_trace(figy, row=1, col=1)
        fig.add_trace(figz, row=2, col=1)
    else:
        fig.add_trace(figz, row=1, col=1)
    fig['layout'].update(margin=dict(l=0,r=0,b=0,t=30))

    # hide all the xticks
    fig.update_xaxes(showticklabels=False)
    fig.update_xaxes(showticklabels=True, row=2, col=1)
    fig.update_layout(showlegend=False)

    #####-----------------

    dfb = df.query('Items == "Coffee"')
    dfb = pd.DataFrame(dfb.groupby('date').size()).reset_index()
    dfb = dfb.rename({0: 'true_values'}, axis=1)
    for i in range(len(dfb)):
        d = random.randint(-5, 5)
        dfb.loc[i, 'prediction'] = dfb.loc[i, 'true_values'] + d

    dfb = dfb[-10:]

    if history:
        fig2 = make_subplots(vertical_spacing = 0.005, rows=2, cols=1,
                        row_width=[0.3, 0.7])
    else:
        fig2 = make_subplots(rows=1, cols=1)
    
    if history:
        figx2 = go.Bar(name='True Sales', x=dfb.date, y=dfb.true_values)
        fig2.update_layout(xaxis={'side': 'top'})
        figy2 = go.Bar(name='Prediction', x=dfb.date, y=dfb.prediction, marker=dict(color=bar_color))
    figz2 = go.Scatter(y=[0,1,2,3,4,5,10,15,14,12,3], mode="lines", line_color=prob_dist_color)

    if history:
        fig2.add_trace(figx2, row=1, col=1)
        fig2.add_trace(figy2, row=1, col=1)
        fig2.add_trace(figz2, row=2, col=1)
    else:
        fig2.add_trace(figz2, row=1, col=1)
    fig2['layout'].update(margin=dict(l=0,r=0,b=0,t=30))

    # hide all the xticks
    fig2.update_xaxes(showticklabels=False)
    fig2.update_xaxes(showticklabels=True, row=2, col=1)
    fig2.update_layout(showlegend=False)

    #####-----------------

    dfb = df.query('Items == "Cake"')
    dfb = pd.DataFrame(dfb.groupby('date').size()).reset_index()
    dfb = dfb.rename({0: 'true_values'}, axis=1)
    for i in range(len(dfb)):
        d = random.randint(-5, 5)
        dfb.loc[i, 'prediction'] = dfb.loc[i, 'true_values'] + d

    dfb = dfb[-10:]

    if history:
        fig3 = make_subplots(vertical_spacing = 0.005, rows=2, cols=1,
                        row_width=[0.3, 0.7])
    else:
        fig3 = make_subplots(rows=1, cols=1)

    if history:
        figx3 = go.Bar(name='True Sales', x=dfb.date, y=dfb.true_values)
        fig3.update_layout(xaxis={'side': 'top'})
        figy3 = go.Bar(name='Prediction', x=dfb.date, y=dfb.prediction, marker=dict(color=bar_color))
    
    figz3 = go.Scatter(y=[0,1,2,3,5,10,15,19,27,15,10,5,2], mode="lines", line_color=prob_dist_color)
  
    if history:
        fig3.add_trace(figx3, row=1, col=1)
        fig3.add_trace(figy3, row=1, col=1)
        fig3.add_trace(figz3, row=2, col=1)
    else:
        fig3.add_trace(figz3, row=1, col=1)

    fig3['layout'].update(margin=dict(l=0,r=0,b=0,t=30))

    # hide all the xticks
    fig3.update_xaxes(showticklabels=False)
    fig3.update_xaxes(showticklabels=True, row=2, col=1)
    fig3.update_layout(showlegend=False)

    return fig, fig2, fig3



# Update page by index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home_layout
    else:
        return home_layout




if __name__ == '__main__':
    app.run_server(debug=True)