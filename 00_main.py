# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Import local packages
import functions.data_prep as dp

activities = dp.import_data()

app = Dash(__name__)

# App layout
app.layout = html.Div(
    [
        html.Div(children="My Strava App"),
        html.Hr(),
        dash_table.DataTable(id='table',
                                data=activities.to_dict('records'),
                                page_size=10)    
    ]
)


# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
