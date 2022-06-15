import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc
from layouts.navbar import LayoutNavbar
from dash_iconify import DashIconify
import dash_daq as daq

class LayoutHomeTest:
    def create(self, history_cb):
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
                html.Div([
                    html.Button("Add Filter", id="dynamic-add-filter", n_clicks=0),
                    html.Div(id='dynamic-dropdown-container', children=[]),
                ])

            ], style={'margin': '20px'})
        ], style={'height':'100vh','margin':'0px','backgroundColor':'#f0f4fa'})

        return home_layout