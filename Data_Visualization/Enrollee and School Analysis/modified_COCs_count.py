import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

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

# Assign custom colors: first one = #636efa, rest = lighter shades
primary_color = '#636efa'
light_colors = [
    '#aab6ff', '#c5ccff', '#dbe0ff', '#e8ebff', '#f0f2ff', '#f5f6ff', '#fafbff'
]
custom_colors = [primary_color] + light_colors[:len(coc_ranking) - 1]

# Create stacked bar chart manually with go.Figure for more control
fig = go.Figure()


for i, coc in enumerate(coc_ranking):
    data = grouped[grouped['Modified COC'] == coc]
    fig.add_trace(go.Bar(
        x=data['Region'],
        y=data['size'],
        name=coc,
        marker=dict(
            color=custom_colors[i],
            line=dict(color='gray', width=1)
        ),
        hovertemplate='<b>Modified COC:</b> %{customdata[0]}<br><b>Region:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>',
        customdata=[[coc] for _ in range(len(data))]
    ))

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

# Update layout
fig.update_layout(
    title="Number of Schools by Region and Modified COC",
    xaxis_title='Region',
    yaxis_title='Number of Schools',
    height=700,
    barmode='stack',
    xaxis=dict(categoryorder='total descending'),
    legend_title='Modified COC'
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
