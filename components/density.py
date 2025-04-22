from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from components.overview import create_info_card, create_two_column_layout
from Data_Visualization.Enrollee_and_School_Analysis.modified_COCs_count import fig
from Data_Visualization.density_piecharts import public_pie_chart, private_pie_chart
from Data_Visualization.density_datavis1 import get_total_schools, get_school_crowding_figure, generate_heatmap

total_schools = get_total_schools()

# Path to the saved pie chart images
public_pie_chart_path = 'assets/public_pie_chart.png'
private_pie_chart_path = 'assets/private_pie_chart.png'

def create_density_content():
    """Create the main dashboard content using reusable components"""
    
    # Create charts
    card1_content = html.Div([
    html.Div([
        html.Div(f"{total_schools:,}", style={
            'fontSize': '130px',
            'fontWeight': '400',
            'background': 'linear-gradient(90deg, rgba(8, 70, 131, 0.47) 0%, rgba(222, 8, 44, 1) 100%)',
            'WebkitBackgroundClip': 'text',
            'WebkitTextFillColor': 'transparent',
            'backgroundClip': 'text',
            'color': 'transparent',
            'fontFamily': 'Revue, Helvetica',
            'lineHeight': '1',
            'letterSpacing': '-5px',
            'marginTop': '0',
            'marginBottom': '0',
            'padding': '0',
        }),
        html.Div([
            html.H4("Schools", style={
                'marginTop': '5px',
                'color': '#084683',
                'fontFamily': 'Montserrat',
                'fontSize': '24px',
                'textAlign': 'left',
                'padding': '0',
            }),
        ])
    ], style={'padding': '0 5px', 'margin': '0'}),

    html.Div([
        dcc.Graph(id='school-crowding-chart', figure=get_school_crowding_figure(), config={'responsive': True})
    ], style={"paddingTop": "0"}),

    html.Div([  # This is the corrected block
        html.H4(style={
            "textAlign": "center", 
            "marginTop": "10px",  
            "fontFamily": "Montserrat"
        }),
        html.Div([
            dcc.Graph(id='heatmap-graph', figure=generate_heatmap('G11'), config={'responsive': True})
        ], style={"display": "flex", "justifyContent": "flex-end"})  # Align the graph to the right
    ], style={"paddingTop": "0"})  # Ensure this is correctly closed
])

    card2_content = html.Div([ 
        html.Div(dcc.Graph(id='private-pie-chart', figure=private_pie_chart(), config={'responsive': True}, style={"height": "50%"})),
        html.Div(dcc.Graph(id='public-pie-chart', figure=public_pie_chart(), config={'responsive': True}, style={"height": "50%"}))
    ], style={"max-height": "820px", "display": "flex", "flexDirection": "column"})

    card3_content = html.Div(dcc.Graph(id='stacked-bar-chart', figure=fig, config={'responsive': True}, style={"height": "100%"}), style={"height": "auto"})
    
    # Create components
    density_main = create_info_card("", card1_content, height=1500)
    card1 = create_info_card("", card2_content, height = 1000)

    main_section = create_two_column_layout(density_main, card1)
    bottom_section = create_info_card("Number of Schools by Region and Modified COC", card3_content,width="100%", height=None)

    # Combine all components
    return html.Div([
        main_section,
        bottom_section
    ], style={
        "max-width": "1400px", 
        "margin": "0 auto", 
        "padding": "20px", 
        "display": "flex", 
        "flexDirection": "column",  
        "boxSizing": "border-box"
    })
