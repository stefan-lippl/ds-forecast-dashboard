import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import html, dcc
import sys
sys.path.append('../')

class LayoutNavbar:
    def __init__(self, title):
        self.title = title

    def create(self):
        navbar = dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink(DashIconify(
                            icon="ant-design:home-outlined",
                            width=30,
                        ), href="/home"), style={'margin-left': '5px', 'margin-right': '5px'}),
                    
                    dbc.NavItem(dbc.NavLink(DashIconify(
                            icon="eos-icons:big-data-outlined",
                            width=30,
                        ), href="/data"), style={'margin-left': '5px', 'margin-right': '5px'}),

                    dbc.NavItem(dbc.NavLink(DashIconify(
                            icon="ion:analytics-outline",
                            width=30,
                        ), href="/analytics"), style={'margin-left': '5px', 'margin-right': '5px'}),

                    dbc.NavItem(dbc.NavLink(DashIconify(
                            icon="fontisto:history",
                            width=30,
                        ), href="/history"), style={'margin-left': '5px', 'margin-right': '5px'}),

                    
                    #dbc.DropdownMenu(
                    #    children=[
                    #        dbc.DropdownMenuItem("More pages", header=True),
                    #        DropdownMenuItem("Profil", href="#"),
                    #    ],
                    #    nav=True,
                    #    in_navbar=True,
                    #    label="More",
                    #),<i class="fa-solid fa-house-chimney"></i>
                ],
                brand=f"ЯD - {self.title}",
                brand_href="/home",
                color="#30a3d1",
                dark=True,
                style={'box-shadow': '0px 0px 3px 0px #000000'}
            )
        return navbar