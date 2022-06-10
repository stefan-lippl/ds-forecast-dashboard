from dash import dash, Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import base64
import random

from charts.charts import PlotlyCharts


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = 'Forecast Dashboard'

##### DATA #####

df = pd.read_csv('data/Bakery.csv', index_col=0)
def dt(x):
    return str(x).split(' ')[0]
df['date'] = df.date.apply(dt)

### Components - Output ###
output_graph_top10 = dcc.Graph(config={'displayModeBar': False})
rest_produkte = dcc.Graph(config={'displayModeBar': False})
turnover_graph = dcc.Graph(config={'displayModeBar': False})
pred_bread = dcc.Graph(config={'displayModeBar': False})

location = dcc.Dropdown(
    ['Gesamt', 'Wallersdorf', 'Plattling', 'Deggendorf'],
    'Gesamt',
    placeholder="Location", 
    #multi=True,
    clearable=False, style={'width': '70%', 'display': 'inline-block'})

# within layout
load_interval = dcc.Interval(
    id="load_interval", 
    n_intervals=0, 
    max_intervals=0, #<-- only run once
    interval=1
)

index_page = html.Div([
    dcc.Link('Go to Home', href='/home'),
    html.Br(),
    dcc.Link('Go to History', href='/history')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

history_table = dash_table.DataTable(
        df.to_dict('records'), 
        [{"name": i, "id": i} for i in df.columns],
        page_size=10
    )

navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/home")),
            dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
            dbc.NavItem(dbc.NavLink("History", href="/history")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Profil", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Robros - Dashboard",
        brand_href="/home",
        color="#30a3d1",
        dark=True,
        style={'box-shadow': '0px 0px 3px 0px #000000'}
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
            dbc.Col([]), 
            dbc.Col([html.H5('\t92%', style={'float': 'right', 'color': 'green'}), html.H5('Aktuelle Genauigkeit:  ', style={'float': 'right'})])
        ]),

        html.Hr(),

        dbc.Row([
            dbc.Col([
                pred_bread
            ]),
            dbc.Col([]),
            dbc.Col([])
        ]) 
    ], style={'margin': '20px'})
])

################## LAYOUT - ANALYTICS ##################
analytics_layout = html.Div([
    navbar,
    html.Div([],id="hidden-div", style={"display":"none"}),

    html.Div([
        html.H5('Filter'),
        dbc.Row([
            dbc.Col([location]), 
        ]),

        html.Hr(),

        dbc.Row([
            dbc.Col([output_graph_top10]), 
            dbc.Col([rest_produkte]),
        ], style={'margin-top': '10px'}),

        dbc.Row([turnover_graph])
    ], style={'margin': '20px'})
    
])

################## LAYOUT - HISTORY ##################
history_layout = html.Div([
    navbar,
    html.Div([
        html.H5('Filter'),
        dbc.Row([
            dbc.Col([dcc.Dropdown(options=[{'label':i, 'value':i} for i in df['Items'].unique()], id='items_dropdown', placeholder="Filter product", multi=True)]),
            dbc.Col([dcc.Dropdown([10, 15, 20, 25, 30, 35, 40, 45, 50], '10', id='table-count', placeholder="Orders per site")]),
            dbc.Col([dcc.Dropdown(options=[{'label':i, 'value':i} for i in df['location'].unique()], id='loc-history', placeholder='Location', multi=True)]) 
        ]),
        html.Div(id='table-container', style={'margin-top': '30px'})
    ], style={'margin': '20px'})
])


###################################################
#################### FUNCTIONS ####################
###################################################

################### HOME ##########################
@app.callback(Output(pred_bread, 'figure'),
              Input('hidden-div', 'children'))
def pred_graph(hidden):
    
    dfb = df.query('Items == "Bread"')
    dfb = pd.DataFrame(dfb.groupby('date').size()).reset_index()
    dfb = dfb.rename({0: 'true_values'}, axis=1)  # new method
    for i in range(len(dfb)):
        d = random.randint(-5, 5)
        dfb.loc[i, 'prediction'] = dfb.loc[i, 'true_values'] + d

    dfb = dfb[-10:]

    fig = make_subplots(vertical_spacing = 0.05, rows=2, cols=1)

    figx = go.Bar(name='True Sales', x=dfb.date, y=dfb.true_values)
    #figx.update_layout(yaxis_visible=False)
    figy = go.Bar(name='Prediction', x=dfb.date, y=dfb.prediction)
    #figy.update_layout(yaxis_visible=False)
    #figz = px.line(x=[0, 1, 2, 3, 4], y=[0, 2, 4, 3, 1], title='Life expectancy in Canada')
    figz = go.Scatter(y=[0, 2, 3, 2, 1], mode="lines")

    fig.add_trace(figx, row=1, col=1)
    fig.add_trace(figy, row=1, col=1)
    fig.add_trace(figz, row=2, col=1)
    #fig.update_layout(xaxis={'side': 'top'})
    fig.update_layout(title_text=f'Bread: 30')
    #fig.update_layout(xaxis_rangeslider_visible=True, xaxis_range=[10,100])
    #fig.update_xaxes(type="date", range=[-3,])
    fig['layout'].update(margin=dict(l=0,r=0,b=0,t=30))

    return fig


# Update page by index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home_layout
    if pathname == '/analytics':
        return analytics_layout
    elif pathname == '/history':
        return history_layout
    else:
        return home_layout


@app.callback(Output(output_graph_top10, 'figure'), 
              Output(rest_produkte, 'figure'),
              Input('hidden-div', 'children'),
              Input(location, 'value'))
def top_10_graph(hidden, location):
    dfc = df.copy()
    if location != 'Gesamt':
        dfc = dfc.query(f'location == "{location}"')

    ser_items_grouped = dfc.groupby(['Items']).size().sort_values(ascending=True)
    top_10_items = ser_items_grouped[-10:]
    rest_items = ser_items_grouped[:-10]
    
    output_graph_top10 = px.bar(top_10_items, y=top_10_items.index, x=top_10_items.values, text_auto='.2s', height=800)
    output_graph_top10.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    output_graph_top10.update_layout(title_text=f'Top 10 meistverkaufe Produkte',
                                     xaxis_title=f"Produkt",
                                     yaxis_title="Anzahl in Stk."
                                    )
    
    rest_produkte = px.bar(rest_items, y=rest_items.index, x=rest_items.values, text_auto='.2s', height=800)
    rest_produkte.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    rest_produkte.update_layout(title_text=f'Restlichen Produkte',
                                     xaxis_title=f"Produkt",
                                     yaxis_title="Anzahl in Stk.",
                                    )
    return output_graph_top10, rest_produkte


@app.callback(Output('table-container', 'children'),
              Input('table-count', 'value'),
              Input('items_dropdown', 'value'),)
def update_table_per_filters___history(value, value2):
    dfc = df.copy()
    new_df = pd.DataFrame()

    if value2 != None:
        for i in range(len(value2)):
            new_df = new_df.append(dfc.query(f'Items == "{value2[i]}"'))
    if len(new_df) == 0:
        if value == None:
            return dash_table.DataTable(
            dfc.to_dict('records'), 
            [{"name": i, "id": i} for i in dfc.columns],
            page_size=25
        )
        else:
            return dash_table.DataTable(
            dfc.to_dict('records'), 
            [{"name": i, "id": i} for i in dfc.columns],
            page_size=int(value)
    )
    else:
        if value == None:
            return dash_table.DataTable(
            new_df.to_dict('records'), 
            [{"name": i, "id": i} for i in new_df.columns],
            page_size=25
        )
        else:
            return dash_table.DataTable(
            new_df.to_dict('records'), 
            [{"name": i, "id": i} for i in new_df.columns],
            page_size=int(value)
            )


@app.callback(Output(turnover_graph, 'figure'), 
              Input('hidden-div', 'children'))
def turnover_graph__analytics(value):
    dfc = df.copy()
    ser_locations = dfc.groupby('location').size()

    fig = px.pie(dfc, values=ser_locations.values, names=ser_locations.index)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)