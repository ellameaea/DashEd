import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("CSV Files/CLEANED_SY2023_Enrollment.csv")

# Melt the DataFrame
melted_df = df.melt(id_vars=["Region"], var_name="Descriptor", value_name="Enrollees")

combined_levels = {
    'K': ['K Male', 'K Female'],
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

# Invert the combined_levels dict
descriptor_to_category = {
    descriptor: category
    for category, descriptors in combined_levels.items()
    for descriptor in descriptors
}

# Extract Gender
melted_df['Gender'] = melted_df['Descriptor'].str.extract(r'(Male|Female)$')[0]

# Map Category
melted_df['Category'] = melted_df['Descriptor'].map(descriptor_to_category)

# Clean data
melted_df['Enrollees'] = pd.to_numeric(melted_df['Enrollees'], errors='coerce')
melted_df.dropna(subset=['Category', 'Gender', 'Enrollees'], inplace=True)

# Group data
grouped = melted_df.groupby(['Category', 'Gender'], observed=False, as_index=False)['Enrollees'].sum()

# Ensure correct category order
category_order = ['K', 'ELEM', 'JHS', 'SHS']
grouped['Category'] = pd.Categorical(grouped['Category'], categories=category_order, ordered=True)
grouped = grouped.sort_values('Category')

# Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
])

# Layout
app.layout = html.Div([
    html.H2("Total Male and Female Enrollees by Category", className="text-center mt-4"),
    html.Div([
        dcc.Graph(id='stacked-bar-chart')
    ], className="mt-4 px-4")
])

# Callback
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    Input('stacked-bar-chart', 'id')  # Dummy input to trigger the callback
)
def update_stacked_bar_chart(_):
    # Calculate percentage and label
    total_per_category = grouped.groupby('Category')['Enrollees'].transform('sum')
    grouped['Percentage'] = (grouped['Enrollees'] / total_per_category) * 100
    grouped['Label'] = grouped.apply(
        lambda row: f"{int(row['Enrollees']):,} ({row['Percentage']:.1f}%)", axis=1
    )

    # Create stacked bar chart
    fig = px.bar(
        grouped,
        x='Percentage',
        y='Category',
        color='Gender',
        barmode='stack',
        orientation='h',
        text='Label',
        color_discrete_map={'Male': '#1f77b4', 'Female': '#e377c2'},
        title="Gender Distribution by Category (K, ELEM, JHS, SHS)"
    )

    total_all = int(grouped['Enrollees'].sum())
    fig.update_layout(
        title={
            'text': f"Gender Distribution by Category (K, ELEM, JHS, SHS)<br><sub>Total Enrollees: {total_all:,}</sub>",
            'x': 0.5
        },
        xaxis=dict(
            title='Percentage',
            ticksuffix='%',
            range=[0, 100]
        ),
        yaxis_title='Category',
        height=600,
        legend_title='Gender',
        margin=dict(l=100, r=40, t=80, b=60)
    )
    fig.update_traces(textposition='inside', insidetextanchor='middle')

    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
