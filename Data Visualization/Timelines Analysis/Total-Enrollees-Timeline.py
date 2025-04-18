import pandas as pd
import plotly.express as px
import os
import re
import plotly.io as pio

def load_and_process_data(directory):
    data = []
    pattern = re.compile(r'CLEANED_SY(\d{4})_Enrollment\.csv')

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            year = int(match.group(1))
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            # Only sum enrollment columns: those that end with 'Male' or 'Female'
            enrollment_columns = [col for col in df.columns if col.endswith('Male') or col.endswith('Female')]
            total_enrollees = df[enrollment_columns].sum().sum()

            data.append({'Year': year, 'Total Enrollees': total_enrollees})
    
    return pd.DataFrame(data)

def plot_enrollment_trend(data):
    """
    Plot a line chart for total enrollees by year.
    Args:
        data (pd.DataFrame): DataFrame containing 'Year' and 'Total Enrollees'.
    """
    data = data.sort_values(by='Year')

    fig = px.line(data, x='Year', y='Total Enrollees', title='Total Enrollees by Year',
                  labels={'Year': 'Year', 'Total Enrollees': 'Total Enrollees'},
                  markers=True)
    fig.update_traces(line=dict(color='blue', width=2), marker=dict(size=8))
    fig.update_layout(title_x=0.5)
    
    fig.update_xaxes(dtick=1, tickformat='.0f')
    fig.show()

# Set the folder containing the cleaned enrollment files
csv_folder = 'CSV Files'

# Load and process data
enrollment_data = load_and_process_data(csv_folder)

# Plot the enrollment trend
plot_enrollment_trend(enrollment_data)
