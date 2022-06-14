from dash import dash, Dash, html, dcc, Input, Output, dash_table, State
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd
import random
import base64
import io

from layouts.analytics import LayoutAnalytics
from layouts.home import LayoutHome
from layouts.data import LayoutData
from layouts.analytics import LayoutAnalytics
from layouts.history import LayoutHistory

########## HTML ##########
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
ext_ss = [
    dbc.themes.BOOTSTRAP,
    FONT_AWESOME
]
app = dash.Dash(
    __name__,
    external_stylesheets=ext_ss,
    suppress_callback_exceptions=True
)

app.title = 'Bakery Demand'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

##### DATA #####
df = pd.read_csv('data/Bakery.csv', index_col=0)
def dt(x):
    return str(x).split(' ')[0]
df['date'] = df.date.apply(dt)

##### Components #####
# Home
output_graph_top10 = dcc.Graph(config={'displayModeBar': False})
rest_produkte = dcc.Graph(config={'displayModeBar': False})
turnover_graph = dcc.Graph(config={'displayModeBar': False})
pred_bread = dcc.Graph(config={'displayModeBar': False})
pred_coffee = dcc.Graph(config={'displayModeBar': False})
pred_cake = dcc.Graph(config={'displayModeBar': False})

history_cb = dcc.Checklist([' Historical View'], [' Historical View'])

filter_box = html.Div([
    html.H5('Filter'),
    history_cb
], id='filter_checklist', style={'display': 'block'})

uploader = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
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
        # Don't allow multiple files to be uploaded
        multiple=True
    )

location = dcc.Dropdown(
    ['Gesamt', 'Wallersdorf', 'Plattling', 'Deggendorf'],
    'Gesamt',
    placeholder="Location", 
    #multi=True,
    clearable=False, style={'width': '70%', 'display': 'inline-block'})

history_table = dash_table.DataTable(
        df.to_dict('records'), 
        [{"name": i, "id": i} for i in df.columns],
        page_size=10
    )

###################################################
##################### LAYOUT ######################
###################################################

### HOME ###
home = LayoutHome()
home_layout = home.create(history_cb=filter_box, pred_bread=pred_bread, pred_coffee=pred_coffee, pred_cake=pred_cake)

### DATA ###
data = LayoutData()
data_layout = data.create(uploader=uploader)

### ANALYTICS ###
analytics = LayoutAnalytics()
analytics_layout = analytics.create(location, output_graph_top10, turnover_graph, rest_produkte)

### HISTORY ###
history = LayoutHistory()
history_layout = history.create(df=df)



###################################################
#################### FUNCTIONS ####################
###################################################

### HOME ###
@app.callback(
   Output(component_id='filter_checklist', component_property='style'),
   [Input(component_id='filter_switch', component_property='on')])

def show_hide_element(on):
    if on:
        return {'display': 'block'}
    else:
        return {'display': 'none'}




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


### ANALYTICS ###
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

@app.callback(Output(turnover_graph, 'figure'), 
              Input('hidden-div', 'children'))
def turnover_graph__analytics(value):
    dfc = df.copy()
    ser_locations = dfc.groupby('location').size()

    fig = px.pie(dfc, values=ser_locations.values, names=ser_locations.index)
    return fig


### HISTORY ###
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
            page_size=15
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
            page_size=15
        )
        else:
            return dash_table.DataTable(
            new_df.to_dict('records'), 
            [{"name": i, "id": i} for i in new_df.columns],
            page_size=int(value)
            )


### DATA ###
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=10
        )
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


### NAVIGATION ### 
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home_layout
    if pathname == '/data':
        return data_layout
    if pathname == '/analytics':
        return analytics_layout
    elif pathname == '/history':
        return history_layout
    else:
        return home_layout


if __name__ == '__main__':
    app.run_server(debug=True)