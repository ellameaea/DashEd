import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load your dataset
combined_population_df = pd.read_csv('CSV Files/combined_population.csv')

# Define available grade levels
grade_levels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"])

# Define the layout
app.layout = html.Div([
    html.H2("Student Population Heatmap by Grade", className="text-center mt-4"),

    html.Div([
        dcc.Dropdown(
            id='grade-dropdown',
            options=[{'label': grade, 'value': grade} for grade in grade_levels],
            value='G11',
            clearable=False,
            style={'width': '50%'}
        ),
    ], className="d-flex justify-content-center mt-3"),

    html.Div([
        dcc.Graph(id='heatmap', style={'height': '800px'})
    ], className="mt-4 px-4"),

    html.H4("Total Enrollees per Grade Level", className="text-center mt-5"),

    html.Div([
        dcc.Graph(id='bar-chart')
    ], className="mt-3 px-4")
])

# Define the heatmap callback
@app.callback(
    Output('heatmap', 'figure'),
    Input('grade-dropdown', 'value')
)
def update_heatmap(selected_grade):
    grade_columns = [col for col in combined_population_df.columns if f'{selected_grade} ' in col and 'Total' in col]

    if not grade_columns:
        return px.imshow([[0]], labels=dict(x="Strand", y="Region", color="Students"),
                         title=f"No data available for Grade {selected_grade}")

    melted_df = combined_population_df.melt(
        id_vars=['Region'],
        value_vars=grade_columns,
        var_name="Strand",
        value_name="Total Students"
    )
    melted_df['Strand'] = melted_df['Strand'].str.extract(r'(\b[A-Za-z]+\b)')
    aggregated_df = melted_df.groupby(['Region', 'Strand'], as_index=False).sum()
    heatmap_data = aggregated_df.pivot(index='Region', columns='Strand', values='Total Students').fillna(0)

    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Strand", y="Region", color="Students"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale="viridis",
        text_auto=True,
        aspect="auto"
    )

    fig.update_layout(
        title=f"Student Population by Region and Strand (Grade {selected_grade})",
        xaxis_title="Strand",
        yaxis_title="Region",
        autosize=False,
        width=1000,
        height=800,
        margin=dict(l=100, r=50, t=100, b=100),
        font=dict(size=12)
    )
    fig.update_xaxes(tickangle=45)

    return fig

# Callback for bar chart of total enrollees per grade
@app.callback(
    Output('bar-chart', 'figure'),
    Input('grade-dropdown', 'value')
)
def update_bar_chart(selected_grade):
    # Define mapping of grade levels to corresponding columns
    grade_column_map = {
        'K': ['K Total'],
        'G1': ['G1 Total'],
        'G2': ['G2 Total'],
        'G3': ['G3 Total'],
        'G4': ['G4 Total'],
        'G5': ['G5 Total'],
        'G6': ['G6 Total'],
        'G7': ['G7 Total'],
        'G8': ['G8 Total'],
        'G9': ['G9 Total'],
        'G10': ['G10 Total'],
        'G11': [col for col in combined_population_df.columns if col.startswith('G11')],
        'G12': [col for col in combined_population_df.columns if col.startswith('G12')],
    }

    # Sum population for each grade level
    grade_totals = []
    for grade in grade_levels:
        columns = grade_column_map.get(grade, [])
        total = combined_population_df[columns].sum().sum() if columns else 0
        grade_totals.append(total)

    fig = px.bar(
        x=grade_levels,
        y=grade_totals,
        labels={'x': 'Grade Level', 'y': 'Total Enrollees'},
        title='Total Enrollees per Grade Level',
        #text=grade_totals,
        color=grade_levels,
        height=400,
        width=600,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(
        
        width=0.9, 
        marker_color='skyblue')
    
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)

    return fig


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
