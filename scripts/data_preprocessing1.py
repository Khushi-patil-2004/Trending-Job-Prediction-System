import pandas as pd
import re
import numpy as np
import datetime

# Load the raw data
raw_data_path = 'data/raw/indeed_job_data.csv'
try:
    df = pd.read_csv(raw_data_path)
except FileNotFoundError:
    raise FileNotFoundError(f"The file {raw_data_path} does not exist.")
except pd.errors.EmptyDataError:
    raise ValueError(f"The file {raw_data_path} is empty.")

# Function to extract experience from description
def extract_experience(text):
    match = re.search(r'(\d+\s*-\s*\d+|\d+\s*\+?)\s*yrs?', str(text), re.IGNORECASE)
    return match.group(0) if match else 'Not Available'

# Function to extract education from description
def extract_education(text):
    education_terms = ['BCA', 'BSc', 'MCA', 'MSc', 'Engineering', 'MBA']
    text_upper = str(text).upper()
    for term in education_terms:
        if term in text_upper:
            return term
    return 'Not Available'

# Function to extract responsibilities
def extract_responsibilities(text):
    match = re.search(r'Responsibilities:([\s\S]*?)(\n\n|$)', str(text), re.IGNORECASE)
    return match.group(1).strip() if match else 'Not Available'

# Function to extract key result areas
def extract_key_result_areas(text):
    match = re.search(r'Key Result Areas:([\s\S]*?)(\n\n|$)', str(text), re.IGNORECASE)
    return match.group(1).strip() if match else 'Not Available'

# Function to extract skills
def extract_skills(text):
    match = re.search(r'Skills:([\s\S]*?)(\n\n|$)', str(text), re.IGNORECASE)
    return match.group(1).strip() if match else 'Not Available'

# Apply the extraction functions
df['experience'] = df['description'].apply(extract_experience)
df['education'] = df['description'].apply(extract_education)
df['responsibilities'] = df['description'].apply(extract_responsibilities)
df['key_result_areas'] = df['description'].apply(extract_key_result_areas)
df['skills'] = df['description'].apply(extract_skills)

# Add a synthetic date column (for testing purposes)
np.random.seed(0)  # For reproducibility
start_date = datetime.date(2023, 1, 1)
num_days = (datetime.date.today() - start_date).days
df['date'] = [start_date + datetime.timedelta(days=int(np.random.rand() * num_days)) for _ in range(len(df))]

# Ensure 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Check and validate columns
required_columns = [
    'company', 'positionName', 'location', 'experience', 'education',
    'description', 'responsibilities', 'key_result_areas', 'skills', 'salary', 'externalApplyLink', 'date'
]

missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
else:
    # Filter and clean the data
    df_cleaned = df[required_columns].copy()

    # Save the cleaned data
    output_path = 'data/processed/cleaned_with_date.csv'
    df_cleaned.to_csv(output_path, index=False)
    print(f'Cleaned job data saved to {output_path}')
