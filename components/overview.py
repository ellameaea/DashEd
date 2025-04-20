from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os





# ===== DATA FUNCTIONS =====

def get_philippines_map_data():

    current_directory = os.getcwd()
    cleaned_file = os.path.join(current_directory, 'CSV Files/CLEANED_SY2023_Enrollment.csv')
    json_file = os.path.join(current_directory, 'ph.json')

    df = pd.read_csv(cleaned_file)
    with open(json_file) as f:
        ph_geojson = json.load(f)

    female_cols = [col for col in df.columns if 'Female' in col]
    male_cols = [col for col in df.columns if 'Male' in col]

    region_gender = df.groupby('Region')[female_cols + male_cols].sum()
    region_gender['Disparity'] = abs(region_gender[female_cols].sum(axis=1) - region_gender[male_cols].sum(axis=1))

    region_gender = region_gender[['Disparity']].reset_index()

    region_mapping = {
        'Region I': 'Ilocos',
        'Region II': 'Cagayan Valley',
        'Region III': 'Central Luzon',
        'Region IV-A': 'Calabarzon',
        'MIMAROPA': 'Mimaropa',
        'Region V': 'Bicol',
        'Region VI': 'Western Visayas',
        'Region VII': 'Central Visayas',
        'Region VIII': 'Eastern Visayas',
        'Region IX': 'Zamboanga Peninsula',
        'Region X': 'Northern Mindanao',
        'Region XI': 'Davao',
        'Region XII': 'Soccsksargen',
        'NCR': 'National Capital Region',
        'CAR': 'Cordillera Administrative Region',
        'BARMM': 'Autonomous Region in Muslim Mindanao',
        'CARAGA': 'Caraga'
    }

    region_gender['id'] = region_gender['Region'].map(region_mapping)

    fig = px.choropleth_mapbox(
        region_gender,
        geojson=ph_geojson,
        locations='id',
        color='Disparity',
        featureidkey='properties.name',
        center={'lat': 12.8797, 'lon': 121.7740},
        mapbox_style='carto-positron',
        zoom=5,
        color_continuous_scale='Plasma',
        labels={'Disparity': 'Gender Disparity'},
        hover_data={'Region': True, 'Disparity': True}
    )

    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>" +
                      "Gender Disparity: %{z}<extra></extra>"
    )
    
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    return fig


def create_philippines_map(data, color_scale=None, height=350):
    """Create a reusable Philippines map visualization"""
    if color_scale is None:
        color_scale = ['yellow', 'pink', 'purple']
        
    # In a real implementation, you would use px.choropleth with appropriate GeoJSON
    fig = px.choropleth(
        data,
        locations='region',
        color='value',
        color_continuous_scale=color_scale,
        scope="asia",
        labels={'value': 'Value'},
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showcoastlines=True,
            coastlinecolor="White",
            showland=True,
            landcolor="lightgrey",
            showocean=True,
            oceancolor="lightgrey",
            showlakes=False,
            showcountries=False,
            projection_scale=7,
            center=dict(lat=12.8797, lon=121.7740),  # Center on Philippines
        ),
        height=height,
    )
    
    return fig

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
            content if isinstance(content, (html.Div, dcc.Graph)) else html.P(content, style={
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
    # Get data
    map_data = get_philippines_map_data()
    
    # Create charts
    map_chart = dcc.Graph(
        figure=map_data,
        config={'displayModeBar': False},
        style={"height": "800px",'width':'200',"padding":"0","margin":"0"}
    )
    
    card1_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    card2_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")

    
    card3_graph = dcc.Graph(
    figure=get_enrollment_trend_figure(),
    config={'displayModeBar': False},
    style={"height": "500px", "width": "800px"}
)
 
    
    # Create components
    card1 = create_info_card("Title for Data Viz 1", card1_content, height = 300)
    card2 = create_info_card("Title for Data Viz 2", card2_content, height = 500)
    stacked_cards = create_stacked_cards([card1, card2])
    number= get_latest_total_enrollees()
    title = html.H3([
    html.Span(f"{number:,} ", style={
        
        "fontSize": "70px",
        "fontWeight": "bold",
        "background": "linear-gradient(45deg, #F9F9F9, #084683, #DE082C)",  
        "WebkitBackgroundClip": "text",  
        "color": "transparent",  
    }),
    "Enrollees"
    ])


    big_card = create_info_card(title, card3_graph, height=820)
    main_section = create_two_column_layout(big_card, stacked_cards)
    
    map_card = create_visualization_card(
        "Regional Gender Disparity in Enrollment",
        map_chart,
        "This heatmap highlights gender enrollment disparities per region across the Philippines.",
        height=890
    )
    
    # Combine all components
    return html.Div([
        main_section,
        map_card
    ], style={"max-width": "1400px", "margin": "0 auto", "padding": "20px"})


