import pandas as pd
import os
from dash import Dash, html, dcc  # Replace JupyterDash with Dash
from dash.dependencies import Input, Output

dataset = 'CSV Files/SY 2023-2024 School Level Data on Official Enrollment 13.xlsx'
df = pd.read_excel(dataset, sheet_name='DB', skiprows=4)

# Print the actual column names from the DataFrame to inspect them
print(df.columns)

columns_to_check = [
    'School Subclassification','K Male', 'K Female', 'G1 Male', 'G1 Female', 'G2 Male', 'G2 Female',
    'G3 Male', 'G3 Female', 'G4 Male', 'G4 Female', 'G5 Male', 'G5 Female',
    'G6 Male', 'G6 Female', 'Elem NG Male', 'Elem NG Female', 'G7 Male', 'G7 Female',
    'G8 Male', 'G8 Female', 'JHS NG Male', 'JHS NG Female',
    'G9 Male', 'G9 Female', 'G10 Male', 'G10 Female',
    'G11 ACAD STEM Male', 'G11 ACAD STEM Female', 'G11 ACAD - HUMSS Male', 'G11 ACAD - HUMSS Female',
    'G11 ACAD - ABM Male', 'G11 ACAD - ABM Female', 'G11 ACAD GAS Male', 'G11 ACAD GAS Female',
    'G11 ACAD PBM Male', 'G11 ACAD PBM Female', 'G11 TVL Male', 'G11 TVL Female',
    'G11 SPORTS Male', 'G11 SPORTS Female', 'G11 ARTS Male', 'G11 ARTS Female',
    'G12 ACAD STEM Male', 'G12 ACAD STEM Female', 'G12 ACAD - HUMSS Male', 'G12 ACAD - HUMSS Female',
    'G12 ACAD - ABM Male', 'G12 ACAD - ABM Female', 'G12 ACAD GAS Male', 'G12 ACAD GAS Female',
    'G12 ACAD PBM Male', 'G12 ACAD PBM Female', 'G12 TVL Male', 'G12 TVL Female',
    'G12 SPORTS Male', 'G12 SPORTS Female', 'G12 ARTS Male', 'G12 ARTS Female'
]

# Drop "Street Address"
df.drop(columns=['Street Address'], inplace=True)

# Check for duplication (BEIS School ID)
df.drop_duplicates(subset='BEIS School ID', inplace=True)

# Drop rows where 'Region' contains 'PSO'
df.drop(df[df['Region'].str.contains('PSO', na=False)].index, inplace=True)

# Replace abbreviations in 'School Name'
df['School Name'] = df['School Name'].str.replace(r'\bES\b', 'Elementary School', regex=True)
df['School Name'] = df['School Name'].str.replace(r'\bHS\b', 'High School', regex=True)

columns_to_rename = {
    'G11 ACAD - HUMSS Male': 'G11 ACAD HUMSS Male',
    'G11 ACAD - HUMSS Female': 'G11 ACAD HUMSS Female',
    'G11 ACAD - ABM Male': 'G11 ACAD ABM Male',
    'G11 ACAD - ABM Female': 'G11 ACAD ABM Female',
    'G12 ACAD - HUMSS Male': 'G12 ACAD HUMSS Male',
    'G12 ACAD - HUMSS Female': 'G12 ACAD HUMSS Female',
    'G12 ACAD - ABM Male': 'G12 ACAD ABM Male',
    'G12 ACAD - ABM Female': 'G12 ACAD ABM Female',
}

df.rename(columns=columns_to_rename, inplace=True)

current_directory = os.getcwd()
output_directory = os.path.join(current_directory, 'CSV Files')
os.makedirs(output_directory, exist_ok=True)
cleaned_file = os.path.join(output_directory, 'CLEANED_SY2023_Enrollment.csv')
df.to_csv(cleaned_file, index=False)