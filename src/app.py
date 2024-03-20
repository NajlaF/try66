import dash
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from dash import Dash, Input, Output, dcc, html

# بيانات الجدول المثالية
data = [
    {"Protein": "Protein A", "Value": 10, "Date": "2024-03-20"},
    {"Protein": "Protein B", "Value": 8, "Date": "2024-03-20"},
    {"Protein": "Protein C", "Value": 6, "Date": "2024-03-20"},
    {"Protein": "Protein D", "Value": 4, "Date": "2024-03-20"},
    {"Protein": "Protein E", "Value": 2, "Date": "2024-03-20"},
    {"Protein": "Protein F", "Value": 9, "Date": "2024-03-19"},
    {"Protein": "Protein G", "Value": 7, "Date": "2024-03-19"},
    {"Protein": "Protein H", "Value": 5, "Date": "2024-03-19"},
    {"Protein": "Protein I", "Value": 3, "Date": "2024-03-19"},
    {"Protein": "Protein J", "Value": 1, "Date": "2024-03-19"},
]

# تحويل البيانات إلى DataFrame
df = pd.DataFrame(data)

# إنشاء تطبيق Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# تخصيص تخطيط الصفحة
app.layout = dbc.Container(
    [
        html.H1("صفحة المريض"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H3("معلومات المريض"),
                            html.P("اسم المريض: محمد"),
                            html.P("العمر: 30 سنة"),
                            html.P("الجنس: ذكر"),
                        ]
                    ),
                    md=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H3("جدول البروتينات العادية"),
                            dcc.DatePickerSingle(
                                id="date-picker",
                                date=datetime.datetime.now().date(),
                            ),
                            html.Table(id="protein-table"),
                        ]
                    ),
                    md=6,
                ),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

# تحديث جدول البروتينات عند تغيير التاريخ
@app.callback(
    Output("protein-table", "children"),
    [Input("date-picker", "date")]
)
def update_protein_table(selected_date):
    selected_df = df[df["Date"] == selected_date].nlargest(10, "Value")
    table_rows = []
    for _, row in selected_df.iterrows():
        table_rows.append(
            html.Tr(
                [
                    html.Td(row["Protein"]),
                    html.Td(row["Value"]),
                ]
            )
        )
    return [
        html.Thead(
            html.Tr(
                [
                    html.Th("اسم البروتين"),
                    html.Th("القيمة"),
                ]
            )
        ),
        html.Tbody(table_rows)
    ]


if __name__ == "__main__":
    app.run_server(debug=True)