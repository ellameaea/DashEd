from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from Data_Visualization.Overview_output import pie_chart_total_enrollees
from Data_Visualization.phmap import phmap
from Data_Visualization.Timelines_Analysis.Total_Male_vs_Female_Time import enrollment_trend_by_gender
from Data_Visualization.Enrollee_Gender_Analysis.Totals_Gender_bar import gender_bar
from Data_Visualization.Enrollee_Gender_Analysis.Totals_SHS_bar import gender_shs_bar



def create_info_card(title, content, height=300, width=None, gradient="linear-gradient(133deg, rgba(249, 249, 249, 0.13) 0%, rgba(8, 70, 131, 1) 70%,rgba(222, 8, 44, 1) 80%"):
    """Create reusable info card with gradient border"""
    return html.Div([
        # Inner card content
        html.Div([
            html.H3(title, style={
                "fontFamily": "Revue",
                "color": "#2D71B8",
                "fontSize": "16px",
                "fontWeight": "bold",
                "marginBottom": "10px"
            }),
            html.P(content, style={
                "fontFamily": 'Montserrat',
                "fontSize": "12px",
                "color": "#333"
            })
        ], style={
            "padding": "15px 20px",
            "background": "white",
            "borderRadius": "8px",
            "height": f"{height}px",  # Fixed height for consistent sizing
            "width": f"{width}px" if width else "auto",
            "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
        })
    ], style={
        "background": gradient,
        "padding": "2px",  # Thickness of the gradient border
        "borderRadius": "10px",
        "display": "inline-block"
    })

def create_visualization_card(title, chart_component, description=None, height=350, gradient="linear-gradient(133deg, rgba(249, 249, 249, 0.13) 0%, rgba(8, 70, 131, 1) 70%,rgba(222, 8, 44, 1) 80%"):
    """Create reusable visualization card with optional description and gradient border"""
    # Inner card content
    children = [
        html.H3(title, style={
            "fontFamily": "Revue",
            "color": "#2D71B8",
            "fontSize": "16px",
            "fontWeight": "bold",
            "marginBottom": "10px"
        }),
    ]
    
    if description:
        children.append(html.P(description, style={
            "fontFamily": 'Montserrat',
            "fontSize": "12px",
            "color": "#333",
            "marginBottom": "10px"
        }))
    
    children.append(html.Div(chart_component, style={
        "flexGrow": "1",
        "height": "100%",
        "overflow": "hidden"
    }))
    
    # Gradient-bordered box
    return html.Div([
        html.Div(children, style={
            "width": "100%",
            "background": "white",
            "borderRadius": "8px",
            "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
            "padding": "10px",
            "height": f"{height}px" if height else "auto"
        })
    ], style={
        "background": gradient,
        "padding": "2px",
        "borderRadius": "10px",
        "display": "inline-block",
        "width": "100%"
    })

def create_two_column_layout(left_component, right_component):
    """Create a reusable two-column layout with responsive and balanced design."""
    return html.Div([
        html.Div(
            [left_component],
            style={
                "flex": "1 1 60%",
                "minWidth": "300px",
                "display": "flex",
                "flexDirection": "column"
            }
        ),
        html.Div(
            [right_component],
            style={
                "flex": "1 1 35%",
                "minWidth": "250px",
                "display": "flex",
                "flexDirection": "column"
            }
        )
    ], style={
        "display": "flex",
        "flexWrap": "wrap",            
        "justifyContent": "space-between",
        "alignItems": "stretch",       
        "gap": "20px",                 
        "marginBottom": "20px"
    })

def create_stacked_cards(cards_list):
    """Create a stack of cards in a single column"""
    return html.Div(
        cards_list,
        style={
            "display": "flex",
            "flex-direction": "column",
            "gap": "20px"
        }
    )

# ===== MAIN LAYOUT FUNCTION =====
def create_overview_content():
    """Create the main dashboard content using reusable components"""
    Total_male_vs_female_enrollees_content = dcc.Graph(figure=enrollment_trend_by_gender)
    gender_total_bar_content = gender_bar()
    Total_Gender_Bar = dcc.Graph(figure=gender_total_bar_content)
    gender_shs_bar_content = gender_shs_bar()
    Total_SHS_Bar = dcc.Graph(figure=gender_shs_bar_content)
    Enrollment_sex_distribution_content = (Total_male_vs_female_enrollees_content, Total_Gender_Bar, Total_SHS_Bar)
    card3_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore. " +
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore. " +
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore. " +
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
 
    
    # Create components
    Pie_chart_total_enrollees = create_info_card("Total Enrollees by Level", pie_chart_total_enrollees, height = 450)
    Enrollment_sex_distribution = create_info_card("Enrollment Sex Distribution", Enrollment_sex_distribution_content, height = 1200)
    stacked_visualization = create_stacked_cards([Pie_chart_total_enrollees, Enrollment_sex_distribution])
    
    big_card = create_info_card("Title for Data Viz 3", card3_content, height=820)
    main_section = create_two_column_layout(big_card, stacked_visualization)
    
    phmap_section = create_visualization_card(
        "Regional Total Enrollment",
        dcc.Graph(figure=phmap()),
        "This heatmap highlights the total enrollment of students per region across the Philippines.",
        height=880
    )
    
    # Combine all components
    return html.Div([
        main_section,
        phmap_section
    ], style={"max-width": "1400px", "margin": "0 auto", "padding": "10px"})


