import pandas as pd
from dash import html
from dash.dependencies import Input, Output
from components.overview import create_overview_content
from components.density  import create_density_content
from Data_Visualization.Enrollee_Gender_Analysis.Totals_Gender_bar import gender_bar
from Data_Visualization.Enrollee_Gender_Analysis.Totals_SHS_bar   import gender_shs_bar

def register_callbacks(app):
    # Tab content renderer
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

    # Overview interactive chart updater
    @app.callback(
    Output("overview-graph","figure"),
    Input("overview-chart-dropdown","value"),
    Input("overview-region-dropdown","value")
)
    def update_overview(chart_type, region):
        df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")
        if region != "All Regions":
            df = df[df.Region == region]
        return gender_shs_bar(df) if chart_type == "shs" else gender_bar(df)