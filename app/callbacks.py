# app/callbacks.py
from dash.dependencies import Input, Output
import plotly.express as px

# from app.layout import layout

# Callback to update the plot based on the selected column
def register_callbacks(app, df):
    @app.callback(
        Output('fig1', 'figure'),
        [Input('column-dropdown', 'value')]
    )
    def update_plot(selected_column):

        # Distance plot
        column_x_counts = df[selected_column].value_counts().reset_index()
        column_x_counts.columns = ['Unique Values', 'Count']

        # Creating a bar chart using Plotly Express
        fig1 = px.bar(column_x_counts, x='Unique Values', y='Count', title='Bar Chart of Column X Counts')

        return fig1