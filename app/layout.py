import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

def layout_define(df) :

    # Distance plot
    column_x_counts = df['start_date'].value_counts().reset_index()
    column_x_counts.columns = ['Unique Values', 'Count']

    # Creating a bar chart using Plotly Express
    fig1 = px.bar(column_x_counts, x='Unique Values', y='Count', title='Bar Chart of Column X Counts')

    layout = html.Div(
        [
            html.Div(children="My Strava App"),
            html.Hr(),
            dash_table.DataTable(id='table',
                                data=df.to_dict('records'),
                                page_size=10,
                                style_table={'className': 'data-table'}  # Apply the data-table class
                                ),
            dcc.Graph(figure=fig1),
        ]
    )
    return layout