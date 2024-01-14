from dash import html, dash_table, dcc
import plotly.express as px


def layout_define(df):
    # Distance plot
    column_x_counts = df["start_date"].value_counts().reset_index()
    column_x_counts.columns = ["Unique Values", "Count"]

    # Creating a bar chart using Plotly Express
    fig1 = px.bar(
        column_x_counts,
        x="Unique Values",
        y="Count",
        title="Bar Chart of Column X Counts",
    )

    page1_layout = html.Div(
        [
            dash_table.DataTable(id="table", data=df.to_dict("records"), page_size=10),
        ]
    )

    page2_layout = html.Div(
        [
            dcc.Dropdown(
                id="column-dropdown",
                options=[
                    {"label": col, "value": col} for col in df.columns[1:]
                ],  # Exclude 'Date'
                value=df.columns[1],  # Default selected column
                multi=False,
            ),
            dcc.Graph(figure=fig1, id="fig1"),
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
