from dash import html, dcc
import base64
import os

def upload_modal():
    return html.Div(
        id="upload-modal",
        style={
            "display": "none",  # Hidden by default
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "backgroundColor": "rgba(0,0,0,0.5)",
            "zIndex": "1000",
            "justifyContent": "center",
            "alignItems": "center"
        },
        children=html.Div(
            style={
                "backgroundColor": "#fff",
                "padding": "20px",
                "borderRadius": "8px",
                "width": "400px",
                "textAlign": "center",
                "position": "relative",
            },
            children=[
                html.Button("×", id="close-upload", n_clicks=0, style={
                    "position": "absolute",
                    "top": "10px",
                    "right": "10px",
                    "background": "transparent",
                    "border": "none",
                    "fontSize": "20px",
                    "cursor": "pointer",
                }),
                html.H3("Import Data Set"),
                dcc.Upload(
                    id='upload-file',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select File')
                    ]),
                    style={
                        "marginTop": "20px",
                        "padding": "20px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "cursor": "pointer"
                    },
                    multiple=False
                ),
                # Status message container
                html.Div(
                    id="upload-status",
                    style={
                        "marginTop": "20px",
                        "color": "#084683",
                        "fontSize": "16px",
                    }
                )
            ]
        )
    )
