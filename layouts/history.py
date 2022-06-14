import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc
from dash import html, dcc
from layouts.navbar import LayoutNavbar
from dash import html, dcc

class LayoutHistory:
    def create(self, df):
        navbar = LayoutNavbar().create()

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
    
        return history_layout