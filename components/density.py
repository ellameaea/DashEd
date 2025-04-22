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

# Path to the saved pie chart images
public_pie_chart_path = 'assets/public_pie_chart.png'
private_pie_chart_path = 'assets/private_pie_chart.png'

def create_density_content():
    """Create the main dashboard content using reusable components"""
    
    # Create charts
    card1_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card2_content = html.Div([ 
        html.Div(dcc.Graph(id='private-pie-chart', figure=private_pie_chart(), config={'responsive': True}, style={"height": "50%"})),
        html.Div(dcc.Graph(id='public-pie-chart', figure=public_pie_chart(), config={'responsive': True}, style={"height": "50%"}))
    ], style={"max-height": "820px", "display": "flex", "flexDirection": "column"})

    card3_content = html.Div(dcc.Graph(id='stacked-bar-chart', figure=fig, config={'responsive': True}, style={"height": "100%"}), style={"height": "auto"})
    
    # Create components
    density_main = create_info_card("Title for Data Viz 1", card1_content, height=820)
    card1 = create_info_card("", card2_content, height = 820)

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
