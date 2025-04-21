# Data_Visualization/overview_layout.py

import pandas as pd
from dash import html, dcc
from Data_Visualization.Overview_output import pie_chart_total_enrollees
from Data_Visualization.phmap import phmap
from Data_Visualization.Enrollee_Gender_Analysis.Totals_Gender_bar import gender_bar
from Data_Visualization.Enrollee_Gender_Analysis.Totals_SHS_bar import gender_shs_bar
from Data_Visualization.Timelines_Analysis.Total_Male_vs_Female_Time import enrollment_trend_by_gender


# ——— Data & Region List ———
DF = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")
REGIONS = ["All Regions"] + sorted(DF["Region"].dropna().unique().tolist())

# ——— Helper: Info Card ———
def create_info_card(title, content, height=300, width=None,
                     gradient="linear-gradient(133deg, rgba(249,249,249,0.13) 0%, rgba(8,70,131,1) 70%, rgba(222,8,44,1) 80%)"):
    return html.Div([
        html.Div([
            html.H3(title, style={
                "fontFamily":"Revue","color":"#2D71B8",
                "fontSize":"16px","fontWeight":"bold","marginBottom":"10px"
            }),
            # if content is a string, renders <p>; if it's a component, renders it directly
            html.Div(content) if hasattr(content, "id") or isinstance(content, (html.Div, dcc.Graph)) 
                             else html.P(content, style={"fontFamily":"Montserrat","fontSize":"12px","color":"#333"})
        ], style={
            "padding":"15px 20px","background":"white",
            "borderRadius":"8px","height":f"{height}px",
            **({"width":f"{width}px"} if width else {}),
            "boxShadow":"0 2px 5px rgba(0,0,0,0.1)"
        })
    ], style={
        "background":gradient,"padding":"2px",
        "borderRadius":"10px","display":"inline-block"
    })

# ——— Helper: Visualization Card ———
def create_visualization_card(title, chart_component, description=None,
                              height=350,
                              gradient="linear-gradient(133deg, rgba(249,249,249,0.13) 0%, rgba(8,70,131,1) 70%, rgba(222,8,44,1) 80%)"):
    children = [
        html.H3(title, style={
            "fontFamily":"Revue","color":"#2D71B8",
            "fontSize":"16px","fontWeight":"bold","marginBottom":"10px"
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
            "flex":"1 1 60%","minWidth":"300px",
            "display":"flex","flexDirection":"column"
        }),
        html.Div([right_component], style={
            "flex":"1 1 35%","minWidth":"250px",
            "display":"flex","flexDirection":"column"
        })
    ], style={
        "display":"flex","flexWrap":"wrap",
        "justifyContent":"space-between","alignItems":"stretch",
        "gap":"20px","marginBottom":"20px"
    })

# ——— Helper: Stack Cards Vertically ———
def create_stacked_cards(cards_list):
    return html.Div(cards_list, style={
        "display":"flex","flexDirection":"column","gap":"20px"
    })

# ——— MAIN: Overview Content ———
def create_overview_content():
    # 1) Pie card
    pie_card = create_visualization_card(
        "Total Enrollees by Level",
        pie_chart_total_enrollees,
        height=450
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
        style={"fontFamily":"Monserrat","width":"45%","display":"inline-block","marginRight":"5%"}
    )
    region_select = dcc.Dropdown(
        id="overview-region-dropdown",
        options=[{"label":r,"value":r} for r in REGIONS],
        value="All Regions", clearable=False,
        style={"fontFamily":"Monserrat","width":"45%","display":"inline-block"}
    )
    
    # Create a combined panel with trend chart and interactive controls
    combined_panel = html.Div([
        # Trend chart section
        html.Div([
            html.H4("Enrollment Sex Distribution", style={
                "fontFamily":"Revue","color":"#2D71B8",
                "fontSize":"14px","fontWeight":"bold","marginBottom":"5px"
            }),
            dcc.Graph(figure=enrollment_trend_by_gender, style={"height":"300px"})
        ], style={"marginBottom":"20px"}),
        
        # Interactive section
        html.Div([
            html.H4("Gender Distribution Analysis", style={
                "fontFamily":"Revue","color":"#2D71B8",
                "fontSize":"14px","marginBottom":"5px", "marginTop":"10px"
            }),
            html.Div([chart_select, region_select], style={"marginBottom":"10px"}),
            dcc.Graph(id="overview-graph", style={"height":"260px"})
        ])
    ], style={"height":"100%", "display":"flex", "flexDirection":"column"})
    
    combined_card = create_visualization_card(
        combined_panel,
        "",
        height=840  # Match the height of the big card
    )

    # 3) Stack pie and combined card
    stacked_visualization = create_stacked_cards([pie_card, combined_card])

    # 4) Big placeholder card
    card3_content = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    )
    big_card = create_info_card("Title for Data Viz 3", card3_content, height=820)

    main_section = create_two_column_layout(big_card, stacked_visualization)

    # 5) Map card
    map_card = create_visualization_card(
        "Regional Total Enrollment",
        dcc.Graph(figure=phmap()),
        "This heatmap highlights total enrollment per region across the Philippines.",
        height=880
    )

    # 6) Compose and return
    return html.Div(
        [main_section, map_card],
        style={"maxWidth":"1400px","margin":"0 auto","padding":"10px"}
    )