import dash
import dash_bootstrap_components as dbc
from components.header import create_header
from components.main import create_main_content
from callbacks import register_callbacks

# Initialize the app
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets'  # Make sure you have an assets folder for storing images
)

# Assemble the layout
app.layout = dash.html.Div(
    children=[
        create_header(),
        dash.html.Div(id="menu-output", style={"margin-top": "20px", "font-size": "18px"}),
        create_main_content(),
    ],
    style={"margin": "0", "padding": "0", "background": "#f5f5f5"}
)

# Register all callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)