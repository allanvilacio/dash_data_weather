import dash
from dash import Dash, dcc ,html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

from utility.data_frames import get_df_weather, get_d_cidades

# Data frames
df_weather = get_df_weather()

dash.register_page(__name__, path='/')

STYLE_CARDS = {"margin-top": "10px", 'text-align':'center'}

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.P(id='teste-ibge'), md=3)
            ]
        ),
    
        dbc.Row(
            [
                dbc.Col(dbc.Card( 
                            dbc.CardBody([
                                html.Span('tempmax', className="card-text"),
                                html.H3( style={"color": "#adfc92"}, id='card-tempmax')
                                ]), color='light', outline=True, 
                                style=STYLE_CARDS)
                ),
                dbc.Col(dbc.Card(
                            dbc.CardBody([
                                html.Span('temp', className="card-text"),
                                html.H3(style={"color": "#adfc92"}, id='card-temp')
                                ]), color="light", outline=True, 
                                style=STYLE_CARDS)
                ),
                dbc.Col(dbc.Card(
                            dbc.CardBody([
                                html.Span('tempmin', className="card-text"),
                                html.H3(style={"color": "#adfc92"}, id='card-tempmin')
                                ]), color="light", outline=True,
                                style=STYLE_CARDS)
                ),
                dbc.Col(dbc.Card( 
                            dbc.CardBody([
                                html.Span('windspeed', className="card-text"),
                                html.H3(style={"color": "#adfc92"}, id='card-windspeed')
                                ]), color="light", outline=True,
                                style=STYLE_CARDS)
                ),
                dbc.Col(dbc.Card( 
                            dbc.CardBody([
                                html.Span('humidity', className="card-text"),
                                html.H3(style={"color": "#adfc92"}, id='card-humidity')
                                ]), color="light", outline=True,
                                style=STYLE_CARDS)
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                        [
                            dcc.Graph(id='example-graph1')
                        ], md=6),
                dbc.Col(
                        [
                            dcc.Graph(id='example-graph2')
                        ], md=6)
            ], style={'margin-top': '10px'}, align='center'
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='example-graph3'))
                
            ], style={'margin-top': '10px'}
        ),

        dbc.Row(
            [
                html.Footer(f"Dados atualizados até: {df_weather['days_datetime'].max().strftime('%d de %B de %Y')}.")
            ], style={'margin': '10px', 'text-align':'right'}
        )
    ], fluid=True
)


@callback(
     [
        Output('example-graph1', 'figure'),
        Output('example-graph2', 'figure'),
        Output('example-graph3', 'figure')
    ],
    [Input('location-dropdown', 'value')]
)
def filtered_dfs(value):

    df_weather_filtered = df_weather[df_weather['codigo_ibge']==value]
    
    # =========== Figure =======================
    fig1 = px.histogram(df_weather_filtered,
                        x='days_temp',
                        nbins=15)
    fig1.update_traces({'hovertemplate':'%{y:.3}</b>'} )
    fig1.update_layout({'hovermode':'x unified', "template":"plotly_dark"},
                      margin=dict(l=10, r=10, b=10, t=50))

    fig2 = px.bar(
                (df_weather_filtered
                    .groupby(by=[df_weather_filtered['days_datetime'].dt.strftime('%Y').rename('ano'),
                                 df_weather_filtered['days_datetime'].dt.strftime('%B')], sort=False)
                ['days_temp']
                .mean()
                .reset_index()),
                x='days_datetime',
                y='days_temp',
                color='ano',
                barmode='group')
    
    fig2.update_traces({'hovertemplate':'%{y:.3}</b>'} )
    fig2.update_layout({'hovermode':'x unified', "template":"plotly_dark"},
                      margin=dict(l=10, r=10, b=10, t=50))
    
    fig2.update_layout({"template":"plotly_dark"},
                      margin=dict(l=10, r=10, b=10, t=50))
    
    fig3 = px.line(
                (df_weather_filtered
                .groupby(by=[df_weather['days_datetime'].dt.strftime('%Y').rename('ano'),
                            df_weather['days_datetime'].dt.dayofyear], sort=False)
                ['days_temp']
                .mean()
                .reset_index()),
                x='days_datetime',
                y='days_temp',
                color='ano',
                title='Fig 1')
    
    fig3.update_traces({'hovertemplate':'%{y:.3}</b>', 'line_shape':'spline'} )
    fig3.update_layout({'hovermode':'x unified', "template":"plotly_dark"},
                      margin=dict(l=10, r=10, b=10, t=50))

    
    return (fig1, fig2, fig3)


@callback(
     [
        Output('teste-ibge', 'children'),
        Output('card-tempmax', 'children'),
        Output('card-temp', 'children'),
        Output('card-tempmin', 'children'),
        Output('card-windspeed', 'children'),
        Output('card-humidity', 'children')
    ],
    [Input('location-dropdown', 'value')]
)
def filtered_cards(value):

    df_weather_filtered = df_weather[df_weather['codigo_ibge']==value]
    
    # ======= Cards =======================
    
    lista_cards = []
    for column in ['days_tempmax', 'days_temp', 'days_tempmin', 'days_windspeed', 'days_humidity']:
        lista_cards.append(df_weather_filtered.loc[df_weather_filtered.index.max()][column])
    
    return (value, lista_cards[0], lista_cards[1], lista_cards[2], 
            lista_cards[3], lista_cards[4])