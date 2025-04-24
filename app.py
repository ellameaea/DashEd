
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import pandas as pd
from callbacks import register_callbacks
import plotly.graph_objects as go
from components.header import create_header
from components.tabs import create_tabs
# from flask_caching import Cache

# cache = Cache(app.server, config={"CACHE_TYPE": "simple"})

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets',
    suppress_callback_exceptions=True
)

import pandas as pd

app.layout = html.Div(
    children=[
        create_header(),  # ✅ Always visible

        dcc.Store(id="stored-data", data=pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv").to_dict('records')),

        html.Div(id="menu-output", style={"margin-top": "20px", "font-size": "18px"}),

        dcc.Loading(
            id="global-loading",
            type="circle",
            color="#084683",
            children=html.Div([
                create_tabs(),
                html.Div(id="tab-content"),
            ]),
            style={
                "position": "fixed",
                "top": "0",
                "left": "0",
                "width": "100vw",
                "height": "100vh",
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "backgroundColor": "rgba(255,255,255,0.5)",
                "zIndex": "9999"
            }
        ),
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
