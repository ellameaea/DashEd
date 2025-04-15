import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load dataset
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

# Create base bar chart
fig = px.bar(
    grouped,
    x='Region',
    y='size',
    color='Modified COC',
    category_orders={'Modified COC': coc_ranking},  # Dynamically ordered by most prominent
    title="Number of Schools by Region and Modified COC",
    labels={'size': 'Number of Schools', 'Modified COC': 'Modified COC'}
)

# Add stacked bar settings
fig.update_layout(
    xaxis_title='Region',
    yaxis_title='Number of Schools',
    height=700,
    barmode='stack',
    xaxis={'categoryorder': 'total descending'}
)

# Add total annotations
for i, row in total_schools_per_region.iterrows():
    fig.add_annotation(
        x=row['Region'],
        y=row['size'],
        text=str(row['size']),
        showarrow=False,
        font=dict(size=12, color="black"),
        xanchor='center',
        yanchor='bottom'
    )

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
])

# Layout
app.layout = html.Div([
    html.H2("Number of Schools by Region and Modified COC", className="text-center mt-4"),

    html.Div([
        dcc.Graph(id='stacked-bar-chart', figure=fig)
    ], className="mt-4 px-4"),

    html.Div([
        html.H5("Ranking of Modified COCs (Most Prominent to Least):", className="text-center mt-4"),
        html.Ol(
            children=[html.Li(coc) for coc in coc_ranking],
            style={'textAlign': 'center', 'listStylePosition': 'inside'}
        )
    ], className="mt-4 px-4")
])

# Run the app
if __name__ == '__main__':
    app.run(port=8050, debug=True)
