import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc

from layouts.navbar import LayoutNavbar

class LayoutHome:
    def create(self, history_cb, pred_bread,pred_coffee, pred_cake):
        navbar = LayoutNavbar().create()
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

        return home_layout