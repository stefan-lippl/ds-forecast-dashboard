import sys
sys.path.append('../')
from dash import html
import dash_bootstrap_components as dbc
from layouts.navbar import LayoutNavbar

class LayoutData:
    def create(self, uploader):
        navbar = LayoutNavbar('Data').create()

        data_layout = html.Div([
            navbar,
            html.Div([],id="hidden-div", style={"display":"none"}),

            html.Div([
                dbc.Row([
                    dbc.Col([]),
                    dbc.Col([uploader]),
                    dbc.Col([])
                ]),
                dbc.Row([
                    dbc.Col([]),
                    dbc.Col([html.Div(id='output-data-upload')]),
                    dbc.Col([])
                ])
            ], style={'margin': '20px'})
        ])

        return data_layout