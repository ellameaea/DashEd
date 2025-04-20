import pandas as pd
import plotly.express as px
import os
import re

def load_and_process_data(directory):
    data = []
    pattern = re.compile(r'CLEANED_SY(\d{4})_Enrollment\.csv')

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            year = int(match.group(1))
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            # KINDERGARTEN
            kinder_cols = ['K Male', 'K Female']
            kinder_total = df[kinder_cols].sum().sum()

            # ELEM: G1 to G6
            elem_cols = [f'G{i} Male' for i in range(1, 7)] + [f'G{i} Female' for i in range(1, 7)]
            elem_total = df[elem_cols].sum().sum()

            # JHS: G7 to G10
            jhs_cols = [f'G{i} Male' for i in range(7, 11)] + [f'G{i} Female' for i in range(7, 11)]
            jhs_total = df[jhs_cols].sum().sum()

            # SHS: All G11 and G12 strands
            strands = ['STEM', 'HUMSS', 'ABM', 'GAS', 'TVL', 'SPORTS', 'ARTS', 'PBM']
            shs_cols = []
            for grade in [11, 12]:
                for strand in strands:
                    if strand in ['STEM', 'HUMSS', 'ABM', 'GAS', 'PBM']:
                        shs_cols += [f'G{grade} ACAD {strand} Male', f'G{grade} ACAD {strand} Female']
                    else:
                        shs_cols += [f'G{grade} {strand} Male', f'G{grade} {strand} Female']
            shs_total = df[[col for col in shs_cols if col in df.columns]].sum().sum()

            data.append({
                'Year': year,
                'Kindergarten': kinder_total,
                'ELEM': elem_total,
                'JHS': jhs_total,
                'SHS': shs_total 
            })

    return pd.DataFrame(data)

def plot_enrollment_by_level(data):
    data = data.sort_values(by='Year')

    # Melt data to long format
    melted = data.melt(id_vars='Year',
                       value_vars=['Kindergarten', 'ELEM', 'JHS', 'SHS'],
                       var_name='Education Level', value_name='Total Enrollees')

    # Define custom colors
    color_map = {
        'Kindergarten': '#a259ff',  # Soft purple
        'ELEM': '#636efa',          # Plotly blue
        'JHS': '#ef553b',           # Reddish-orange
        'SHS': '#00cc96'            # Teal green
    }

    fig = px.line(melted, x='Year', y='Total Enrollees', color='Education Level',
                  title='Enrollment Trends by Education Level (Kinder to SHS)',
                  markers=True, color_discrete_map=color_map)

    fig.update_traces(line=dict(width=2), marker=dict(size=8))
    fig.update_layout(title_x=0.5)
    fig.update_xaxes(dtick=1, tickformat='.0f')
    fig.show()

# Folder containing the cleaned CSV files
csv_folder = 'CSV Files'

# Load and process
enrollment_data = load_and_process_data(csv_folder)

# Plot the result
plot_enrollment_by_level(enrollment_data)
