import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px

# Load dataset
df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

# Melt to long format
melted_df = df.melt(id_vars=["Region"], var_name="Descriptor", value_name="Enrollees")

# Extract SHS Grade, Strand, Gender
extracted = melted_df['Descriptor'].str.extract(r'^(G11|G12)\s*([A-Za-z\s]*)\s+(Male|Female)$')
melted_df['Grade Level'] = extracted[0]
melted_df['Strand'] = extracted[1].str.strip()
melted_df['Gender'] = extracted[2]

# Drop invalid rows
melted_df.dropna(subset=['Grade Level', 'Strand', 'Gender'], inplace=True)

# Convert Enrollees to numeric
melted_df['Enrollees'] = pd.to_numeric(melted_df['Enrollees'], errors='coerce').fillna(0)

# Group data across all SHS (G11 and G12)
grouped = melted_df.groupby(['Strand', 'Gender'], as_index=False)['Enrollees'].sum()

# Calculate percentages for 100% stacked chart
total_per_strand = grouped.groupby('Strand')['Enrollees'].transform('sum')
grouped['Percentage'] = (grouped['Enrollees'] / total_per_strand) * 100

# Add combined label
grouped['Label'] = grouped.apply(
    lambda row: f"{int(row['Enrollees']):,} ({row['Percentage']:.1f}%)", axis=1
)

# Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
])

# Layout
app.layout = html.Div([
    html.H2("Senior High School Enrollee Gender Distribution by Strand", className="text-center mt-4"),
    html.Div([
        dcc.Graph(id='shs-bar-chart') # Bar chart for SHS enrollee distribution
    ], className="mt-4 px-4")
])

# Callback (triggered once on load)
@app.callback(
    Output('shs-bar-chart', 'figure'), # Output for the SHS bar chart
    Input('shs-bar-chart', 'id') # Dummy input to trigger the callback
)

# Callback function to update the SHS bar chart
def display_shs_bar_chart(_):
    total_all = int(grouped['Enrollees'].sum()) # Total enrollees for all regions
    
    # formats each bar for chart
    fig = px.bar(
        grouped, # Data for the bar chart
        x='Percentage', # X-axis: percentage of enrollees
        y='Strand', # Y-axis: strand
        color='Gender', # Color by command
        orientation='h', # Horizontal orientation
        barmode='stack', # Stacked bar mode
        text='Label', # Text on bars
        color_discrete_map={'Male': '#1f77b4', 'Female': '#e377c2'}, # Color mapping
        title=f"Gender Distribution in SHS (All Regions)<br><sub>Total Enrollees for SHS: {total_all:,}</sub>", # Title
        labels={'Percentage': 'Percentage of Students'} # Label for x-axis
    )

    # Update layout for entire chart
    fig.update_layout(
        xaxis=dict(title='Percentage', # X-axis title
                   ticksuffix='%', # Suffix for x-axis ticks (can remove for cleanliness)
                   range=[0, 100]), # Range for x-axis
        yaxis_title='Strand', # Y-axis title
        height=700, # Height of the chart
        legend_title='Gender', # Legend title
        margin=dict(l=100, r=40, t=80, b=60) # Margin settings
    )
    fig.update_traces(textposition='inside', # Position text inside bars
                      insidetextanchor='middle') # Position labels inside bars

    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
