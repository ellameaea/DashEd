from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from components.overview import create_info_card, create_two_column_layout
from Data_Visualization.Enrollee_and_School_Analysis.modified_COCs_count import fig



def create_density_content():
    """Create the main dashboard content using reusable components"""
    
    # Create charts
    card1_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card2_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card3_content = html.Div(dcc.Graph(id='stacked-bar-chart', figure=fig, config={'responsive': True},style={"width": "1215", "height": "100%"}),style={"height": "auto"})


    # Create components
    density_main = create_info_card("Title for Data Viz 1", card1_content, height=820)
    card1 = create_info_card("Title for Data Viz 2", card2_content, height = 820)

    main_section = create_two_column_layout(density_main, card1)
    bottom_section = create_info_card("Number of Schools by Region and Modified COC", card3_content, width="1215", height=None)
    
    # Combine all components
    return html.Div([
        main_section,
        bottom_section
    ], style={"max-width": "1400px", "margin": "0 auto", "padding": "20px"})
