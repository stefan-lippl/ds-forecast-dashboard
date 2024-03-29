import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc
from layouts.navbar import LayoutNavbar
from dash_iconify import DashIconify
import dash_daq as daq
import config

class LayoutHome:
    def create(self, filter, pred_bread,pred_coffee, pred_cake, pred_sandwitch):
        navbar = LayoutNavbar('Home').create()
        home_layout = html.Div([
            navbar,
            html.Div([],id="hidden-div", style={"display":"none"}),

            html.Div([
                dbc.Row([
                    dbc.Col([daq.BooleanSwitch(id='filter_switch', 
                                               on=False, 
                                               color=config.toggle_button['background_color'],
                                               #label="Filter",
                                               labelPosition="top",
                                               style={'margin-left': '0px', 'float': 'left'})]),
                    dbc.Col([html.H5('92%', style={'float': 'right', 'color': 'green'}), html.H5('Aktuelle Genauigkeit:  \t', style={'float': 'right'})])
                ]),
                dbc.Row([
                    dbc.Col([filter])
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
                    ]),
                    dbc.Col([
                        html.H5('Sandwich: 5', style={'margin-bottom': '0px'}),
                        pred_sandwitch
                    ])
                ])
            ], style={'margin': '20px'})
        ], style={'height':'100vh','margin':'0px','backgroundColor':config.html['main_background_color']})

        return home_layout