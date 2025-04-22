from dash import Input, Output, State, html
from components.overview import create_overview_content
from components.density import create_density_content
import os
import base64
import subprocess
import re
import pandas as pd
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
    
    # Upload & Process Excel Callback 
    # (tinry ko lang to hahaha pwede niyo idelete to kung may malagay kayo masokay)
    raw_excel_dir = '_Raw Excel Files' # Directory for storing raw excel files
    @app.callback(
        Output("upload-status", "children"),
        Output("processing-trigger", "data"),
        Input("upload-data", "contents"),
        State("upload-data", "filename")
    )
    def handle_file_upload(contents, filename, raw_excel_dir=raw_excel_dir):
        # Validate filename
        pattern = re.compile(r'SY \d{4}-\d{4} School Level Data on Official Enrollment.*\.xlsx')
        if not pattern.match(filename):
            return " Invalid filename format."

        try:
            # Save file
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            file_path = os.path.join(raw_excel_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(decoded)

            # Run external scripts
            subprocess.run(['python3', 'Data Cleaning/data-cleaning_1.py'], check=True)
            subprocess.run(['python3', 'Data Cleaning/combine_population.py'], check=True)

            return "File uploaded and processed successfully!"
        except Exception as e:
            return f" Error during processing: {e}"

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
