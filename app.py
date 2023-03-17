import dash
import dash_bootstrap_components as dbc
from dash import  html

app = dash.Dash(use_pages=True , 
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.MATERIA, dbc.icons.FONT_AWESOME])


sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("Data Weather", style={"color": "white"}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Dashboard")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-sharp fa-solid fa-sliders"),
                        html.Span("Detalhe"),
                    ],
                    href="/detalhe",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Datasets"),
                    ],
                    href="/datasets",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

app.layout = html.Div(
    [
        sidebar,
        html.Div(
            [
                dash.page_container
            ],
            className="content",
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)