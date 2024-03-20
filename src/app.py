import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, dcc, html
from sklearn import datasets
from sklearn.cluster import KMeans

iris_raw = datasets.load_iris()
iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])

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
                dbc.Label("تاريخ"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in iris.columns
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("عدد البروتينات"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("تجميع البروتينات في زهرة الآيرس"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("cluster-graph", "figure"),
    [
        Input("x-variable", "value"),
        Input("cluster-count", "value"),
    ],
)
def make_graph(x, n_clusters):
    # التحقق الأدنى من المدخلات، تأكد من وجود عدد البروتينات المطلوب على الأقل
    km = KMeans(n_clusters=max(n_clusters, 1))
    df = iris.loc[:, [x]]
    km.fit(df.values)
    df["cluster"] = km.labels_

    centers = km.cluster_centers_

    data = [
        go.Scatter(
            x=df.loc[df.cluster == c, x],
            y=df.loc[df.cluster == c, x],
            mode="markers",
            marker={"size": 8},
            name="Cluster {}".format(c),
        )
        for c in range(n_clusters)
    ]

    data.append(
        go.Scatter(
            x=centers[:, 0],
            y=centers[:, 0],
            mode="markers",
            marker={"color": "#000", "size": 12, "symbol": "diamond"},
            name="مراكز الأcluster",
        )
    )

    layout = {"xaxis": {"title": x}, "yaxis": {"title": "عدد البروتينات"}}

    return go.Figure(data=data, layout=layout)


# التأكد من أن قيم x و y لا يمكن أن تكونا نفس المتغير
def filter_options(v):
    """تعطيل الخيار v"""
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in iris.columns
    ]


# نفس الوظيفة لكل من القائمتين المنسدلتين، لذا نعيد استخدام filter_options
app.callback(Output("x-variable", "options"), [Input("cluster-count", "value")])(
    filter_options
)


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)