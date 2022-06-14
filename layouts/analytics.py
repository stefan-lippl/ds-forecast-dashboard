import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc
from layouts.navbar import LayoutNavbar

class LayoutAnalytics:
    def create(self, location, output_graph_top10, turnover_graph, rest_produkte):
        navbar = LayoutNavbar('Analytics').create()

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
    
        return analytics_layout