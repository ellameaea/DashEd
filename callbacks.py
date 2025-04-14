from dash import Input, Output, State, callback_context, html
from dash.exceptions import PreventUpdate
import json

def register_callbacks(app):
    # Callback to Show/Hide Dropdown Menu
    @app.callback(
        Output("dropdown-menu", "style"),
        [Input("menu-button", "n_clicks"),
         Input("close-menu", "n_clicks")],
        State("dropdown-menu", "style"),
        prevent_initial_call=True
    )
    def toggle_dropdown(menu_clicks, close_clicks, current_style):
        ctx = callback_context
        if not ctx.triggered:
            return current_style
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "menu-button":
            if not current_style or current_style.get("display") == "none":
                return {**current_style, "display": "block"}
        return {**current_style, "display": "none"}

    # Callback to Handle Clicks on Menu Items
    @app.callback(
        Output("menu-output", "children"),
        [Input("user-btn", "n_clicks"),
         Input("calendar-btn", "n_clicks"),
         Input("statistics-btn", "n_clicks"),
         Input("settings-btn", "n_clicks")]
    )
    def menu_action(user, calendar, stats, settings):
        ctx = callback_context
        if not ctx.triggered:
            return ""

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        menu_map = {
            "user-btn": "User Profile clicked!",
            "calendar-btn": "Calendar opened!",
            "statistics-btn": "Statistics page loading...",
            "settings-btn": "Settings menu opened!"
        }
        return menu_map.get(button_id, "")

    # Add more callbacks as needed


def register_callbacks(app):
    # Menu callbacks
    @app.callback(
        Output("dropdown-menu", "style"),
        [Input("menu-button", "n_clicks"),
         Input("close-menu", "n_clicks")],
        State("dropdown-menu", "style")
    )
    def toggle_dropdown(menu_clicks, close_clicks, current_style):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate
        
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "menu-button":
            return {**current_style, "display": "block"}
        return {**current_style, "display": "none"}

    # SVG Map callbacks
    @app.callback(
        Output('svg-container', 'children'),
        Input('svg-store', 'data')
    )
    def display_svg(svg_data):
        if not svg_data:
            try:
                with open('assets/philippines_map.svg', 'r') as f:
                    svg_data = f.read()
                svg_data = svg_data.replace('<svg', '<svg id="philippines-map"')
                return html.Iframe(
                    srcDoc=svg_data,
                    style={"width": "100%", "height": "350px", "border": "none"}
                )
            except FileNotFoundError:
                return html.Div("Map not found", style={"color": "red"})
        raise PreventUpdate

    # Region selection callback
    @app.callback(
        Output('region-info', 'children'),
        Input('region-clicked', 'children'),
        prevent_initial_call=True
    )
    def update_region_info(region_id):
        if region_id:
            return f"Selected region: {region_id}"
        return "Click on a region to select"

    # Clientside callback for map interactions
    app.clientside_callback(
        """
        function() {
            function addInteractivity() {
                const svg = document.getElementById('philippines-map');
                if (!svg) {
                    setTimeout(addInteractivity, 200);
                    return;
                }
                
                const paths = svg.querySelectorAll('path');
                paths.forEach(path => {
                    path.addEventListener('click', function() {
                        const event = new CustomEvent('regionSelected', {
                            detail: { regionId: this.id }
                        });
                        document.dispatchEvent(event);
                    });
                });
            }
            addInteractivity();
            
            return '';
        }
        """,
        Output('region-clicked', 'children'),
        Input('svg-container', 'children')
    )