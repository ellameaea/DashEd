from dash import dcc, html

def create_tabs():
    return html.Div(
        style={
            "padding": "0 80px",  # Adjusted padding to align with the main content
        },
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "flex-end",
                },
                children=[
                    dcc.Tabs(
                        id='tabs',
                        value='overview',
                        children=[
                            dcc.Tab(
                                label='Overview',
                                value='overview',
                                style={
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "16px",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "border": "none",
                                    "borderBottom": "3px solid transparent",
                                    "boxShadow": "none",
                                    "fontWeight": "normal",
                                    "padding": "6px 0",
                                    "cursor": "pointer",
                                    "lineHeight": "1.5",
                                    "position": "relative",
                                    "zIndex": "1",
                                    "paddingBottom": "12px"
                                },
                                selected_style={
                                    "fontWeight": "bold",
                                    "border": "none",
                                    "borderBottom": "3px solid #084683",
                                    "boxShadow": "none",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "padding": "6px 0 12px 0",
                                    "lineHeight": "1.5",
                                    "position": "relative",
                                    "zIndex": "1"
                                }
                            ),
                            dcc.Tab(
                                label='Density',
                                value='density',
                                style={
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "16px",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "border": "none",
                                    "borderBottom": "3px solid transparent",
                                    "boxShadow": "none",
                                    "fontWeight": "normal",
                                    "padding": "6px 0",
                                    "cursor": "pointer",
                                    "lineHeight": "1.5",
                                    "position": "relative",
                                    "zIndex": "1",
                                    "paddingBottom": "12px"
                                },
                                selected_style={
                                    "fontWeight": "bold",
                                    "border": "none",
                                    "borderBottom": "3px solid #084683",
                                    "boxShadow": "none",
                                    "color": "#084683",
                                    "backgroundColor": "transparent",
                                    "padding": "6px 0 12px 0",
                                    "lineHeight": "1.5",
                                    "position": "relative",
                                    "zIndex": "1"
                                }
                            ),
                        ],
                        style={"display": "flex", "gap": "24px"}
                    ),
                    html.Div(
                        children=[
                                dcc.Dropdown(
                                    id="dataset-dropdown",
                                    placeholder="Select Data Set",
                                    style={
                                        "minWidth": "200px",
                                        "marginRight": "10px",
                                        "fontFamily": "Montserrat, sans-serif",
                                        "fontSize": "14px",
                                    }
                                ),
                                html.Button("+ Import Data Set", id="open-upload", n_clicks=0, style={
                                "fontFamily": "Montserrat, sans-serif",
                                "fontSize": "14px",
                                "padding": "6px 16px",
                                "backgroundColor": "transparent",
                                "color": "#084683",
                                "border": "2px solid #DE082C",
                                "borderRadius": "999px",
                                "cursor": "pointer",
                            }),
                        ],
                        style={"display": "flex", "alignItems": "center", "paddingBottom": "12px"}
                    )
                ]
            ),
            html.Div(
                style={
                    "width": "100%",
                    "borderBottom": "1px solid #ccc",
                    "marginTop": "0",  
                    "position": "relative",
                    "zIndex": "0"
                }
            )
        ]
    )
