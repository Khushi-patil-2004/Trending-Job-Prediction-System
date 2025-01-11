import pandas as pd
import re
import os

# Load the raw data
raw_data_path = 'data/raw/indeed_job_data.csv'
df = pd.read_csv(raw_data_path)

# Function to extract experience from description
def extract_experience(text):
    match = re.search(r'(\d+\s*-\s*\d+|\d+\s*\+?)\s*yrs?', str(text), re.IGNORECASE)
    return match.group(0) if match else 'Not Available'

# Function to extract education from description
def extract_education(text):
    education_terms = ['BCA', 'BSc', 'MCA', 'MSc', 'Engineering', 'MBA']
    for term in education_terms:
        if term in str(text):
            return term
    return 'Not Available'

# Function to extract responsibilities (simple example)
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

# Select necessary columns for the cleaned data
required_columns = [
    'company', 'positionName', 'location', 'experience', 'education',
    'description', 'responsibilities', 'key_result_areas', 'skills', 
    'externalApplyLink', 'salary'
]

# Check for any missing columns in the dataframe after extraction
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Still missing columns: {', '.join(missing_columns)}")
else:
    # Filter and clean the data
    df_cleaned = df[required_columns].copy()

    # Save the cleaned data to a new file
    output_path = 'data/processed/cleaned_job_data_v2.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    print(f'Cleaned job data saved to {output_path}')
