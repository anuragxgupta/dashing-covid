import plotly.express as px
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
from generate_data import GenerateData
import config as cfg


class Dashboard:

    def __init__(self):
        self.colors = cfg.colors

    def confirmed_trend(self, cntry='India', window=3):
        data = GenerateData()
        data.get_data()
        df = data.process_data(data.df_confirmed, cntry=cntry, window=window)
        if window == 1:
            yaxis_title = "Daily Cases"
        else:
            yaxis_title = "Daily Cases ({}-day MA)".format(window)
        fig = px.line(df, y='Total', x=df.index, title='Daily confirmed cases trend for {}'.format(cntry.upper()),
                      height=600,
                      color_discrete_sequence=['maroon'])
        fig.update_layout(title_x=0.5, plot_bgcolor='#F2DFCE', paper_bgcolor='#F2DFCE', xaxis_title="Date",
                          yaxis_title=yaxis_title)
        return fig

    def generate_page_header(self):
        main_header = dbc.Row(
            [
                dbc.Col(
                    html.Div('COVID-19 Dashboard',
                             style={
                                 'textAlign': 'center',
                                 'color': self.colors['text'],
                                 'fontSize': 30,
                                 'fontWeight': 900,
                             }), md=12
                )
            ],
            align='center',
            style={'backgroundColor': self.colors['background']}
        )

        sub_header = dbc.Row(
            [
                dbc.Col(
                    html.Div(children='Data Visualization of COVID-19 data generated from sources all over the world.',
                             style={
                                 'textAlign': 'center',
                                 'color': self.colors['text'],
                                 'fontSize': 20,
                             }), md=12
                )
            ],
            align='center',
            style={'backgroundColor': self.colors['background']}
        )
        header = (main_header, sub_header)
        return header

    def card_content(self, header, card_value, overall):
        card_header_style = {'textAlign': 'center', 'fontSize': '150%', 'fontWeight': '900'}
        card_body_style = {'textAlign': 'center', 'fontSize': '200%', 'fontWeight': '900'}
        card_body = dbc.CardBody(
            [
                html.P(header, style=card_header_style),
                html.Hr(),
                html.H5(f'{int(card_value):,}', className='card-title', style=card_body_style),
                html.P('Worldwide: {:,}'.format(overall), className='class-text', style={'textAlign': 'center'}),
            ]
        )
        return card_body

    def generate_cards(self, cntry='India'):
        data = GenerateData()
        dashboard = Dashboard()
        data.get_data()
        confirm_cntry = data.get_total_country(data.df_confirmed, cntry)
        deaths_cntry = data.get_total_country(data.df_deaths, cntry)
        confirm_world = data.get_total_world(data.df_confirmed)
        deaths_world = data.get_total_world(data.df_deaths)
        cards = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(dashboard.card_content('Confirmed', confirm_cntry, confirm_world), color='warning',
                                     ), md=dict(size=3)),
                        dbc.Col(
                            html.Div(cntry.upper(), style={'textAlign': 'center', 'fontSize': '200%', 'color': 'black',
                                                          'fontWeight': '900', 'margin': 'auto'}),
                            md=dict(size=3), className='justify-content-center align-items-center'),
                        dbc.Col(dbc.Card(dashboard.card_content('Deaths', deaths_cntry, deaths_world), color='danger',
                                         ), md=dict(size=3)),
                    ], className='mb-4 justify-content-center align-items-center',
                ),
            ], id='card1'
        )
        return cards

    def generate_dropdown(self, sid):
        data = GenerateData()
        data.get_data()
        cntry_ls = data.df_confirmed['Country/Region'].unique()
        dropdown_ls = []
        for cntry in sorted(cntry_ls):
            temp = {'label': cntry, 'value': cntry}
            dropdown_ls.append(temp)
        dropdown = html.Div(
            [
                html.Label('Select Country', style={'color': 'black'}),
                dcc.Dropdown(id='id-' + str(sid),
                             options=dropdown_ls,
                             value='India', style={'color': self.colors['text']}),
                html.Div(id='div-' + str(sid))
            ]
        )
        return dropdown

    def confirmed_chart(self):
        dashboard = Dashboard()
        return dcc.Graph(id='graph1', figure=dashboard.confirmed_trend())

    def generate_slider(self):
        slider = html.Div(
            [
                html.Label('Select Average Window', style={'color': 'black'}),
                dcc.Slider(id='slider', min=1, max=14, step=None, marks={
                                1: '1',
                                3: '3',
                                5: '5',
                                7: '1-Week',
                                14: 'Fortnight'
                            }, value=3),
            ]
        )
        return slider

    def generate_layout(self):
        dashboard = Dashboard()
        page_header = dashboard.generate_page_header()
        layout = dbc.Container(
            [
                page_header[0],
                page_header[1],
                html.Br(),
                dashboard.generate_cards(),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(dashboard.generate_dropdown(sid=1), md=dict(size=3, offset=2)),
                        dbc.Col(dashboard.generate_slider(), md=dict(size=4, offset=1)),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dashboard.confirmed_chart(), md=12)
                    ],
                    align='center',
                ),
            ], fluid=True, style={'backgroundColor': self.colors['bodyColor']}
        )
        return layout

# app = dash.Dash()
# df = pd.read_csv(r'country_wise_latest.csv', delimiter=',')
#
# app.layout = html.Div(
#     [html.H1(id='topic', children='COVID-19 Death Ratio',
#              style={'textAlign': 'center'}),
#      html.Div(
#          [
#              html.Label("Select Region"),
#              dcc.Dropdown(id='region-dropdown', options=[
#                  {'label': s, 'value': s} for s in df['WHO Region'].unique()
#              ],
#                           className='dropdown', style={'cursor': 'pointer'})
#          ]
#      ),
#      html.Div(dcc.Graph(id='plot'), className='chart'),
#      ]
# )
#
#
# @app.callback(
#     Output('plot', 'figure'),
#     Input('region-dropdown', 'value'),
# )
# def update_figure(region):
#     ndf = df
#     if region:
#         ndf = df[df['WHO Region'] == region]
#
#     fig = px.scatter(ndf, x='Deaths / 100 Cases', y='Deaths / 100 Recovered', hover_name='Country/Region', size='Confirmed')
#     return fig
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
