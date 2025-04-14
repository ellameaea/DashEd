from dash import html, dcc

def create_header():
    return html.Header(
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
    )