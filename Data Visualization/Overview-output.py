import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
import plotly.express as px
import json
import os

# Load the dataset (change later to let user select dataset!!)
file_path = "CSV Files/CLEANED_SY2023_Enrollment.csv"  # Update this path if necessary
df = pd.read_csv(file_path)

# Columns containing enrollment data
enrollment_columns = [
    'K Male', 'K Female', 'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
    'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
    'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female', 'G7 Male', 'G7 Female',
    'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female',
    'JHS NG Male', 'JHS NG Female', 'G11 ACAD ABM Male', 'G11 ACAD ABM Female',
    'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Male', 'G11 ACAD STEM Female',
    'G11 ACAD GAS Male', 'G11 ACAD GAS Female', 'G11 ACAD PBM Male', 'G11 ACAD PBM Female',
    'G11 TVL Male', 'G11 TVL Female', 'G11 SPORTS Male', 'G11 SPORTS Female',
    'G11 ARTS Male', 'G11 ARTS Female', 'G12 ACAD ABM Male', 'G12 ACAD ABM Female',
    'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female', 'G12 ACAD STEM Male', 'G12 ACAD STEM Female',
    'G12 ACAD GAS Male', 'G12 ACAD GAS Female', 'G12 ACAD PBM Male', 'G12 ACAD PBM Female',
    'G12 TVL Male', 'G12 TVL Female', 'G12 SPORTS Male', 'G12 SPORTS Female',
    'G12 ARTS Male', 'G12 ARTS Female'
]

# Ensure numeric values for enrollment columns
df[enrollment_columns] = df[enrollment_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Calculate total enrollees
total_enrollees = df[enrollment_columns].sum().sum()

# Calculate total male and female enrollees
male_columns = [col for col in enrollment_columns if 'Male' in col]
female_columns = [col for col in enrollment_columns if 'Female' in col]

total_male_enrollees = df[male_columns].sum().sum()
total_female_enrollees = df[female_columns].sum().sum()

# Count total number of schools
total_schools = df.shape[0]

# Count DepEd Managed schools
deped_managed_schools = df[df['Sector'] == 'Public']['Sector'].count()

# Dictionary for combined levels
combined_levels = {
    'Kindergarten': [
        'K Male', 'K Female'
    ],
    'ELEM': [
        'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
        'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
        'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female'
    ],
    'JHS': [
        'G7 Male', 'G7 Female', 'G8 Male', 'G8 Female', 'G9 Male', 'G9 Female',
        'G10 Male', 'G10 Female', 'JHS NG Male', 'JHS NG Female'
    ],
    'SHS': [
        'G11 ACAD ABM Male', 'G11 ACAD ABM Female', 'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female',
        'G11 ACAD STEM Male', 'G11 ACAD STEM Female', 'G11 ACAD GAS Male', 'G11 ACAD GAS Female',
        'G11 ACAD PBM Male', 'G11 ACAD PBM Female', 'G11 TVL Male', 'G11 TVL Female',
        'G11 SPORTS Male', 'G11 SPORTS Female', 'G11 ARTS Male', 'G11 ARTS Female',
        'G12 ACAD ABM Male', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female',
        'G12 ACAD STEM Male', 'G12 ACAD STEM Female', 'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
        'G12 ACAD PBM Male', 'G12 ACAD PBM Female', 'G12 TVL Male', 'G12 TVL Female',
        'G12 SPORTS Male', 'G12 SPORTS Female', 'G12 ARTS Male', 'G12 ARTS Female'
    ]
}

# Calculate total enrollees for each combined level
combined_totals = {level: df[columns].sum().sum() for level, columns in combined_levels.items()}

# Calculate total enrollees per region
region_enrollment = df.groupby('Region')[enrollment_columns].sum().sum(axis=1).reset_index()
region_enrollment.columns = ['Region', 'Total_Enrollees']

# CODE FOR HEATMAP!! starts at line 82 and ends in line 128 remove as needed
# use Overview-heatmap.py for the heatmap code

# Aggregate total per region by level
region_level_totals = df.groupby('Region').agg({
    **{col: 'sum' for col in enrollment_columns}
}).reset_index()

# Add level-based totals per region
region_heatmap_data = pd.DataFrame()
region_heatmap_data['Region'] = region_level_totals['Region']

# Calculate per-level totals per region
for level, columns in combined_levels.items():
    region_heatmap_data[level] = region_level_totals[columns].sum(axis=1)

# Subtotal per region
region_heatmap_data['Subtotal'] = region_heatmap_data[
    ['Kindergarten', 'ELEM', 'JHS', 'SHS']
].sum(axis=1)

# Add Grand Total Row
grand_totals = region_heatmap_data[['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal']].sum()
grand_total_row = pd.DataFrame([['Grand Total'] + grand_totals.tolist()], columns=region_heatmap_data.columns)
region_heatmap_data = pd.concat([region_heatmap_data, grand_total_row], ignore_index=True)

# Create heatmap figure
heatmap_fig = px.imshow(
    region_heatmap_data.set_index('Region'),
    labels=dict(x="Level", y="Region", color="Enrollees"),
    x=['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal'],
    y=region_heatmap_data['Region'],
    color_continuous_scale="blues",
    text_auto=True,
    aspect="auto"
)

heatmap_fig.update_layout(
    title="Enrollment Heatmap by Region and Level (with Totals)",
    xaxis=dict(
        title="Education Level",
        side="top"  # Place x-axis labels at the top
    ),
    yaxis_title="Region",
    height=800,
    margin=dict(l=100, r=50, t=100, b=100),
    font=dict(size=12)
)

# Display the results
print("===== Enrollment Summary =====")
print(f"Total Enrollees (K to G12, including strands): {int(total_enrollees):,}")
print(f"Total Male Enrollees: {int(total_male_enrollees):,}")
print(f"Total Female Enrollees: {int(total_female_enrollees):,}")
print(f"Total Number of Schools: {total_schools:,}")
print(f"Number of DepEd Managed Schools: {deped_managed_schools:,}")

# Create the Dash app
app = Dash(__name__)

# Layout for the Dash app
app.layout = html.Div([
    html.H1("Enrollment Summary", style={'textAlign': 'center'}),
    
    # Single horizontal bar graph comparing Male vs Female Enrollees
    dcc.Graph(
        id='male-vs-female-bar', # ID for the graph
        figure=go.Figure(
            data=[
                go.Bar(
                    x=[total_male_enrollees, total_female_enrollees], # X-axis values (total male/female enrollees)
                    y=['Male Enrollees', 'Female Enrollees'], # Y-axis labels
                    orientation='h', # Horizontal orientation
                    marker=dict(color=['blue', 'pink']) # Color for bars
                )
            ],
            layout=go.Layout(
                title="Male vs Female Enrollees",
                xaxis=dict(title="Number of Enrollees"), # X-axis title
                yaxis=dict(title=""), # Y-axis title
                height=400 # Height of the graph
            )
        )
    ),
    
    # Pie chart for total enrollees by combined levels
    dcc.Graph(
        id='combined-levels-pie',
        figure=go.Figure(
            data=[
                go.Pie(
                    labels=list(combined_totals.keys()), # Labels for pie chart
                    values=list(combined_totals.values()), # Values for pie chart
                    hole=0.5, # Hole size for donut chart
                    textfont=dict(size=10) # Font size for text
                    #textinfo='none' # removed for now to show percentage of grade levels
                )
            ],
            layout=go.Layout(
                title="Total Enrollees by Level (ELEM, JHS, SHS)", # Title of the pie chart
                height=400 # Height of the graph
            )
        )
    ),

    dcc.Graph(
        id='region-level-heatmap',
        figure=heatmap_fig
    )

])

# Run the Dash app
if __name__ == '__main__':
    app.run(port=8051, debug=True)
