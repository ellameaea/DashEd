import dash
import dash_bootstrap_components as dbc
from dash import html
from components.header import create_header
from components.tabs import create_tabs
from callbacks import register_callbacks

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets',
    suppress_callback_exceptions=True    # ← add this
)

# Layout
app.layout = html.Div(
    children=[
        create_header(),
        html.Div(id="menu-output", style={"margin-top": "20px", "font-size": "18px"}),
        create_tabs(),
        html.Div(id="tab-content"),
    ],
    style={"margin": "0", "padding": "0", "background": "#f5f5f5"}
)

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
