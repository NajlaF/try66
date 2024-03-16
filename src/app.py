'''
 # @ Create Time: 2024-03-17 00:43:05.269944
'''

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__, title="try6")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.H1(children='Doctor Dashboard'),
    html.Table(
        # Header
        [html.Tr([html.Th(col) for col in patients_data.columns])] +

        # Rows
        [html.Tr([html.Td(patients_data.iloc[i][col]) for col in patients_data.columns])
         for i in range(len(patients_data))]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
