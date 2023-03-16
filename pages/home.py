import dash
import pandas as pd
from dash import dcc ,html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from utility.data_frames import get_df_weather, get_d_cidades
import json
import plotly.express as px

token = open(".mapbox_token").read()
stados_brasil = json.load(open('database/geojson/brazil_geo.json', "r"))

d_cidades = get_d_cidades()
df_weather = get_df_weather()


dash.register_page(__name__, path='/')

layout = html.Div(children=
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Open",
                        id="open-offcanvas-scrollable",
                        n_clicks=0,
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(id='home-dropdown-tipo-visualizacao', 
                        options=[{'label': 'Regiões', 'value': 'regiao'},
                                    {'label': 'Estados', 'value': 'uf'}],
                        value = 'regiao'
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(id='location-dropdown-regiao',
                        options=d_cidades['regiao'].unique().tolist(),
                        multi=True, clearable=True, placeholder='Filtro por região'

                    ), md=3
                ),
                dbc.Col(
                    dcc.DatePickerRange(
                        id='home-filtro-datas',
                        min_date_allowed=('2021-01-01'),
                        max_date_allowed=('2023-12-31'),
                        start_date =('2023-01-01'),
                        end_date=('2023-03-31') ,
                        display_format='DD/MM/YYYY'
                    ), md=3
                ),
                dbc.Col(
                    dbc.Button(
                        'submit',
                        id='submit-button',
                        n_clicks=0,
                    ),md=1
                )
            ], style={ 'height': '80px', 'align-items': 'center'}
        ),
        dbc.Row(
            [
                dbc.Col(
                        [
                            dcc.Graph(id='home-histo'),
                            dcc.Graph(id='home-acumulado-precip')
                        ]
                    ,md=8),
                dbc.Col(
                    dcc.Graph(id='home-map'), md=4
                )
            ]
            
        ),
        dbc.Row(
            dcc.Graph(id='home-line')
        )
    ]
)

@callback(
    [
        Output('home-map', 'figure'),
        Output('home-histo', 'figure'),
        Output('home-line', 'figure'),
        Output('home-acumulado-precip', 'figure')
    ],
        Input('submit-button', 'n_clicks'),
    [
        State('home-filtro-datas', 'start_date'),
        State('home-filtro-datas', 'end_date'),
        State('location-dropdown-regiao', 'value'),
        State('home-dropdown-tipo-visualizacao', 'value')
    ]
)
def update_graphs(n_clicks, start_date, end_date, value_regiao, tipo_visualizacao):

    if value_regiao:
        filtro_regiao = d_cidades[d_cidades['regiao'].isin(value_regiao)]['codigo_ibge'].unique()
    else:
        filtro_regiao = d_cidades['codigo_ibge'].unique()

    df_weather_filtered = (df_weather[(df_weather['days_datetime'].isin(pd.date_range(start_date, end_date))) &
                                    (df_weather['codigo_ibge'].isin(filtro_regiao))]
                                [['days_datetime','days_temp','codigo_ibge', 'days_precip']])
    df_weather_filtered = df_weather_filtered.merge(d_cidades[['codigo_ibge', 'uf','regiao']], how='left')

    df_weather_filtered.sort_values(by=['regiao', 'uf', 'days_datetime'], 
                                    ignore_index=True, inplace=True)
    df_weather_filtered['days_precip_acum'] = df_weather_filtered.groupby(by=['codigo_ibge'])['days_precip'].cumsum()
    

    fig_map = px.choropleth_mapbox(
        df_weather_filtered.groupby(by=['uf','regiao'])['days_temp'].mean().reset_index(),
        locations='uf',
        color='days_temp',
        geojson = stados_brasil, 
        center={"lat": -16.50, "lon": -53.80},
        zoom=2.5, 
        opacity=1
    )

    fig_map.update_layout(
                    mapbox_accesstoken=token,
                    margin={"r":0,"t":0,"l":0,"b":0}
    )

    fig_histo = px.histogram(
        (df_weather_filtered.groupby(by=[tipo_visualizacao,'days_datetime'])['days_temp']
            .mean(numeric_only=True)
            .reset_index()
        ),
        x='days_temp', 
        color=tipo_visualizacao,
        nbins=20
    )
    
    fig_line = px.line(
        (df_weather_filtered.groupby(by=[tipo_visualizacao, 'days_datetime'])['days_temp']
            .mean(numeric_only=True)
            .reset_index()),
        color=tipo_visualizacao,
        x='days_datetime',
        y='days_temp',
    )

    fig_precip_cum = px.line(
        df_weather_filtered.groupby(by=[tipo_visualizacao, 'days_datetime']).sum(numeric_only=True).reset_index(),
        x='days_datetime',
        y='days_precip_acum',
        color = tipo_visualizacao
    )
    
    return fig_map, fig_histo, fig_line, fig_precip_cum