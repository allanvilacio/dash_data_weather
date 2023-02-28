from dash import Dash, dcc ,html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from utility.data_frames import get_df_weather, get_d_cidades
import pandas as pd

# Data frames
df_weather = get_df_weather()
d_cidades = get_d_cidades()

# teste ________________

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "dash data weather"

app.layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Button(
                    "Open scrollable offcanvas",
                    id="open-offcanvas-scrollable",
                    n_clicks=0,
                ),
                dbc.Offcanvas(
                    html.P("The contents on the main page are now scrollable."),
                    id="offcanvas-scrollable",
                    scrollable=True,
                    title="Scrollable Offcanvas",
                    is_open=False
                ),
            ]
        ),
        
        dcc.Dropdown(id='location-dropdown', 
                     options=[{'label': label, 'value': value} for label, value in d_cidades[['nome_mun','codigo_ibge']].sort_values(by='nome_mun').values],
                       value='2704302'),
        html.P(id='teste-ibge'),

        dbc.Row(
            [
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span('tempmax', className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_tempmax'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_1")
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF",'text-align':'center'})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span('temp', className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_temp'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_2")
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF",'text-align':'center'})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span('tempmin', className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_tempmin'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_3")
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF",'text-align':'center'})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span('windspeed', className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_windspeed'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_4")
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF",'text-align':'center'})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span('humidity', className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_humidity'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_5")
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF", 'text-align':'center'}))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                        [
                            dcc.Graph(id='example-graph')
                        ]
                ),
                dbc.Col(
                        [
                            dcc.Graph(id='example-graph2')
                        ]
                )
            ], style={'margin-top': '10px'}
        ),
        dbc.Row(
            [
                html.Footer(f"Dados atualizados até: {df_weather['days_datetime'].max().strftime('%d de %B de %Y')}.")
            ], style={'margin': '10px', 'text-align':'right'}
        )
    ]
)

@app.callback(
    Output("offcanvas-scrollable", "is_open"),
    Input("open-offcanvas-scrollable", "n_clicks"),
    State("offcanvas-scrollable", "is_open"),
)
def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    [
        Output('teste-ibge', 'children'),
        Output('example-graph', 'figure'),
        Output('example-graph2', 'figure')
    ],
    [Input('location-dropdown', 'value')]
)
def filtered_dfs(value):
    
    df_weather_fig = (df_weather[df_weather['codigo_ibge']==value]
                      .groupby(by=['days_datetime','codigo_ibge'])
                      .mean(numeric_only=True)['days_temp']
                      .reset_index()
                    )

    fig = px.line(df_weather_fig,
             y='days_temp',
             x=df_weather_fig['days_datetime'].dt.dayofyear,
             color= df_weather_fig['days_datetime'].dt.year,
             title='Fig 1')
    fig.update_traces({'hovertemplate':'%{y:.2}</b>', 'line_shape':'spline'} )
    fig.update_layout({'hovermode':'x unified', "template":"plotly_dark"},
                      margin=dict(l=10, r=10, b=10, t=50))

    fig2 = px.line(df_weather_fig,
             y='days_temp',
             x=df_weather_fig['days_datetime'].dt.strftime('%m-%Y'),
             color= df_weather_fig['codigo_ibge'],
             title='Fig 2')
    fig2.update_traces({'hovertemplate':'%{y:.2}</b>'})
    fig2.update_layout({'hovermode':'x unified', "template":"plotly_dark"},
                       margin=dict(l=10, r=10, b=10, t=50))

    
    return value, fig, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
