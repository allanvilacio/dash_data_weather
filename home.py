from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
from utility.data_frames import get_df_weather, get_d_cidades

# Data frames
df_weather = get_df_weather()
d_cidades = get_d_cidades()

#filtros
filtro_cidades = d_cidades['nome_mun'].unique().tolist()
filtro_cidades.append('Todas as cidades')

# Estilos e updates
update_traces = {'hovertemplate':'%{y:.2}</b>', 'line_shape':'spline'}
update_layout = {'hovermode':'x unified'}


app = Dash(__name__)
app.title = 'Data dash weather'


'''
df_weather_fig = df_weather.groupby(by='days_datetime').mean(numeric_only=True)['days_temp'].reset_index()
fig = px.line(df_weather_fig,
             y='days_temp',
             x=df_weather_fig['days_datetime'].dt.dayofyear,
             color= df_weather_fig['days_datetime'].dt.year)
fig.update_traces(update_traces)
fig.update_layout(update_layout)
'''

app.layout = html.Div(children=[

    html.H1(children='Data dash weather'),

    # Dropdown para colocar no layout
    dcc.Dropdown(filtro_cidades, 'Todas as cidades', id='filtro_cidades'),

    html.Div(id='teste_filtro_div', children=''),
    html.Div(id='teste_filtro_ibge', children='Ibge'),


    dcc.Graph(
        id='example-graph'),
    
    dash_table.DataTable(id='example-table',
                        columns=[{"name": i.upper(), "id": i, "presentation": "markdown"} for i in d_cidades.columns],
                        data=d_cidades.to_dict('records'))
])

@app.callback(
    [Output('teste_filtro_div', 'children'),
     Output('teste_filtro_ibge', 'children'),
     Output('example-graph', 'figure')],
    [Input('filtro_cidades', 'value')]
)
def update_filtros(input_value):

    teste_filtro_div = f'Dash: A web application framework for your data da cidade de {input_value}.'
    teste_filtro_ibge = d_cidades[d_cidades['nome_mun']==input_value]['codigo_ibge'].tolist()
    
    if input_value == 'Todas as cidades':
        df_weather_fig = df_weather
    else:
        df_weather_fig = df_weather.loc[df_weather['codigo_ibge'].isin(teste_filtro_ibge)]
    
    df_weather_fig = df_weather_fig.groupby(by=['days_datetime']).mean(numeric_only=True)['days_temp'].reset_index()
    
    fig = px.line(df_weather_fig,
                x=df_weather_fig['days_datetime'].dt.dayofyear,
                y='days_temp', 
                color=df_weather_fig['days_datetime'].dt.year)
    
    fig.update_traces(update_traces)
    fig.update_layout(update_layout)

    return teste_filtro_div, teste_filtro_ibge, fig



if __name__ == '__main__':
    app.run_server(debug=True)
