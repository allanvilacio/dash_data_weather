import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, State, dcc
from utility.data_frames import get_d_cidades

d_cidades = get_d_cidades()

app = dash.Dash(use_pages=True ,external_stylesheets=[dbc.themes.CYBORG])


app.layout = dbc.Container(
    [
        dbc.Offcanvas(
            [
                html.H2("Sidebar"),
                html.Hr(),
                html.P("A simple sidebar layout with navigation links"),
                dbc.Nav(
                    [
                        dbc.NavLink(page['name'], href= page["relative_path"], active="exact")
                        for page in dash.page_registry.values()
                    ],
                    vertical=True,
                    pills=True,
                ),
                dcc.DatePickerRange(
                        id='home-fildddtro-datas',
                        min_date_allowed=('2021-01-01'),
                        max_date_allowed=('2023-12-31'),
                        start_date =('2023-01-01'),
                        end_date=('2023-03-31') ,
                        display_format='DD/MM/YYYY'
                    )

            ],
            id="offcanvas-scrollable",
            scrollable=True,
            is_open=False, style={'width':'350px'}
        ),
        dash.page_container
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
    