# Data_Visualization/overview_layout.py

import pandas as pd
from dash import html, dcc
from Data_Visualization.Overview_output import pie_chart_total_enrollees
from Data_Visualization.phmap import phmap
from Data_Visualization.Timelines_Analysis.Total_Male_vs_Female_Time import enrollment_trend_by_gender
from Data_Visualization.Timelines_Analysis.Total_Enrollees_Timeline import get_enrollment_trend_figure, get_latest_total_enrollees
from Data_Visualization.Overview_heatmap import get_region_heatmap_figure

# ——— Data & Region List ———
DF = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")
REGIONS = ["All Regions"] + sorted(DF["Region"].dropna().unique().tolist())

# ——— Helper: Info Card ———
def create_info_card(title, content, height=None, width=None,
                     gradient="linear-gradient(133deg, rgba(249,249,249,0.13) 0%, rgba(8,70,131,1) 70%, rgba(222,8,44,1) 80%)"):
    return html.Div([
        html.Div([
            html.H3(title, style={
                "fontFamily": "Revue", "color": "#2D71B8",
                "fontSize": "16px", "fontWeight": "bold", "marginBottom": "10px"
            }),
            html.Div(content) if hasattr(content, "id") or isinstance(content, (html.Div, dcc.Graph))
            else html.P(content, style={"fontFamily": "Montserrat", "fontSize": "12px", "color": "#333"})
        ], style={
            "padding": "15px 20px",
            "background": "white",
            "borderRadius": "8px",
            **({"height": f"{height}px"} if height else {}),
            **({"width": f"{width}px"} if width else {}),
            "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
            "flex": "1"
        })
    ], style={
        "background": gradient,
        "padding": "2px",
        "borderRadius": "10px",
        "display": "flex",
        "flex": "1"
    })

# ——— Helper: Visualization Card ———
def create_visualization_card(title, chart_component, description=None,
                              height=350,
                              gradient="linear-gradient(133deg, rgba(249,249,249,0.13) 0%, rgba(8,70,131,1) 70%, rgba(222,8,44,1) 80%)"):
    children = [
        html.H3(title, style={
            "fontFamily": "Google Sans, sans-serif",
            "color": "#DE082C",
            "fontSize": "24px",
            "marginBottom": "10px",
            "fontWeight": "Normal",
            "marginTop": "0px" 
        })
    ]
    if description:
        children.append(html.P(description, style={
            "fontFamily":"Montserrat","fontSize":"12px","color":"#333","marginBottom":"10px"
        }))
    children.append(html.Div(chart_component, style={
        "flexGrow":"1","height":"100%","overflow":"hidden"
    }))
    return html.Div([
        html.Div(children, style={
            "width":"100%","background":"white",
            "borderRadius":"8px","boxShadow":"0 2px 5px rgba(0,0,0,0.1)",
            "padding":"10px", **({"height":f"{height}px"} if height else {})
        })
    ], style={
        "background":gradient,"padding":"2px",
        "borderRadius":"10px","display":"inline-block","width":"100%"
    })

# ——— Helper: Two‑Column Layout ———
def create_two_column_layout(left_component, right_component):
    return html.Div([
        html.Div([left_component], style={
            "flex":"1 1 60%",
            "display": "flex",
            "flexDirection": "column",
            "paddingRight": "10px"  # ✅ prevents content hugging the divider
        }),
        html.Div([right_component], style={
            "flex": "1 1 35%",
            "display": "flex",
            "flexDirection": "column",
            "paddingLeft": "10px"   # ✅ prevents crowding at the edge
        })
    ], style={
        "display": "flex",
        "flexWrap": "nowrap",           # Prevents wrapping
        "alignItems": "stretch",        # Ensures columns match height
        "gap": "20px",
        "width": "100%"
    })

# ——— Helper: Stack Cards Vertically ———
def create_stacked_cards(cards_list):
    return html.Div(cards_list, style={
        "display":"flex","flexDirection":"column","gap":"20px"
    })

# ——— MAIN: Overview Content ———
def create_overview_content():
    pie_card = create_visualization_card(
        "Total Enrollees by Level",
        pie_chart_total_enrollees,
        height=450,
    )

    # 2) Combined card for trend and interactive components
    # Create dropdowns
    chart_select = dcc.Dropdown(
        id="overview-chart-dropdown",
        options=[
            {"label":"SHS Gender Distribution",     "value":"shs"},
            {"label":"Gender Distribution by Level","value":"category"},
        ],
        value="shs", clearable=False,
        style={"fontFamily":"Google Sans, sans--serif", "fontSize":"14px","width":"300px","display":"inline-block","marginRight":"5%", "fontWeight":"Normal"}
    )
    region_select = dcc.Dropdown(
        id="overview-region-dropdown",
        options=[{"label":r,"value":r} for r in REGIONS],
        value="All Regions", clearable=False,
        style={"fontFamily":"Google Sans, sans--serif","fontSize":"14px","width":"200px","display":"inline-block", "marginBottom":"10px", "fontWeight":"Normal"}
    )
    
    # Create a combined panel with trend chart and interactive controls
    combined_panel = html.Div([
        # Trend chart section
        html.Div([
           html.H4("Enrollment Sex Distribution", style={
            "fontFamily": "Google Sans, sans-serif",
            "color": "#DE082C",
            "fontSize": "24px",
            "marginBottom": "10px",
            "fontWeight": "Normal",
            "marginTop": "0px"  # ← This line ensures no space above title
        }),
            dcc.Loading(children=[dcc.Graph(figure=enrollment_trend_by_gender, style={"height":"300px"})], type = "circle")
        ], style={"marginBottom": "30px",
                "marginTop": "0px",          # ← Removes default padding from above the card
                "paddingTop": "0px"          # ← Just in case some internal Dash default is adding padding
            }),
        
        # Interactive section
        html.Div([
            html.H4("Gender Distribution Analysis", style={
                "fontFamily":"Google Sans, sans-serif",
                "color":"#DE082C",
                "fontSize":"24px","marginBottom":"10px",
                "fontWeight":"Normal",
            }),
            html.Div([chart_select, region_select], style={"marginBottom":"10px"}),
            dcc.Loading(children=[dcc.Graph(id="overview-graph", style={"height":"300px"})], type = "circle")
        ])
    ], style={"height":"100%", "display":"flex", "flexDirection":"column"})
    
    combined_card = create_visualization_card(
        combined_panel,
        "",
        height=1025  # Match the height of the big card
    )

    # 3) Stack pie and combined card
    stacked_visualization = create_stacked_cards([pie_card, combined_card])

    # 4) Big placeholder card
    number= get_latest_total_enrollees()
    card3_title = html.H3([
    html.Span(f"{number:,} ", style={
        
        "fontSize": "70px",
        "fontWeight": "bold",
        "background": "linear-gradient(45deg, #F9F9F9, #084683, #DE082C)",  
        "WebkitBackgroundClip": "text",  
        "color": "transparent",  
    }),
    html.Span("Enrollees", style={
        "fontSize": "30px",           # Smaller size for "Enrollees"
        "fontWeight": "normal",        # Regular weight
        "color": "#084683",            # Dark gray color
        "marginLeft": "10px",          # Small spacing from the number
        "fontFamily": "Google Sans, sans--serif",  # Font style
    })
])
    
    card3_content = html.Div([
        # Trend Graph (Existing)
        dcc.Graph(
            figure=get_enrollment_trend_figure(),
            config={'displayModeBar': False},
            style={"height": "500px", "width": "800px"}
        ),
        # Dropdown to select education level for heatmap
        dcc.Dropdown(
            id='level-dropdown',  # Dropdown to select education level
            options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'Kindergarten', 'value': 'Kindergarten'},
                {'label': 'ELEM', 'value': 'ELEM'},
                {'label': 'JHS', 'value': 'JHS'},
                {'label': 'SHS', 'value': 'SHS'},
                {'label': 'Total NG', 'value': 'Total NG'}, # to count how many total NG students there are per region
                {'label': 'Subtotal', 'value': 'Subtotal'}
            ],
            value='All',
            clearable=False,
            style={'width': '300px', 'marginBottom': '20px'}
        ),
    
            # Heatmap (New addition)
        dcc.Graph(
            id='region-level-heatmap',
            figure=get_region_heatmap_figure(selected_level='All'),  # Placeholder for heatmap
            config={'displayModeBar': False},
            style={"height": "400px", "width": "800px"}
        )
    ], style={'marginTop': '20px'})

    big_card = create_info_card(card3_title, card3_content, height=1500)

    main_section = create_two_column_layout(big_card, stacked_visualization)

    # 5) Map card
    map_card = create_visualization_card(
        "Regional Total Enrollment",
        dcc.Graph(figure=phmap()),
        "This heatmap highlights total enrollment per region across the Philippines.",
        height=880
    )

    # 6) Compose and return
    return html.Div([
        html.Div(main_section, style={"marginBottom": "30px"}), map_card],
        style={"maxWidth":"1400px","margin":"0 auto","padding":"10px"}
    )