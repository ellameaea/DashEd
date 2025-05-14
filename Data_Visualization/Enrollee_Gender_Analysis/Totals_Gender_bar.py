import pandas as pd
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go

# ——— Figure builder: Stacked Gender Bar by Category ———
def gender_bar(df: pd.DataFrame) -> go.Figure:
    """
    Given a DataFrame with enrollment records, returns a horizontal
    stacked bar chart of gender distribution by category (K, ELEM, JHS, SHS).
    """
    # Melt the DataFrame to long format
    melted = df.melt(
        id_vars=["Region"],
        var_name="Descriptor",
        value_name="Enrollees"
    )

    # Define category mapping
    combined_levels = {
        'K': ['K Male', 'K Female'],
        'ELEM': [
            'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
            'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female',
            'G5 Male', 'G5 Female', 'G6 Male', 'G6 Female',
            'Elem NG Male', 'Elem NG Female'
        ],
        'JHS': [
            'G7 Male', 'G7 Female', 'G8 Male', 'G8 Female',
            'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female',
            'JHS NG Male', 'JHS NG Female'
        ],
        'SHS': [
            'G11 ACAD ABM Male', 'G11 ACAD ABM Female',
            'G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female',
            'G11 ACAD STEM Male', 'G11 ACAD STEM Female',
            'G11 ACAD GAS Male', 'G11 ACAD GAS Female',
            'G11 ACAD PBM Male', 'G11 ACAD PBM Female',
            'G11 TVL Male', 'G11 TVL Female',
            'G11 SPORTS Male', 'G11 SPORTS Female',
            'G11 ARTS Male', 'G11 ARTS Female',
            'G12 ACAD ABM Male', 'G12 ACAD ABM Female',
            'G12 ACAD HUMSS Male', 'G12 ACAD HUMSS Female',
            'G12 ACAD STEM Male', 'G12 ACAD STEM Female',
            'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
            'G12 ACAD PBM Male', 'G12 ACAD PBM Female',
            'G12 TVL Male', 'G12 TVL Female',
            'G12 SPORTS Male', 'G12 SPORTS Female',
            'G12 ARTS Male', 'G12 ARTS Female'
        ]
    }

    # Build descriptor to category map
    descriptor_map = {desc: cat for cat, descs in combined_levels.items() for desc in descs}

    # Extract gender and category
    melted['Gender'] = melted['Descriptor'].str.extract(r'(Male|Female)$')
    melted['Category'] = melted['Descriptor'].map(descriptor_map)

    # Clean and drop NA
    melted['Enrollees'] = pd.to_numeric(melted['Enrollees'], errors='coerce').fillna(0)
    melted = melted.dropna(subset=['Category', 'Gender'])

    # Aggregate
    grouped = (
        melted
        .groupby(['Category', 'Gender'], as_index=False)['Enrollees']
        .sum()
    )

    # Order categories
    category_order = ['K', 'ELEM', 'JHS', 'SHS']
    grouped['Category'] = pd.Categorical(grouped['Category'], categories=category_order, ordered=True)
    grouped = grouped.sort_values('Category')

    # Compute labels
    totals = grouped.groupby('Category')['Enrollees'].transform('sum')
    grouped['Percentage'] = grouped['Enrollees'] / totals * 100
    grouped['Label'] = grouped.apply(lambda r: f"{int(r['Enrollees']):,} ({r['Percentage']:.1f}%)", axis=1)

    # Create figure
    fig = px.bar(
        grouped,
        x='Percentage',
        y='Category',
        color='Gender',
        barmode='stack',
        orientation='h',
        text='Label',
        color_discrete_map={'Male': '#084683', 'Female': '#DE082C'}
    )

    total_all = int(grouped['Enrollees'].sum())
    fig.update_layout(
        title={
            'text': (
                "Gender Distribution by Category (K, ELEM, JHS, SHS)"
                f"<br><sub>Total Enrollees: {total_all:,}</sub>"
            ),
            'x': 0.5,
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'bottom',
            'pad': {'t': 15}
        },
        xaxis=dict(title='Percentage', ticksuffix='%', range=[0,100]),
        yaxis_title='Category',
        height=380,
        legend_title='Gender',
        margin=dict(l=20, r=20, t=80, b=20)
    )
    fig.update_traces(textposition='inside', insidetextanchor='middle')

    return fig

# # ——— Component builder: Gender Bar with Loading Spinner ———
# def create_gender_bar(df: pd.DataFrame, graph_id: str = 'overview-graph') -> dcc.Loading:
#     """
#     Returns a dcc.Loading wrapper containing the gender bar Graph.
#     """
#     return dcc.Loading(
#         dcc.Graph(
#             id=graph_id,
#             figure=gender_bar(df),
#             config={'displayModeBar': False},
#             style={'height': '100%', 'width': '100%'}
#         ),
#         type='circle',
#         style={'height': '380px', 'width': '100%', 'display': 'inline-block'}
#     )
