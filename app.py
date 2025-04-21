import dash
import dash_bootstrap_components as dbc
from dash import html
from components.header import create_header
from components.tabs import create_tabs
from callbacks import register_callbacks  # <== import your callback function
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets'
)

app = dash.Dash(__name__, suppress_callback_exceptions=True)

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

@app.callback(
    Output('region-level-heatmap', 'figure'),
    Input('level-dropdown', 'value')
)

def update_region_heatmap_figure(selected_level):
    from Data_Visualization.Overview_heatmap import get_region_heatmap_figure
    return get_region_heatmap_figure(selected_level)



if __name__ == '__main__':
    app.run(debug=True)


