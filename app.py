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

from charts.bar_chart import PlotlyBarChart

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
pred_sandwitch = dcc.Graph(config={'displayModeBar': False})

#history_cb = dcc.Checklist([' Historical View'], [' Historical View'])
history_cb = dcc.RadioItems(['on',  'off'], 'on')

filter_box = html.Div([
    html.H5('Filter'),
    html.P('Historical Chart'),
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

filter_form_analytics = html.Div([
    html.H5('Filter'),
    location
], id='filter_form_analytics', style={'display': 'block'})


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
home_layout = home.create(filter=filter_box, pred_bread=pred_bread, pred_coffee=pred_coffee, pred_cake=pred_cake, pred_sandwitch=pred_sandwitch)

### DATA ###
data = LayoutData()
data_layout = data.create(uploader=uploader)

### ANALYTICS ###
analytics = LayoutAnalytics()
analytics_layout = analytics.create(filter_form_analytics, output_graph_top10, turnover_graph, rest_produkte)

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
              Output(pred_sandwitch, 'figure'),
              Input(history_cb, 'value'))
def pred_graph(history):
    bar = PlotlyBarChart()
    fig1 = bar.create(df=df, history=history, item='Bread')
    fig2 = bar.create(df=df, history=history, item='Coffee')
    fig3 = bar.create(df=df, history=history, item='Cake')
    fig4 = bar.create(df=df, history=history, item='Sandwich')

    return fig1, fig2, fig3, fig4


### ANALYTICS ###
@app.callback(
   Output(component_id='filter_form_analytics', component_property='style'),
   [Input(component_id='filter_switch_analytics', component_property='on')])
def filter_analytics(on):
    if on:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


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