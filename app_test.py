import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash('example')

app.layout = html.Div([
    dcc.Dropdown(
        id = 'dropdown-to-show_or_hide-element',
        options=[
            {'label': 'Show element', 'value': 'on'},
            {'label': 'Hide element', 'value': 'off'}
        ],
        value = 'on'
    ),

    # Create Div to place a conditionally visible element inside
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
        id = 'element-to-hide',
        placeholder = 'something',
        value = 'Can you see me?',
        )
    ], style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
    ),
    html.H1('Always')
    ])

@app.callback(
   Output(component_id='element-to-hide', component_property='style'),
   [Input(component_id='dropdown-to-show_or_hide-element', component_property='value')])

def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)