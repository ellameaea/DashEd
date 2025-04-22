import pandas as pd
import plotly.express as px
import os
import re
import plotly.io as pio

# Automatically reads files from the CSV folder
def load_and_process_data(directory):
    data = []
    pattern = re.compile(r'CLEANED_SY(\d{4})_Enrollment\.csv')

    # Loop through all files in the directory
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

# Function to plot enrollment trend
def plot_enrollment_trend(data):
    """
    Plot a line chart for total enrollees by year.
    Args:
        data (pd.DataFrame): DataFrame containing 'Year' and 'Total Enrollees'.
    """
    data = data.sort_values(by='Year') # Sort by year

    # Ensure the 'Year' column is numeric
    fig = px.line(data, 
                  x='Year', # X-axis values
                  y='Total Enrollees', # Y-axis values
                  title='Total Enrollees by Year', # Chart title
                  labels={'Year': 'Year', # X-axis label
                          'Total Enrollees': 'Total Enrollees'}, # Y-axis label
                  markers=True) # Show markers on the line
    # Set the template for the chart
    fig.update_traces(line=dict(color='blue', # Line color
                                width=2), # Line width
                      marker=dict(size=8))  # Marker size
    fig.update_layout(title_x=0.5) # Center the title
    
    fig.update_xaxes(dtick=1, tickformat='.0f') # Set x-axis ticks to 1 year and format
    fig.show()

# Set the folder containing the cleaned enrollment files
csv_folder = 'CSV Files'

# Load and process data
enrollment_data = load_and_process_data(csv_folder)

# Plot the enrollment trend
plot_enrollment_trend(enrollment_data)
