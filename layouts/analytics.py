import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
import config
from layouts.navbar import LayoutNavbar

class LayoutAnalytics:
    def create(self, filter, output_graph_top10, turnover_graph, rest_produkte):
        navbar = LayoutNavbar('Analytics').create()

        analytics_layout = html.Div([
            navbar,
            html.Div([],id="hidden-div", style={"display":"none"}),

            html.Div([
                dbc.Row([
                    dbc.Col([daq.BooleanSwitch(id='filter_switch_analytics', 
                                                on=False, 
                                                color=config.toggle_button['background_color'],
                                                #label="Filter",
                                                labelPosition="top",
                                                style={'margin-left': '0px', 'float': 'left'})]),
                    dbc.Col([html.H5('92%', style={'float': 'right', 'color': 'green'}), html.H5('Aktuelle Genauigkeit:  \t', style={'float': 'right'})]),
                ]),    
                dbc.Row([
                    dbc.Col([filter]), 
                ]),

                html.Hr(),

                dbc.Row([
                    dbc.Col([output_graph_top10]), 
                    dbc.Col([rest_produkte]),
                ], style={'margin-top': '10px'}),

                dbc.Row([turnover_graph])
            ], style={'margin': '20px'})
        ], style={'height':'100vh','margin':'0px','backgroundColor':config.html['main_background_color']})
    
        return analytics_layout