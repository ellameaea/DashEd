import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the dataset
file_path = "CSV Files/CLEANED_SY2023_Enrollment.csv"
df = pd.read_csv(file_path)

# Columns with enrollment data
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

df[enrollment_columns] = df[enrollment_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

# Total schools
total_schools = df.shape[0]

# Export the value
def get_total_schools():
    return total_schools

def get_school_crowding_figure():
    # Load the dataset
    df = pd.read_csv('CSV Files/CLEANED_SY2023_Enrollment.csv')  # Adjust path as needed

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

    df['Total Enrollees'] = df[enrollee_columns].sum(axis=1)

    region_summary = df.groupby('Region').agg({
        'Total Enrollees': 'sum',
        'BEIS School ID': 'nunique'
    }).reset_index()

    region_summary.rename(columns={'BEIS School ID': 'Number of Schools'}, inplace=True)
    region_summary['Enrollees per School'] = (region_summary['Number of Schools'] / region_summary['Total Enrollees']) * 100
    region_summary = region_summary.sort_values(by='Enrollees per School', ascending=False).reset_index(drop=True)

    colors = []
    for idx in range(len(region_summary)):
        if idx == 0 or idx == len(region_summary) - 1:
            colors.append('green')
        else:
            colors.append('#90ee90')

    fig = go.Figure(data=[
        go.Bar(
            name='Enrollees per School',
            x=region_summary['Region'],
            y=region_summary['Enrollees per School'],
            marker_color=colors,
            text=region_summary['Enrollees per School'].round(2),
            textposition='outside'
        )
    ])

    fig.update_layout(
    height=550,
    title=dict(
        text='Measures of School Crowding per Region',
        font=dict(size=15)
    ),
    xaxis_title='Region',
    yaxis=dict(
        title='Percentage (%)',
        range=[0, region_summary['Enrollees per School'].max() * 1.1]
    ),
    barmode='group',
    legend=dict(title='Metric'),
    xaxis_tickangle=-45,
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    margin=dict(b=200),
    annotations=[
        dict(
            text="Normal crowding across regions will be reached after <b>n years</b>",
            xref="paper", yref="paper",
            x=1, y=-0.6,
            showarrow=False,
            font=dict(size=18, color="#084683"),
            xanchor='right'
        ),
        dict(
            text="<b>Student Population Heatmap by Region and Strand</b>",
            xref="paper", yref="paper",
            x=0, y=-0.8,
            showarrow=False,
            font=dict(size=18, color="#DE082C"),
            xanchor='left'
        )
    ]
)

    return fig

# Load CSV
combined_population_df = pd.read_csv('CSV Files/combined_population_2023.csv')

# Generate default heatmap for 'G11'
def generate_heatmap(selected_grade='G11'):
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
        xaxis_title="Strand",
        yaxis_title="Region",
        autosize=False,
        width=700,
        height=550,
        margin=dict(l=100, r=50, t=40, b=100),
        font=dict(size=10),
    )
    fig.update_xaxes(tickangle=45)

    return fig
