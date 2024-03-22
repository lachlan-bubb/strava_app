from dash import html, dash_table, dcc
import plotly.express as px


def layout_define(df):

    # Creating a bar chart using Plotly Express
    column_x_counts = df["start_date"].value_counts().reset_index()
    column_x_counts.columns = ["Unique Values", "Count"]
    fig1 = px.bar(
        column_x_counts,
        x="Unique Values",
        y="Count",
    )

    # Creating a line chart using Plotly Express
    fig2 = px.line(
        df,
        x="start_date",
        y="name",
    )

    page1_layout = html.Div(
        [
            dash_table.DataTable(id="table", data=df.to_dict("records"), page_size=10),
        ]
    )

    page2_layout = html.Div(
        [
            html.Div([
                html.Label('Select Y Axis:'),
                dcc.Dropdown(
                    id="yaxis-dropdown",
                    options=[
                        {"label": col, "value": col} for col in df.columns[1:]
                    ],  # Exclude 'Date'
                    value=df.columns[1],  # Default selected column
                    multi=False,
                ),
                ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select Color:'),    
                dcc.Dropdown(
                    id="color-dropdown",
                    options=[
                        {"label": col, "value": col} for col in df.columns[1:]
                    ],  # Exclude 'Date'
                    value='athlete.id',  # Default selected column
                    multi=False,
            ),
            ], style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(figure=fig1, id="fig1"),
            dcc.Graph(figure=fig2, id="fig2"),
        ]
    )

    layout = html.Div(
        [
            html.Div(children="My Strava App: Summary of my Strava activities."),
            html.Hr(),
            dcc.Tabs(
                [
                    dcc.Tab(label="Table", value="page-1", children=page1_layout),
                    dcc.Tab(label="Chart", value="page-2", children=page2_layout),
                ]
            ),
        ]
    )
    return layout
