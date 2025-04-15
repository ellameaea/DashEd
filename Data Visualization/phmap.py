import pandas as pd
import plotly.express as px
import json
import os
 
# Load your CSV data
current_directory = os.getcwd()
cleaned_file = os.path.join(current_directory, 'CSV Files/CLEANED_SY2023_Enrollment.csv')
df = pd.read_csv(cleaned_file)

# Load your GeoJSON data (ph.json)
json_file = os.path.join(current_directory, 'ph.json')
with open(json_file) as f:
    ph_geojson = json.load(f)

# Calculate total enrollees per region
enrollment_columns = [col for col in df.columns if ('Male' in col or 'Female' in col) and col != 'BEIS School ID']
region_enrollment = df.groupby('Region')[enrollment_columns].sum().sum(axis=1).reset_index()
region_enrollment.columns = ['Region', 'Total_Enrollees']

# Map region names from your CSV to the GeoJSON feature IDs.
region_mapping = {
    'Region I': 'Ilocos',
    'Region II': 'Cagayan Valley',
    'Region III': 'Central Luzon',
    'Region IV-A': 'Calabarzon',
    'MIMAROPA': 'Mimaropa',
    'Region V': 'Bicol',
    'Region VI': 'Western Visayas',
    'Region VII': 'Central Visayas',
    'Region VIII': 'Eastern Visayas',
    'Region IX': 'Zamboanga Peninsula',
    'Region X': 'Northern Mindanao',
    'Region XI': 'Davao',
    'Region XII': 'Soccsksargen',
    'NCR': 'National Capital Region',
    'CAR': 'Cordillera Administrative Region',
    'BARMM': 'Autonomous Region in Muslim Mindanao',
    'CARAGA': 'Caraga'
}

# Create a new column in your DataFrame with the GeoJSON feature IDs.
region_enrollment['id'] = region_enrollment['Region'].map(region_mapping)

# Print for inspection
print("Region Enrollment Data:")
print(region_enrollment)

print("\nGeoJSON Feature Names (first 5):")
for feature in ph_geojson['features'][:5]:
    print(feature['properties']['name'])

# Create the choropleth map
fig = px.choropleth_mapbox(
    region_enrollment,
    geojson=ph_geojson,
    locations='id',
    color='Total_Enrollees',
    featureidkey='properties.name',
    center={'lat': 12.8797, 'lon': 121.7740},
    mapbox_style='carto-positron',
    zoom=5,
    color_continuous_scale='Plasma',
    labels={'Total_Enrollees': 'Total Enrollees'},
    hover_data={'Region': True, 'Total_Enrollees': True}
)

# Use update_traces() to set the hovertemplate
fig.update_traces(
    hovertemplate="</b> <b style='color:%{marker.color}'>%{properties.name}</b><br>" +
                  "Total Enrollees: %{z}<extra></extra>"
)

fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
fig.show()