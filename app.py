import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import uuid
import os
import base64
from callbacks import register_callbacks
import plotly.graph_objects as go
from components.header import create_header
from components.tabs import create_tabs
from components.upload_modal import upload_modal
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Indiv_private_deficiency import indiv_private_deficiency_chart
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Total_deficiency_private import private_deficiency_chart

from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Total_deficiency_public import public_deficiency_chart
from Data_Visualization.Density_Tab_Latest.Dropout_Deficiency.Indiv_public_deficiency import indiv_public_deficiency_chart

from Data_Visualization.Timelines_Analysis.Total_Enrollees_Timeline import get_enrollment_trend_figure, get_latest_total_enrollees

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
        upload_modal(),

        dcc.Store(id="upload-trigger", data=False),

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

# For Density Dropdown (Private)
@app.callback(
    Output('private-deficiency-graph', 'figure'),
    Input('private-deficiency-dropdown', 'value')
)
def update_private_deficiency_graph(selected_option):
    if selected_option == 'by_level':
        return indiv_private_deficiency_chart()
    return private_deficiency_chart()

# For Density Dropdown (Public)
@app.callback(
    Output('public-deficiency-graph', 'figure'),
    Input('public-deficiency-dropdown', 'value')
)
def update_public_deficiency_chart(selected_option):
    if selected_option == 'total':
        return public_deficiency_chart()
    else:
        return indiv_public_deficiency_chart()

dcc.Store(id="upload-trigger", data=False),

@app.callback(
    Output("upload-modal", "style"),
    [Input("open-upload", "n_clicks"),
     Input("close-upload", "n_clicks")],
    [State("upload-modal", "style")]
)
def toggle_modal(open_clicks, close_clicks, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_style
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "open-upload":
        return {**current_style, "display": "flex"}
    elif button_id == "close-upload":
        return {**current_style, "display": "none"}
    return current_style

@app.callback(
    Output("dataset-dropdown", "options"),
    Output("dataset-dropdown", "value"),
    Input("tabs", "value"),
    Input("upload-trigger", "data"),
    prevent_initial_call=False
)
def populate_dataset_dropdown(_, upload_trigger):
    folder = "CSV Files"
    csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    options = [{"label": f, "value": f} for f in csv_files]
    default_value = csv_files[-1] if csv_files else None  # Latest file uploaded
    return options, default_value

@app.callback(
    Output("upload-trigger", "data"),
    Input("upload-file", "contents"),
    Input("upload-file", "filename"),
    prevent_initial_call=True
)
def handle_upload(file_contents, file_name):
    if file_contents is not None:
        # Decode the file contents
        content_type, content_string = file_contents.split(',')
        decoded = base64.b64decode(content_string)

        # Save the file to the CSV folder
        file_path = os.path.join("CSV Files", file_name)
        with open(file_path, "wb") as f:
            f.write(decoded)

        # Trigger the dropdown to refresh
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
    