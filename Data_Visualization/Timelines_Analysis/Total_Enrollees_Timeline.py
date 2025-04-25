# trend_chart.py

import pandas as pd
import plotly.express as px
import os
import re

def get_enrollment_trend_figure(directory='CSV Files'):
    data = []
    pattern = re.compile(r'CLEANED_SY(\d{4})_Enrollment\.csv')

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            year = int(match.group(1))
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            enrollment_columns = [col for col in df.columns if col.endswith('Male') or col.endswith('Female')]
            total_enrollees = df[enrollment_columns].sum().sum()
            data.append({'Year': year, 'Total Enrollees': total_enrollees})
    
    df = pd.DataFrame(data).sort_values(by='Year')

    fig = px.line(df, x='Year', y='Total Enrollees', title='',
                  labels={'Year': 'Year', 'Total Enrollees': 'Total Enrollees'},
                  markers=True)
    fig.update_traces(line=dict(color='blue', width=2), marker=dict(size=8))
    fig.update_layout(title_x=0.5, height=750)
    fig.update_xaxes(dtick=1, tickformat='.0f')

    return fig

def get_latest_total_enrollees(directory='CSV Files'):
    """
    Get the total number of enrollees from the most recent year.
    """
    # careful with this. Make sure that the correct year is selected. 
    # title_enrollees for overview.py
    data = []
    pattern = re.compile(r'CLEANED_SY(\d{4})_Enrollment\.csv')

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            year = int(match.group(1))
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            enrollment_columns = [col for col in df.columns if col.endswith('Male') or col.endswith('Female')]
            total_enrollees = df[enrollment_columns].sum().sum()
            data.append({'Year': year, 'Total Enrollees': total_enrollees})
    
    df = pd.DataFrame(data)
    latest_row = df[df['Year'] == df['Year'].max()]
    return int(latest_row['Total Enrollees'].values[0])
