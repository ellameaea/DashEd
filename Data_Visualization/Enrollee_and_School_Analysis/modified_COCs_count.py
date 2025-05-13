import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

# Load the dataset (change later to let user select dataset!!)
df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

# Group data by Region and Modified COC to count the number of schools
grouped = df.groupby(['Region', 'Modified COC'], as_index=False).size()

# Calculate total counts for each Modified COC
coc_totals = grouped.groupby('Modified COC')['size'].sum().sort_values(ascending=False)
coc_ranking = coc_totals.index.tolist()  # most prominent to least

# Apply the sorted order as category order
df['Modified COC'] = pd.Categorical(df['Modified COC'], categories=coc_ranking, ordered=True)

# Total schools per region (for annotations)
total_schools_per_region = grouped.groupby('Region')['size'].sum().reset_index()

# Assign custom colors: first one = #636efa, rest = lighter shades
#primary_color = '#636efa'
#light_colors = [
    #'#aab6ff', '#c5ccff', '#dbe0ff', '#e8ebff', '#f0f2ff', '#f5f6ff', '#fafbff'
#]
#custom_colors = [primary_color] + light_colors[:len(coc_ranking) - 1]

custom_palette = ['#084683', '#DE082C', '#F2EC1A', '#D9D9D9', '#0174DF']
custom_colors = (custom_palette * ((len(coc_ranking) // len(custom_palette)) + 1))[:len(coc_ranking)]

# Create stacked bar chart manually with go.Figure for more control
fig = go.Figure()

# Add bars for each Modified COC
for i, coc in enumerate(coc_ranking):
    data = grouped[grouped['Modified COC'] == coc] # Filter data for the current COC
    fig.add_trace(go.Bar(
        x=data['Region'], # Computes X-axis values
        y=data['size'], # Computes Y-axis values
        name=coc, # Name of the bar
        marker=dict(
            color=custom_colors[i], # Color for the bar
            line=dict(color='gray', width=1) # Border color
        ),
        # Text on bars
        hovertemplate='<b>Modified COC:</b> %{customdata[0]}<br><b>Region:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>',
        customdata=[[coc] for _ in range(len(data))] # Custom data for hover
    ))

# This finds total schools per region
for i, row in total_schools_per_region.iterrows():
    fig.add_annotation(
        x=row['Region'], # X-axis value
        y=row['size'], # Y-axis value
        text=str(row['size']), # Text to show
        showarrow=False, # No arrow
        font=dict(size=12, color="black"), # Font size and color
        xanchor='center', # Center the text
        yanchor='bottom' # Anchor the text to the bottom
    )

# organize the layout of the chart itself with this
fig.update_layout(
    title="Number of Schools by Region and Modified COC", # Title of the chart
    xaxis_title='Region', # X-axis title
    yaxis_title='Number of Schools', # Y-axis title
    height=700, # Height of the chart
    barmode='stack', # Stacked bar mode
    xaxis=dict(categoryorder='total descending'), # Order x-axis by total
    legend_title='Modified COC' # Legend title
)

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
])

# Layout
app.layout = html.Div([
    # to edit title of chart!
    html.H2("Number of Schools by Region and Modified COC", className="text-center mt-4"),

    # Stacked bar chart
    html.Div([
        dcc.Graph(id='stacked-bar-chart', figure=fig) # Chart itself
    ], className="mt-4 px-4"), 

    # Ranking of Modified COCs as a list
    html.Div([
        html.H5("Ranking of Modified COCs (Most Prominent to Least):", className="text-center mt-4"), # Title
        html.Ol(
            children=[html.Li(coc) for coc in coc_ranking], # List of COCs
            style={'textAlign': 'center', 'listStylePosition': 'inside'} # Center the list
        )
    ], className="mt-4 px-4")
])

# Run the app
if __name__ == '__main__':
    app.run(port=8050, debug=True)
