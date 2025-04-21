import pandas as pd
import numpy as np
from dash import dcc
import plotly.graph_objects as go

def get_region_heatmap_figure(selected_level='All'):
    # Load the dataset
    file_path = "CSV Files/CLEANED_SY2023_Enrollment.csv"
    df = pd.read_csv(file_path)

    # Define combined levels
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

    enrollment_columns = [col for cols in combined_levels.values() for col in cols]
    region_level_totals = df.groupby('Region').agg({col: 'sum' for col in enrollment_columns}).reset_index()

    region_heatmap_data = pd.DataFrame()
    region_heatmap_data['Region'] = region_level_totals['Region']

    for level, columns in combined_levels.items():
        region_heatmap_data[level] = region_level_totals[columns].sum(axis=1)

    region_heatmap_data['Subtotal'] = region_heatmap_data[['Kindergarten', 'ELEM', 'JHS', 'SHS']].sum(axis=1)

    grand_totals = region_heatmap_data[['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal']].sum()
    grand_total_row = pd.DataFrame([['Grand Total'] + grand_totals.tolist()], columns=region_heatmap_data.columns)

    region_heatmap_data = pd.concat([region_heatmap_data, grand_total_row], ignore_index=True)
    region_heatmap_data = region_heatmap_data.iloc[::-1].reset_index(drop=True)

    if selected_level == 'All':
        display_data = region_heatmap_data.set_index('Region').loc[:, ['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal']]
        x_axis = ['Kindergarten', 'ELEM', 'JHS', 'SHS', 'Subtotal']
    else:
        display_data = region_heatmap_data.set_index('Region').loc[:, [selected_level]]
        x_axis = [selected_level]

    y_axis = display_data.index.tolist()

    # Exclude Grand Total for min/max logic
    filtered = display_data.drop(index='Grand Total', errors='ignore')

    # Determine min/max rows
    max_idx = filtered[selected_level].idxmax() if selected_level != 'All' else filtered['Subtotal'].idxmax()
    min_idx = filtered[selected_level].idxmin() if selected_level != 'All' else filtered['Subtotal'].idxmin()

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
    value_map = {-1: 0.0, 0: 0.33, 1: 0.66, 2: 1.0}
    normalized_colors = np.vectorize(value_map.get)(colors)

    # Custom colorscale
    custom_colorscale = [
        [0.0, '#DE082C'],    # Min - red
        [0.33, '#F0F8FF'],   # Normal - light gray
        [0.66, '#F2EC1A'],   # Max - green
        [1.0, '#084683']     # Grand Total - blue
    ]

    fig = go.Figure(data=go.Heatmap(
        z=normalized_colors,
        x=x_axis,
        y=y_axis,
        text=z,
        texttemplate="%{text}",
        colorscale=custom_colorscale,
        zmin=0,
        zmax=1,
        showscale=False,
        xgap=1,  # Horizontal grid space
        ygap=1   # Vertical grid space
    ))

    fig.update_layout(
        title=f"Enrollment Heatmap by Region - {selected_level if selected_level != 'All' else 'All Levels'}",
        xaxis=dict(title="Education Level", side="top"),
        yaxis_title="Region",
        plot_bgcolor='#C9E1E6',
        height=800,
        width=800,
        margin=dict(l=100, r=50, t=100, b=100),
        font=dict(size=10)
    )

    return fig
