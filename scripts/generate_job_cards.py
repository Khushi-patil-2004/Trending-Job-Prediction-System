# import pandas as pd
# import os

# # Load the cleaned data
# df = pd.read_csv('data/processed/cleaned_indeed_job_data.csv')

# # Check column names
# print("Column names in the dataset:")
# print(df.columns)

# # Define the path for saving the generated job cards
# output_dir = 'data/generated_job_cards'
# os.makedirs(output_dir, exist_ok=True)

# # Define a template for job cards
# job_card_template = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Job Card</title>
#     <style>
#         .job-card {{
#             border: 1px solid #ddd;
#             border-radius: 8px;
#             padding: 16px;
#             margin-bottom: 16px;
#             box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#         }}
#         .job-card h2 {{
#             margin: 0;
#             font-size: 1.5em;
#         }}
#         .job-card p {{
#             margin: 0.5em 0;
#         }}
#     </style>
# </head>
# <body>
#     <div class="job-card">
#         <h2>{positionName}</h2>
#         <p><strong>Description:</strong></p>
#         <p>{description}</p>
#     </div>
# </body>
# </html>
# """

# # Generate a job card for each job posting
# for index, row in df.iterrows():
#     # Prepare the job card content
#     job_card_html = job_card_template.format(
#         positionName=row['positionName'],
#         description=row['description']
#     )
    
#     # Save the job card HTML to a file with UTF-8 encoding
#     file_path = os.path.join(output_dir, f'job_card_{index + 1}.html')
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write(job_card_html)

# print(f"Job cards have been generated and saved to {output_dir}")



# import pandas as pd
# from jinja2 import Environment, FileSystemLoader
# import os

# # Load the cleaned data
# df = pd.read_csv('data/processed/cleaned_indeed_job_data.csv')

# # Top job titles with high demand
# top_job_titles = df['positionName'].value_counts().head(10).index

# # Filter jobs based on top job titles
# top_jobs = df[df['positionName'].isin(top_job_titles)]

# # Load the Jinja2 template
# env = Environment(loader=FileSystemLoader('templates'))
# template = env.get_template('job_card_template.html')

# # Generate job cards
# job_cards = ""
# for _, row in top_jobs.iterrows():
#     job_card = template.render(
#         position=row['positionName'],
#         description=row['description'],
#         url="http://example.com"  # Placeholder URL; you may adjust based on your data
#     )
#     job_cards += job_card

# # Save the dashboard HTML
# output_path = 'output/dashboard.html'
# with open(output_path, 'w') as f:
#     f.write(f"""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Job Dashboard</title>
#         <link rel="stylesheet" href="styles.css">
#     </head>
#     <body>
#         <div class="container">
#             <h1>Trending Job Listings</h1>
#             {job_cards}
#         </div>
#     </body>
#     </html>
#     """)

# print(f'Dashboard HTML saved to {output_path}')




# scripts/generate_job_cards.py
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import json

# Load the cleaned data
df = pd.read_csv('data/processed/cleaned_indeed_job_data.csv')

# Check if necessary columns are present
required_columns = ['company', 'positionName', 'location', 'experience', 'education', 'responsibilities', 'key_result_areas', 'skills', 'externalApplyLink']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Missing columns: {', '.join(missing_columns)}")
    exit(1)

# Load the Jinja2 template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('job_card_template.html')

# Load the top job titles
with open('data/results/top_job_titles.json') as f:
    top_job_titles = json.load(f)

# Extract top job titles for job cards
top_job_title_names = [job['positionName'] for job in top_job_titles]

# Ensure unique job titles
unique_top_job_title_names = list(dict.fromkeys(top_job_title_names))

# Filter the dataframe for these top job titles
df_top_jobs = df[df['positionName'].isin(unique_top_job_title_names)]

# Function to safely handle the 'skills' field
def format_skills(skills_str):
    try:
        if pd.notna(skills_str):
            return ', '.join(eval(skills_str))
        return 'Not Available'
    except (SyntaxError, ValueError):
        return 'Not Available'

# Generate job cards
job_cards = ""
for i, row in df_top_jobs.iterrows():
    card_id = f"card_{i}"
    job_card = template.render(
        card_id=card_id,
        position=row.get('positionName', 'Not Available'),
        company=row.get('company', 'Not Available'),
        location=row.get('location', 'Not Available'),
        experience=row.get('experience', 'Not Available'),
        education=row.get('education', 'Not Available'),
        responsibilities=row.get('responsibilities', 'Not Available'),
        key_result_areas=row.get('key_result_areas', 'Not Available'),
        skills=format_skills(row['skills']),
        apply_link=row.get('externalApplyLink', '#')
    )
    job_cards += job_card

# Save the dashboard HTML
output_path = 'output/dashboard.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 80%;
                margin: 0 auto;
                padding: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Trending Job Listings</h1>
            {job_cards}
        </div>
    </body>
    </html>
    """)

print(f'Dashboard HTML saved to {output_path}')
