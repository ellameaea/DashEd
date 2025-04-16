from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os

# ===== DATA FUNCTIONS =====
def get_pie_data():
    """Return sample data for pie chart"""
    return {
        'Category': ['Category 1', 'Category 2', 'Category 3'],
        'Value': [60, 30, 10]
    }

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


# ===== CHART CREATION FUNCTIONS =====
def create_pie_chart(data, hole_size=0.4, height=200, colors=None):
    """Create a reusable pie chart"""
    if colors is None:
        colors = ['#2D71B8', '#F7A823', '#EB5757']
        
    df = pd.DataFrame(data)
    fig = go.Figure(data=[go.Pie(
        labels=df['Category'],
        values=df['Value'],
        hole=hole_size,
        marker_colors=colors
    )])
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
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

# ===== UI COMPONENT FUNCTIONS =====
def create_header_banner(title, description, total_students, pie_chart_fig):
    """Create reusable header banner with title, description and chart"""
    return html.Div([
        # Left side - Title and description
        html.Div([
            html.H2(title, style={"fontFamily": "Revue", "color": "white", "font-size": "24px", "margin-bottom": "15px"}),
            html.P(
                description,
                style={"fontFamily": 'Montserrat', "color": "white", "font-size": "12px", "line-height": "1.4", "max-width": "90%"}
            ),
            html.A("Read Full Article →", href="#", style={"fontFamily": 'Montserrat', "color": "white", "font-size": "12px", "margin-top": "10px", "display": "block"})
        ], style={"width": "60%", "padding": "20px 30px"}),
        
        # Right side - Big number and chart
        html.Div([
            html.H2(f"{total_students:,}", style={"fontFamily": "Revue", "color": "white", "font-size": "32px", "font-weight": "bold", "margin-bottom": "5px", "text-align": "center"}),
            html.P("Total Students", style={"fontFamily": 'Montserrat', "color": "white", "font-size": "12px", "text-align": "center"}),
            dcc.Graph(
                figure=pie_chart_fig,
                config={'displayModeBar': False},
                style={"height": "150px", "width": "150px", "margin": "0 auto"}
            )
        ], style={"fontFamily": 'Montserrat', "width": "40%", "padding": "20px", "display": "flex", "flex-direction": "column", "justify-content": "center"})
    ], style={
        "display": "flex", 
        "backgroundImage": "linear-gradient(154deg,rgba(217, 217, 217, 1) 0%, rgba(8, 70, 131, 0.64) 55%, rgba(222, 8, 44, 1) 100%), url('/assets/library-background.png')",
        "background-size": "cover",
        "border-radius": "24px",
        "margin-bottom": "20px",
        "box-shadow": "0 2px 5px rgba(0,0,0,0.1)",
        "height": "100%",
        "width": "100%"
    })

def create_info_card(title, content, height=300, gradient="linear-gradient(133deg, rgba(249, 249, 249, 0.13) 0%, rgba(8, 70, 131, 1) 70%,rgba(222, 8, 44, 1) 80%"):
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
    """Create a reusable two-column layout"""
    return html.Div([
        html.Div([left_component], style={"width": "48%"}),
        html.Div([right_component], style={"width": "48%"})
    ], style={
        "display": "flex", 
        "justify-content": "space-between",
        "margin-bottom": "20px"
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
def create_main_content():
    """Create the main dashboard content using reusable components"""
    # Get data
    pie_data = get_pie_data()
    map_data = get_philippines_map_data()
    
    # Create charts
    pie_chart = create_pie_chart(pie_data)
    map_chart = dcc.Graph(
        figure=map_data,
        config={'displayModeBar': False},
        style={"height": "800px",'width':'200',"padding":"0","margin":"0"}
    )
    
    # Sample text content
    title = "What Constitutes to the Gender Disparity among Students from Kinder to Senior High School?"
    description = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. At venenatis quis morbi " +
                  "senectus ultrices at urna. Amet, facilisis mauris donec enim. Sed adipiscing " +
                  "aliquet ut faucibus eros. Fames in diam eu sollicitudin viverra enim. " +
                  "Egestas ac ultrices pellentesque sed ac aliquet accumsan.")
    
    card1_content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore."
    card2_content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore."
    card3_content = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore. " +
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore. " +
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore. " +
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
 
    
    # Create components
    header = create_header_banner(title, description, 13986745, pie_chart)
    
    card1 = create_info_card("Title for Data Viz 1", card1_content)
    card2 = create_info_card("Title for Data Viz 3", card2_content)
    stacked_cards = create_stacked_cards([card1, card2])
    
    big_card = create_info_card("Title for Data Viz 2", card3_content, height=620)
    middle_section = create_two_column_layout(stacked_cards, big_card)
    
    map_card = create_visualization_card(
        "Regional Gender Disparity in Enrollment",
        map_chart,
        "This heatmap highlights gender enrollment disparities per region across the Philippines.",
        height=890
    )
    ...
    
    # Combine all components
    return html.Div([
        header,
        middle_section,
        map_card
    ], style={"max-width": "1200px", "margin": "0 auto", "padding": "20px"})


