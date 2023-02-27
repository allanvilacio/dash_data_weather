from dash import Dash, dcc ,html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from utility.data_frames import get_df_weather, get_d_cidades

# Data frames
df_weather = get_df_weather()
d_cidades = get_d_cidades()

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

df_weather_fig = df_weather.groupby(by='days_datetime').mean(numeric_only=True)['days_temp'].reset_index()
fig = px.line(df_weather_fig,
             y='days_temp',
             x=df_weather_fig['days_datetime'].dt.dayofyear,
             color= df_weather_fig['days_datetime'].dt.year,
             title='Fig 1')
fig.update_traces({'hovertemplate':'%{y:.2}</b>', 'line_shape':'spline'})
fig.update_layout({'hovermode':'x unified'})

fig2 = px.bar(df_weather_fig,
             y='days_temp',
             x=df_weather_fig['days_datetime'].dt.dayofyear,
             color= df_weather_fig['days_datetime'].dt.year,
             title='Fig 2')
fig2.update_traces({'hovertemplate':'%{y:.2}</b>'})
fig2.update_layout({'hovermode':'x unified'})

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
                dbc.Col(html.Div("One of three columns1"),width="auto"),
                dbc.Col(html.Div("One of three columns2"),width="auto", align='center'),
                dbc.Col(html.Div("One of three columns3"),width="auto", align='center'),
                dbc.Col(html.Div("One of three columns4"),width="auto", align='center'),
                dbc.Col(html.Div("One of three columns5"),width="auto", align='center')
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
                            dcc.Graph(id='example-graph', figure=fig2)
                        ]
                )
            ], style={'margin-top': '10px'}  
    
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
        print(n1)
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)
