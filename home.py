from dash import Dash, dcc ,html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from utility.data_frames import get_df_weather, get_d_cidades

# Data frames
df_weather = get_df_weather()
d_cidades = get_d_cidades()

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "dash data weather"

df_weather_fig = df_weather.groupby(by='days_datetime').mean(numeric_only=True)['days_temp'].reset_index()
fig = px.line(df_weather_fig,
             y='days_temp',
             x=df_weather_fig['days_datetime'].dt.dayofyear,
             color= df_weather_fig['days_datetime'].dt.year,
             title='Fig 1')
fig.update_traces({'hovertemplate':'%{y:.2}</b>', 'line_shape':'spline'} )
fig.update_layout({'hovermode':'x unified', "template":"plotly_dark"})

fig2 = px.bar(df_weather_fig,
             y='days_temp',
             x=df_weather_fig['days_datetime'].dt.dayofyear,
             color= df_weather_fig['days_datetime'].dt.year,
             title='Fig 2')
fig2.update_traces({'hovertemplate':'%{y:.2}</b>'})
fig2.update_layout({'hovermode':'x unified', "template":"plotly_dark"})

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

        dbc.Row(
            [
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span("Casos recuperados", className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_tempmax'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_1"),
                                html.Span("Em acompanhamento", className="card-text"),
                                html.H5(id="em-acompanhamento-text_1"),
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF"})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span("Casos recuperados", className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_temp'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_2"),
                                html.Span("Em acompanhamento", className="card-text"),
                                html.H5(id="em-acompanhamento-text_2"),
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF"})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span("Casos recuperados", className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_tempmin'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_3"),
                                html.Span("Em acompanhamento", className="card-text"),
                                html.H5(id="em-acompanhamento-text_3"),
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF"})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span("Casos recuperados", className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_windspeed'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_4"),
                                html.Span("Em acompanhamento", className="card-text"),
                                html.H5(id="em-acompanhamento-text_4"),
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF"})),
                dbc.Col(dbc.Card([   
                            dbc.CardBody([
                                html.Span("Casos recuperados", className="card-text"),
                                html.H3(children=df_weather[df_weather.index == df_weather.index.max()]['days_humidity'],
                                        style={"color": "#adfc92"}, id="casos-recuperados-text_5"),
                                html.Span("Em acompanhamento", className="card-text"),
                                html.H5(id="em-acompanhamento-text_5"),
                                ])
                            ], color="light", outline=True, style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                    "color": "#FFFFFF"}))
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                        [
                            dcc.Graph(id='example-graph', figure=fig)
                        ]
                ),
                dbc.Col(
                        [
                            dcc.Graph(id='example-graph2', figure=fig2)
                        ]
                )
            ], style={'margin-top': '10px'}
        )
    ], fluid=True
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

if __name__ == '__main__':
    app.run_server(debug=True)
