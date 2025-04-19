from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from components.overview import create_info_card



def create_two_column_layout(left_component, right_component):
    """Create a reusable two-column layout"""
    return html.Div([
        html.Div([left_component], style={"width": "63%"}),
        html.Div([right_component], style={"width": "33%"})
    ], style={
        "display": "flex", 
        "justify-content": "space-between",
        "margin-bottom": "20px"
    })

def create_density_content():
    """Create the main dashboard content using reusable components"""
    
    # Create charts
    card1_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card2_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card3_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")


    # Create components
    density_main = create_info_card("Title for Data Viz 1", card1_content)
    card1 = create_info_card("Title for Data Viz 2", card2_content)

    main_section = create_two_column_layout(density_main, card1)
    bottom_section = create_info_card("Title for Data Viz 3", card3_content)
    
    # Combine all components
    return html.Div([
        main_section,
        bottom_section,
    ], style={"max-width": "1400px", "margin": "0 auto", "padding": "20px"})
