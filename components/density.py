from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from components.overview import create_info_card, create_two_column_layout


def create_density_content():
    """Create the main dashboard content using reusable components"""
    
    # Create charts
    card1_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card2_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card3_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")


    # Create components
    density_main = create_info_card("Title for Data Viz 1", card1_content, height=820)
    card1 = create_info_card("Title for Data Viz 2", card2_content, height = 820)

    main_section = create_two_column_layout(density_main, card1)
    bottom_section = create_info_card("Title for Data Viz 3", card3_content, width= 1355)
    
    # Combine all components
    return html.Div([
        main_section,
        bottom_section
    ], style={"max-width": "1400px", "margin": "0 auto", "padding": "20px"})
