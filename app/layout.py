import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

def layout_define(data) :

    layout = html.Div(
        [
            html.Div(children="My Strava App"),
            html.Hr(),
            dash_table.DataTable(id='table',
                                    data=data.to_dict('records'),
                                    page_size=10)    
        ]
    )
    return layout