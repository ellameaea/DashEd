import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc  # Using Bootstrap for styling

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# List of 17 Philippine regions
philippine_regions = [
    "Ilocos Region (Region I)",
    "Cagayan Valley (Region II)",
    "Central Luzon (Region III)",
    "CALABARZON (Region IV-A)",
    "MIMAROPA (Region IV-B)",
    "Bicol Region (Region V)",
    "Western Visayas (Region VI)",
    "Central Visayas (Region VII)",
    "Eastern Visayas (Region VIII)",
    "Zamboanga Peninsula (Region IX)",
    "Northern Mindanao (Region X)",
    "Davao Region (Region XI)",
    "SOCCSKSARGEN (Region XII)",
    "Caraga (Region XIII)",
    "Cordillera Administrative Region (CAR)",
    "National Capital Region (NCR)",
    "Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)"
]

app.layout = html.Div(
    children=[
        # Header
        html.Header(
            children=[
                html.Div(
                    [
                        # ☰ Menu Button
                        html.Div(
                            "☰",
                            id="menu-button",
                            style={"font-size": "24px", "cursor": "pointer", "position": "relative"}
                        ),
                        
                        # Dropdown Menu (Initially Hidden)
                        html.Div(
                            id="dropdown-menu",
                            children=[
                                # Close button (X) at the top right
                                html.Div(
                                    "✕",
                                    id="close-menu",
                                    style={
                                        "position": "absolute",
                                        "top": "5px",
                                        "right": "10px",
                                        "cursor": "pointer",
                                        "font-size": "18px"
                                    }
                                ),
                                html.Div("User", id="user-btn", n_clicks=0, className="dropdown-item"),
                                html.Div("Calendar", id="calendar-btn", n_clicks=0, className="dropdown-item"),
                                html.Div("Statistics", id="statistics-btn", n_clicks=0, className="dropdown-item"),
                                html.Div("Settings", id="settings-btn", n_clicks=0, className="dropdown-item"),
                            ],
                            style={
                                "position": "absolute",
                                "top": "40px",
                                "left": "0",
                                "background": "white",
                                "border": "1px solid #ddd",
                                "border-radius": "5px",
                                "box-shadow": "0 2px 5px rgba(0,0,0,0.2)",
                                "display": "none",
                                "padding": "10px",
                                "min-width": "120px",
                                "z-index": "1000",
                            }
                        ),

                        html.Img(
                            src="https://via.placeholder.com/150",
                            style={"height": "150px", "width": "150px"},
                        ),
                        html.Div(
                            [
                                html.P("*Username*", style={"margin": "0", "font-weight": "bold"}),
                                html.Img(
                                    src="https://via.placeholder.com/150",
                                    style={
                                        "height": "50px",
                                        "width": "50px",
                                        "border-radius": "50%",
                                        "margin-left": "10px",
                                    }
                                )
                            ],
                            style={"display": "flex", "align-items": "center", "gap": "10px"},
                        )
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                        "align-items": "center",
                        "width": "100%",
                        "max-width": "1200px",
                        "margin": "0 auto",
                        "position": "relative",
                    },
                )
            ],
            style={
                "background-color": "#b3b3b3",
                "padding": "10px 0 10px 0px",
                "border-radius": "0 0 20px 20px",
                "box-shadow": "0px 4px 6px -2px gray",
                "margin": "0 30px 30px 30px",
            },
        ),

        # Placeholder for Clicked Menu Item
        html.Div(id="menu-output", style={"margin-top": "20px", "font-size": "18px"}),

        # Main Content
        html.Div(
            children=[
                # Left Section
                html.Div(
                    children=[
                        html.H1("Welcome back, *User*!"),
                        html.P("Lorem ipsum dolor sit amet"),
                        
                        # Search Bar
                        html.Div(
                            [
                                dcc.Input(
                                    id='search-input',
                                    type='text',
                                    placeholder='Search...',
                                    style={
                                        'width': '100%',
                                        'padding': '10px',
                                        'border-radius': '20px',
                                        'border': '1px solid #ccc',
                                        'font-size': '16px'
                                    }
                                ),
                                html.Button(
                                    'Search',
                                    id='search-button',
                                    style={
                                        'margin-top': '10px',
                                        'padding': '10px 20px',
                                        'background-color': '#b3b3b3',
                                        'border': 'none',
                                        'border-radius': '20px',
                                        'cursor': 'pointer'
                                    }
                                )
                            ],
                            style={'margin-top': '20px'}
                        ),
                        
                        # Regions Figure Box (Two Columns)
                        html.Div(
                            [
                                html.H3("Lorem ipsum dolor sit amet", style={'margin-bottom': '10px'}),
                                html.Div(id='regions-container', children=[
                                    html.Button(
                                        region,
                                        id={'type': 'region-btn', 'index': region},
                                        style={
                                            'display': 'inline-block',
                                            'width': '48%',  # Ensures two columns
                                            'padding': '10px',
                                            'margin': '5px 1%',  # Adds spacing between buttons
                                            'background-color': '#f0f0f0',
                                            'border': '1px solid #ddd',
                                            'border-radius': '5px',
                                            'cursor': 'pointer',
                                            'text-align': 'left',
                                            'min-width': '150px'  # Ensures it looks good on smaller screens
                                        }
                                    ) for region in philippine_regions
                                ], style={
                                    'display': 'flex',
                                    'flex-wrap': 'wrap',
                                    'justify-content': 'space-between'
                                }),
                                # Empty div to display provinces when a region is clicked
                                html.Div(id='provinces-container', style={'margin-top': '20px'})
                            ],
                            style={
                                'margin-top': '30px',
                                'padding': '20px',
                                'background-color': '#f0f0f0',
                                'border-radius': '10px',
                                'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
                                'border': '1px solid #CE1126'
                            }
                        )
                    ],
                    style={"flex": "2", "padding": "20px"},
                ),

                # Right Sidebar
                html.Div(
                    children=[
                        html.Div(style={"background": "#b3b3b3", "height": "200px", "width": "500px", "border-radius": "20px"}),
                        html.Div(style={"background": "#b3b3b3", "height": "200px", "width": "500px", "border-radius": "20px"}),
                        html.Div(style={"background": "#b3b3b3", "height": "200px", "width": "500px", "border-radius": "20px"}),
                        html.Div(style={"background": "#b3b3b3", "height": "200px", "width": "500px", "border-radius": "20px"}),
                    ],
                    style={"flex": "1", "display": "flex", "flex-direction": "column", "gap": "10px", "padding": "20px"},
                ),
            ],
            style={"display": "flex", "max-width": "1200px", "margin": "0 auto"},
        ),
    ],
    style={"margin": "0", "padding": "0"},
)


# Callback to Show/Hide Dropdown Menu
@callback(
    Output("dropdown-menu", "style"),
    [Input("menu-button", "n_clicks"),
     Input("close-menu", "n_clicks")],
    State("dropdown-menu", "style"),
    prevent_initial_call=True
)
def toggle_dropdown(menu_clicks, close_clicks, current_style):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_style
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "menu-button":
        if not current_style or current_style.get("display") == "none":
            return {**current_style, "display": "block"}
    return {**current_style, "display": "none"}

# Callback to Handle Clicks on Menu Items
@callback(
    Output("menu-output", "children"),
    [Input("user-btn", "n_clicks"),
     Input("calendar-btn", "n_clicks"),
     Input("statistics-btn", "n_clicks"),
     Input("settings-btn", "n_clicks")]
)
def menu_action(user, calendar, stats, settings):
    ctx = dash.callback_context
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

if __name__ == '__main__':
    app.run(debug=True)