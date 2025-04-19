from dash import Input, Output, html
from components.overview import create_overview_content
from components.density import create_density_content

def register_callbacks(app):
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
