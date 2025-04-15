import pandas as pd
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv('CSV Files/CLEANED_SY2023_Enrollment.csv')  # Replace with your file path

# List of columns to sum for total enrollees
enrollee_columns = [
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

# Calculate total enrollees per row
df['Total Enrollees'] = df[enrollee_columns].sum(axis=1)

# Group by region and aggregate
region_summary = df.groupby('Region').agg({
    'Total Enrollees': 'sum',
    'BEIS School ID': 'nunique'  # Count unique school IDs for number of schools
}).reset_index()

# Rename the BEIS School ID column
region_summary.rename(columns={'BEIS School ID': 'Number of Schools'}, inplace=True)

# Sort by Total Enrollees in descending order
region_summary = region_summary.sort_values(by='Total Enrollees', ascending=False)

# Calculate the "Enrollees per School" ratio for each region
region_summary['Enrollees per School'] =  (region_summary['Number of Schools'] / region_summary['Total Enrollees'])*100

# Create grouped bar chart with the ratio metric
fig = go.Figure(data=[
    #go.Bar(name='Number of Schools', x=region_summary['Region'],y=region_summary['Number of Schools'], marker_color='steelblue', text=region_summary['Number of Schools'],textposition='auto'),
    #go.Bar(name='Total Enrollees', x=region_summary['Region'], y=region_summary['Total Enrollees'], marker_color='indianred', text=region_summary['Total Enrollees'], textposition='auto'),
    go.Bar(
        name='Enrollees per School',
        x=region_summary['Region'],
        y=region_summary['Enrollees per School'],
        marker_color='green',
        text=region_summary['Enrollees per School'].round(2),  
        textposition='auto'
    )
])

# Update layout
fig.update_layout(
    title='Measures of School Crowding per Region',
    xaxis_title='Region',
    yaxis_title='Percentage (%)',
    barmode='group',
    legend=dict(title='Metric'),
    xaxis_tickangle=-45
)

# Show the plot
fig.show()