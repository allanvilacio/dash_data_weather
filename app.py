from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
from utility.data_frames import get_d_cidades

# Data frames
d_cidades = get_d_cidades()


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "1rem 1rem",
    "background-color": "#424242",
}

CONTENT_STYLE = {
    "margin-left": "13rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",
}

app.layout = dbc.Container(
    [
        html.Div(
            [
                html.H2("Sidebar"),
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink(page['name'], href= page["relative_path"], active="exact")
			            for page in dash.page_registry.values()
                    ],
                    vertical=True,
                    pills=True,
                ),
		        html.Hr(),
                html.H5('Filtro'),

                dcc.Dropdown(id='location-dropdown', 
                    options=[{'label': label, 'value': value} 
			        for label, value in d_cidades[['nome_mun','codigo_ibge']].sort_values(by='nome_mun').values],
                    value='2704302')
            ],
            style=SIDEBAR_STYLE,
        ),
        html.Div(
            [
                dash.page_container,  

            ], style=CONTENT_STYLE
        )
            
    ], fluid= True
)

if __name__ == '__main__':
	app.run_server(debug=True)
