# app/callbacks.py
from dash.dependencies import Input, Output
import plotly.express as px

# from app.layout import layout


# Callback to update the plot based on the selected column
def register_callbacks(app, df):
    @app.callback([Output("fig1", "figure"),Output("fig2", "figure")], 
                  [Input("yaxis-dropdown", "value"),Input("color-dropdown", "value")])
    def update_plot(selected_column,selected_color):
        # print('selected_column:'+selected_column)
        # print('selected_color:'+selected_color)
        
        # Distance plot
        column_x_counts = df[selected_column].value_counts().reset_index()
        column_x_counts.columns = ["Unique Values", "Count"]

        # Creating a bar chart using Plotly Express
        fig1 = px.bar(
            column_x_counts,
            x="Unique Values",
            y="Count",
            title="Bar Chart of Column X Counts"
        )

        # Creating a bar chart using Plotly Express
        fig2 = px.line(
            df,
            x="start_date",
            y=selected_column,
            title="Bar Chart of Column X Counts",
            color=selected_color
        )

        return fig1, fig2
