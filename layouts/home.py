import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc
from layouts.navbar import LayoutNavbar
from dash_iconify import DashIconify
import dash_daq as daq

class LayoutHome:
    def create(self, history_cb, pred_bread,pred_coffee, pred_cake):
        navbar = LayoutNavbar('Home').create()
        home_layout = html.Div([
            navbar,
            html.Div([],id="hidden-div", style={"display":"none"}),
            html.Div([
                dbc.Row([
                    dbc.Col([daq.BooleanSwitch(id='filter_switch', 
                                               on=False, 
                                               color="#9B51E0",
                                               #label="Filter",
                                               labelPosition="top",
                                               style={'margin-left': '0px', 'float': 'left'})]),
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