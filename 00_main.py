# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Import local packages
import functions.data_prep as dp
from app.layout import layout_define

# Stand up app
app = Dash(__name__)

# create data
activities = dp.import_data()

# App layout
app.layout = layout_define(activities)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
