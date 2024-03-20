import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, dcc, html
from sklearn.cluster import KMeans
from datetime import datetime, timedelta

# بيانات الأمثلة
data = [
    {"date": datetime.now() - timedelta(days=7), "top_ten": 15},
    {"date": datetime.now() - timedelta(days=6), "top_ten": 10},
    {"date": datetime.now() - timedelta(days=5), "top_ten": 13},
    {"date": datetime.now() - timedelta(days=4), "top_ten": 9},
    {"date": datetime.now() - timedelta(days=3), "top_ten": 12},
    {"date": datetime.now() - timedelta(days=2), "top_ten": 8},
    {"date": datetime.now() - timedelta(days=1), "top_ten": 11},
]

df = pd.DataFrame(data)

app = dash.Dash(
    title="Dpage",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Date"),
                dcc.Dropdown(
                    id="date-variable",
                    options=[
                        {"label": date.strftime("%Y-%m-%d"), "value": date} for date in df["date"]
                    ],
                    value=df["date"].max(),
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Top Ten"),
                dcc.Dropdown(
                    id="top-ten-variable",
                    options=[
                        {"label": row["date"].strftime("%Y-%m-%d"), "value": row["top_ten"]} for _, row in df.iterrows()
                    ],
                    value=df.loc[df["date"] == df["date"].max(), "top_ten"].values[0],
                ),
            ]
        ),
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Top Ten Classification"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="classification-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("classification-graph", "figure"),
    [
        Input("date-variable", "value"),
        Input("top-ten-variable", "value"),
    ],
)
def make_graph(date, top_ten):
    df_filtered = df.loc[df["date"] == date]

    data = [
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered["top_ten"],
            mode="markers",
            marker={"size": 8},
            name="Top Ten",
        ),
        go.Scatter(
            x=[date],
            y=[top_ten],
            mode="markers",
            marker={"color": "#000", "size": 12, "symbol": "diamond"},
            name="Selected Top Ten",
        )
    ]

    layout = {"xaxis": {"title": "Date"}, "yaxis": {"title": "Top Ten"}}

    return go.Figure(data=data, layout=layout)


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)