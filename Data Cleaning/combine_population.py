import pandas as pd
from dash import dcc, html, Input, Output
import plotly.express as px
import os

# To combine population of male and female enrolments per school

df = pd.read_csv('CSV Files/CLEANED_SY2023_Enrollment.csv')

combined_population_df = df[['Region', 'School Name', 'BEIS School ID', 'Division', 'District']].copy()

# Define grade levels
grade_levels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']

for grade in grade_levels:
    male_col = f'{grade} Male'
    female_col = f'{grade} Female'

    # Handle from kinder to grade 10
    combined_population_df[f'{grade} Total'] = df.apply(lambda row: row.get(male_col, 0) + row.get(female_col, 0), axis=1)

# Include all strands for grades 11 and 12
strands = ['STEM', 'HUMSS', 'ABM', 'GAS', 'TVL', 'SPORTS', 'ARTS', 'PBM']
for grade in [11, 12]:
    for strand in strands:
        # More robust column name generation
        male_col = f'G{grade} ACAD {strand} Male' if strand in ['STEM', 'HUMSS', 'ABM', 'GAS', 'PBM'] else f'G{grade} {strand} Male'
        female_col = f'G{grade} ACAD {strand} Female' if strand in ['STEM', 'HUMSS', 'ABM', 'GAS', 'PBM'] else f'G{grade} {strand} Female'

        # Check if columns exist for summing
        if male_col in df.columns and female_col in df.columns:
            combined_population_df[f'G{grade} {strand} Total'] = df.apply(lambda row: row.get(male_col, 0) + row.get(female_col, 0), axis=1)

# Save to a new CSV file
current_directory = os.getcwd()
output_directory = '/Users/aarondavelim/Documents/College year 3/2nd Sem/Big Data Analytics/DASH APP/DashEd/CSV Files'
combined_population_file = os.path.join(output_directory, 'combined_population.csv')
combined_population_df.to_csv(combined_population_file, index=False)

print(f"Combined population data saved to: {combined_population_file}")