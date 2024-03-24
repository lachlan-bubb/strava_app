# app/callbacks.py
from dash.dependencies import Input, Output
import plotly.express as px
import functions.model_build as mb
import pandas as pd


# Callback to update the plot based on the selected column
def register_callbacks(app, df, model_object):
    @app.callback(
        [Output("fig1", "figure"), Output("fig2", "figure")],
        [Input("yaxis-dropdown", "value"), Input("color-dropdown", "value")],
    )
    def update_plot(selected_column, selected_color):
        
        # Distance plot
        column_x_counts = df[selected_column].value_counts().reset_index()
        column_x_counts.columns = ["Unique Values", "Count"]

        # Creating a bar chart using Plotly Express
        fig1 = px.bar(
            column_x_counts,
            x="Unique Values",
            y="Count",
            title="Bar Chart of Column X Counts",
        )

        # Creating a bar chart using Plotly Express
        fig2 = px.line(
            df,
            x="start_date",
            y=selected_column,
            title="Line Chart of Column X",
            color=selected_color,
        )

        return fig1, fig2

    @app.callback(
        [
            Output("output-container-distance", "children"),
            Output("output-container-speed", "children"),
            Output("output-container-effort", "children"),
        ],
        [Input("input-box-distance", "value"), Input("input-box-speed", "value")],
    )
    def update_output(distance, speed):

        def check_valid(value):
            bool_value = value is not None and not pd.isna(value) and value is not ""
            return bool_value

        effort = ""
        if check_valid(distance) and check_valid(speed):
            effort = mb.model_score(model_object, distance, speed)

        return (
            f"You have entered: {distance} miles",
            f"You have entered: {speed} minutes per mile",
            f"The estimated effort: {effort}",
        )
