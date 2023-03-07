from dash import Dash, html, dcc, Input, Output, State, callback
import dash
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container(
    [
        dbc.Button(
            "Open scrollable offcanvas",
            id="open-offcanvas-scrollable",
            n_clicks=0,
        ),
        dbc.Offcanvas(
            [
                html.P("The contents on the main page are now scrollable."),
                dbc.Nav(
                    [
                        dbc.NavLink(page['name'], href= page["relative_path"], active="exact") for page in dash.page_registry.values()

                    ],
                    vertical=True,
                    pills=True,
                )
            ],
            id="offcanvas-scrollable",
            scrollable=True,
            title="Scrollable Offcanvas",
            is_open=False,
        ),
        html.H1('Multi-page app with Dash Pages', style={'text-align':'center'}),
        dash.page_container,              
    ], fluid= True
)

@callback(
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
