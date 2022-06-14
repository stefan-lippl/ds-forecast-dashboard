import dash_bootstrap_components as dbc
import sys
sys.path.append('../')

class LayoutNavbar:
    def create(self):
        navbar = dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="/home")),
                    dbc.NavItem(dbc.NavLink("Data", href="/data")),
                    dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
                    dbc.NavItem(dbc.NavLink("History", href="/history")),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("More pages", header=True),
                            dbc.DropdownMenuItem("Profil", href="#"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="More",
                    ),
                ],
                brand="Robros - Dashboard",
                brand_href="/home",
                color="#30a3d1",
                dark=True,
                style={'box-shadow': '0px 0px 3px 0px #000000'}
            )
        return navbar