import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from plotly import graph_objects as go
import numpy as np

# use this code instead for the overview heatmap as shown from figma

# Load the dataset (change later to let user select dataset!!)
file_path = "CSV Files/CLEANED_SY2023_Enrollment.csv"  # Update this path if necessary
df = pd.read_csv(file_path)

# Dictionary for each grade level
combined_levels = {
    'Kindergarten': ['K Male', 'K Female'],
    'ELEM': [
        'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female', 'G3 Male', 'G3 Female',
        'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female', 'G6 Male', 'G6 Female',
        'Elem NG Male', 'Elem NG Female'
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

# Ensure numeric values for enrollment columns
enrollment_columns = [col for cols in combined_levels.values() for col in cols]
region_level_totals = df.groupby('Region').agg({col: 'sum' for col in enrollment_columns}).reset_index()

# Create a new DataFrame for the heatmap
region_heatmap_data = pd.DataFrame()
region_heatmap_data['Region'] = region_level_totals['Region']

# Calculate total enrollees for each region
for level, columns in combined_levels.items():
    region_heatmap_data[level] = region_level_totals[columns].sum(axis=1)

# Calculate subtotal for each region
region_heatmap_data['Subtotal'] = region_heatmap_data[['Kindergarten', 'ELEM', 'JHS', 'SHS']].sum(axis=1)

# Calculate grand total for each region
grand_totals = region_heatmap_data[['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal']].sum()
grand_total_row = pd.DataFrame([['Grand Total'] + grand_totals.tolist()], columns=region_heatmap_data.columns)

# Append grand total row to the DataFrame
region_heatmap_data = pd.concat([region_heatmap_data, grand_total_row], ignore_index=True)
region_heatmap_data = region_heatmap_data.iloc[::-1].reset_index(drop=True)

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Label("Select Education Level:"), #Label for Dropdown
        dcc.Dropdown(
            id='level-dropdown', # Dropdown for selecting education level
            options=[
                {'label': 'All', 'value': 'All'}, # Displays all columns
                {'label': 'Kindergarten', 'value': 'Kindergarten'}, # display kindergarten column
                {'label': 'ELEM', 'value': 'ELEM'}, # display ELEM column
                {'label': 'JHS', 'value': 'JHS'}, # display JHS column
                {'label': 'SHS', 'value': 'SHS'}, # display SHS column
                {'label': 'Subtotal', 'value': 'Subtotal'} # display subtotal column
            ],
            value='All',
            clearable=False, # Prevents clearing of selection
            style={'width': '300px'} # Styles the dropdown
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}), # Centered and spaced

    dcc.Graph(id='region-level-heatmap') # Graph for displaying heatmap
])

@app.callback(
    Output('region-level-heatmap', 'figure'), # Output for the heatmap
    Input('level-dropdown', 'value') # Input for the selected education level
)

# Callback function to update the heatmap based on selected education level
def update_heatmap(selected_level):
    if selected_level == 'All': # If 'All' is selected, show all levels
        display_data = region_heatmap_data.set_index('Region').loc[:, ['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal']]
        x_axis = ['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal']
    else:
        display_data = region_heatmap_data.set_index('Region').loc[:, [selected_level]]
        x_axis = [selected_level]

    # Get the y-axis labels (regions)
    y_axis = display_data.index.tolist()

    # Exclude Grand Total for min/max logic
    filtered = display_data.drop(index='Grand Total', errors='ignore')

    # Determine min/max rows
    max_idx = filtered[selected_level].idxmax() if selected_level != 'All' else filtered['Subtotal'].idxmax()
    min_idx = filtered[selected_level].idxmin() if selected_level != 'All' else filtered['Subtotal'].idxmin()

    # Get the values for the heatmap
    z = display_data.values

    # Create mask for color mapping
    colors = np.full_like(z, fill_value=0, dtype=int)  # Default = Normal (0)

    for i, region in enumerate(y_axis):
        for j, level in enumerate(x_axis):
            if region == max_idx:
                colors[i][j] = 1  # Max
            elif region == min_idx:
                colors[i][j] = -1  # Min
            elif region == 'Grand Total':
                colors[i][j] = 2  # Grand Total

    # Normalize to [0, 1] for Plotly
    value_map = {-1: 0.0, # Min
                 0: 0.33, # Normal
                 1: 0.66, # Max
                 2: 1.0} # Grand Total
    
    # Map colors to normalized values
    normalized_colors = np.vectorize(value_map.get)(colors)     

    # Custom colorscale
    custom_colorscale = [
        [0.0, '#DE082C'],  
        [0.33, '#F0F8FF'],  
        [0.66, '#F2EC1A'],  
        [1.0, '#084683']     
    ]

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=normalized_colors, # Normalized values for color mapping
        x=x_axis, # X-axis labels (education levels)
        y=y_axis, # Y-axis labels (regions)
        text=z, # Original values for display
        texttemplate="%{text}", # Display original values
        colorscale=custom_colorscale, # Custom colorscale
        zmin=0, # Min value for color mapping
        zmax=1, # Max value for color mapping
        showscale=False, # Hide color scale
        xgap=1,  # Horizontal grid space
        ygap=1   # Vertical grid space
    ))

    # Add annotations for the values
    fig.update_layout(
        title=f"Enrollment Heatmap by Region - {selected_level if selected_level != 'All' else 'All Levels'}",
        xaxis=dict(title="Education Level", side="top"), # X-axis title
        yaxis_title="Region", # Y-axis title
        plot_bgcolor='#C9E1E6',     # Optional: makes grid gaps visible
        height=800, # Height of the heatmap
        width=800, # Width of the heatmap
        margin=dict(l=100, r=50, t=100, b=100), # Margin settings
        font=dict(size=10) # Font size for the text
    )

    return fig

if __name__ == '__main__':
    app.run(port=8051, debug=True)
