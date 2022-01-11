import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import pandas as pd
from dashboard1 import Dashboard
from dash.dependencies import Input, Output


dashboard = Dashboard()
ext_style = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets=ext_style)
server = app.server
app.title = 'COVID-19 Dashboard'
app.layout = dashboard.generate_layout()


@app.callback(
    Output(component_id='graph1', component_property='figure'),
    Output(component_id='card1', component_property='children'),
    Input(component_id='id-1', component_property='value'),
    Input(component_id='slider', component_property='value')
)
def update_output_div(input_value1, input_value2):
    return dashboard.confirmed_trend(input_value1, input_value2), dashboard.generate_cards(input_value1)


# app.run_server(debug=True)
















# app = dash.Dash()
# df = pd.read_csv(r'country_wise_latest.csv', delimiter=',')
# filter_df = df[(df['WHO Region'] != 'Europe')]
#
#
# def covid_stat():
#     # fig = go.Figure([go.Scatter(x=df['Date'], y=df['Deaths'], line=dict(color='firebrick', width=4), name='COVID')])
#     fig = px.scatter(df, x='Deaths / 100 Cases', y='Deaths / 100 Recovered')
#     # fig.update_layout(title='Deaths over time',
#     #                   xaxis_title='Dates',
#     #                   yaxis_title='Deaths')
#     return fig
#
#
# app.layout = html.Div(
#     [html.H1(id='H1', children='COVID-19 Death Ratio',
#              style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
#      html.Div(
#          dcc.Graph(id='line_plot', figure=covid_stat())
#      )
#      ]
# )
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
