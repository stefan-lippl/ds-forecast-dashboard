from dash import dash, Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import random


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
pred_coffee = dcc.Graph(config={'displayModeBar': False})
pred_cake = dcc.Graph(config={'displayModeBar': False})

# Home
history_cb = dcc.Checklist(
    [' Historical View'],
    id="history_cb"
)

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
    max_intervals=0,
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
            html.H5('Filter'),
            dbc.Col([history_cb]), 
            dbc.Col([html.H5('92%', style={'float': 'right', 'color': 'green'}), html.H5('Aktuelle Genauigkeit:  \t', style={'float': 'right'})])
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