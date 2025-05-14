from dash import Input, Output, State, html, dcc, callback_context
from dash.exceptions import PreventUpdate
import os, base64, subprocess, re, pandas as pd
import pandas as pd
from components.overview import create_overview_content
from components.density import create_density_content
from Data_Visualization.Enrollee_Gender_Analysis.Totals_Gender_bar import gender_bar
from Data_Visualization.Enrollee_Gender_Analysis.Totals_SHS_bar import gender_shs_bar
from Data_Visualization.Overview_output import pie_chart_total_enrollees
from Data_Visualization.Timelines_Analysis.Total_Male_vs_Female_Time import enrollment_trend_by_gender
from Data_Visualization.Overview_heatmap import get_region_heatmap_figure

def register_callbacks(app):
    # 1. Render page content based on selected tab
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

    raw_excel_dir = "_Raw Excel Files"

    # 2. Show or hide the file upload component
    @app.callback(
        Output("upload-container", "children"),
        Input("show-upload-btn", "n_clicks")
    )
    def display_upload(n_clicks):
        if n_clicks and n_clicks > 0:
            return dcc.Upload(
                id="upload-data",
                children=html.Div(["Drag & Drop or ", html.A("Select a File")]),
                style={
                    "width": "200px",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center"
                },
                multiple=False
            )
        return html.Div()

    # 3. Handle file upload: save, process, and trigger data refresh
    @app.callback(
        Output("upload-status", "children"),
        Output("processing-trigger", "data"),
        Input("upload-data", "contents"),
        State("upload-data", "filename")
    )
    def handle_upload(contents, filename):
        if not contents or not filename:
            raise PreventUpdate
        # Validate filename pattern
        pattern = re.compile(r"SY \d{4}-\d{4} School Level Data on Official Enrollment.*\.xlsx")
        if not pattern.match(filename):
            return "Invalid filename format.", None
        try:
            _, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            filepath = os.path.join(raw_excel_dir, filename)
            with open(filepath, "wb") as f:
                f.write(decoded)
            # Run cleaning and combine scripts
            subprocess.run(["python3", "Data Cleaning/data_cleaning_1.py"], check=True)
            subprocess.run(["python3", "Data Cleaning/combine_population.py"], check=True)
            return "File uploaded and processed successfully!", "start_processing"
        except Exception as e:
            return f"Error during processing: {e}", None

    # 4. Reload dropdown options when a new CSV appears
    @app.callback(
        Output("dataset-select", "options"),
        Input("upload-status", "children")
    )
    def refresh_dropdown(_msg):
        files = [f for f in os.listdir("CSV Files") if f.endswith(".csv")]
        return [{"label": f, "value": f} for f in files]

    # 5. Update overview graph based on stored-data and filters
    @app.callback(
        Output("overview-graph", "figure"),
        Input("overview-chart-dropdown", "value"),
        Input("overview-region-dropdown", "value"),
        State("stored-data", "data")
    )
    def update_overview(chart_type, region, stored_data):
        df = pd.DataFrame(stored_data or [])
        if region and region != "All Regions":
            df = df[df.Region == region]
        return gender_shs_bar(df) if chart_type == "shs" else gender_bar(df)

    # 6. Show which dataset is active, with row/column counts
    @app.callback(
        Output("dataset-info", "children"),
        Input("dataset-select", "value"),
        State("stored-data", "data")
    )
    def show_dataset_info(filename, stored_data):
        if not filename or not stored_data:
            return "No dataset loaded."
        df = pd.DataFrame(stored_data)
        rows, cols = df.shape
        return f"Showing “{filename}” ({rows} rows × {cols} columns)"

    # 7. Single callback to update stored-data from either a file import or dataset selection
    @app.callback(
        Output("stored-data", "data"),
        Input("processing-trigger", "data"),
        Input("dataset-select", "value")
    )
    def update_stored_data(trigger, fname):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        prop = ctx.triggered[0]["prop_id"]
        # Priority to processing-trigger
        if "processing-trigger.data" in prop:
            if trigger == "start_processing":
                df = pd.read_csv(os.path.join("CSV Files", "CLEANED_SY2023_Enrollment.csv"))
            else:
                raise PreventUpdate
        # Fallback to dataset-select
        elif "dataset-select.value" in prop:
            if not fname:
                raise PreventUpdate
            df = pd.read_csv(os.path.join("CSV Files", fname))
        else:
            raise PreventUpdate
        return df.to_dict("records")
    

    #  ❏ Pie chart
    @app.callback(Output("pie-chart","figure"), 
                  Input("stored-data","data"))
    
    def update_pie(_):
        return pie_chart_total_enrollees.figure


    #  ❏ Trend chart
    @app.callback(Output("trend-chart","figure"), 
                  Input("stored-data","data"))
    def update_trend(_):
        return enrollment_trend_by_gender

    #  ❏ Region heatmap
    @app.callback(Output("region-heatmap","figure"),
                Input("level-dropdown","value"))
    def update_heatmap(level):
        return get_region_heatmap_figure(selected_level=level)

    #  8. Auto-refresh region dropdown options when data changes
    @app.callback(
        Output("overview-region-dropdown", "options"),
        Input("stored-data", "data")
    )
    def update_region_options(data):
        df = pd.DataFrame(data or [])
        regions = ["All Regions"] + sorted(df.Region.dropna().unique().tolist())
        return [{"label": r, "value": r} for r in regions]

    @app.callback(
        Output("combined-levels-pie","figure"),
        Input("stored-data","data")
    )
    def update_pie(data):
        df = pd.DataFrame(data or [])
        return pie_chart_total_enrollees(df)

