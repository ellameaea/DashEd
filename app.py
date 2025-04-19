import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output
from components.header import create_header
from components.tabs import create_tabs
from components.overview import create_overview_content
from components.density import create_density_content

# Initialize the app
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets' 
)

# Layout
app.layout = html.Div(
    children=[
        create_header(),
        html.Div(id="menu-output", style={"margin-top": "20px", "font-size": "18px"}),
        create_tabs(),
        html.Div(id="tab-content"),  # <- dynamic tab content goes here
    ],
    style={"margin": "0", "padding": "0", "background": "#f5f5f5"}
)

# Callback for tab switching
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_content(tab_value):
    if tab_value == "overview":
        return create_overview_content()
    elif tab_value == "density":
        return create_density_content()
    return html.Div("No content available.")

if __name__ == '__main__':
    app.run(debug=True)
