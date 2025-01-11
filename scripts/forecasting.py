# import pandas as pd
# import matplotlib.pyplot as plt
# from collections import Counter
# import re

# # Load the cleaned data
# df = pd.read_csv('data/processed/cleaned_with_date.csv')

# # Ensure 'date' column exists and is in datetime format
# if 'date' in df.columns:
#     df['date'] = pd.to_datetime(df['date'], errors='coerce')
# else:
#     print("The dataset lacks a 'date' column. Trending analysis requires dates for time series plotting.")
#     exit(1)

# # Define the list of key skills to analyze
# key_skills = [
#     'java', 'html5', 'css', 'bootstrap', 'problem solving', 'decision making',
#     'backend developer', 'js', 'javascript', 'python', 'sql', 'react', 'node.js'
# ]

# # Function to extract skills from text
# def extract_skills(text):
#     if not isinstance(text, str):
#         return []
#     text = text.lower()
#     skills = []
#     for skill in key_skills:
#         if re.search(r'\b' + re.escape(skill) + r'\b', text):
#             skills.append(skill)
#     return skills

# # Trending Skills Analysis
# def analyze_trending_skills(df):
#     if 'description' not in df.columns:
#         print("The dataset lacks a 'description' column. Trending skills analysis requires description data.")
#         return

#     # Extract skills from descriptions
#     df['skills'] = df['description'].apply(extract_skills)
    
#     # Create a 'year_month' column for grouping by month
#     df['year_month'] = df['date'].dt.to_period('M')
    
#     # Create a DataFrame to store skill counts over time
#     skill_time_series = df.explode('skills').dropna(subset=['skills'])
#     skill_time_series['skill'] = skill_time_series['skills'].apply(lambda x: x.strip())  # Clean skill names
    
#     # Print a sample of skills after extraction
#     print("Sample of skills after extraction:")
#     print(skill_time_series[['skill']].dropna().head(10))
    
#     # Filter to include only the key skills
#     skill_time_series = skill_time_series[skill_time_series['skill'].isin(key_skills)]
    
#     # Check if there are any skills left after filtering
#     if skill_time_series.empty:
#         print("No key skills found in the data after filtering.")
#         return
    
#     # Aggregate counts by month and skill
#     skill_counts_over_time = skill_time_series.groupby(['year_month', 'skill']).size().unstack(fill_value=0)
    
#     # Check the contents of the DataFrame before plotting
#     print("Skill counts over time:")
#     print(skill_counts_over_time.head())
    
#     # Check if the DataFrame is empty
#     if skill_counts_over_time.empty or skill_counts_over_time.select_dtypes(include=['number']).empty:
#         print("No numeric data to plot.")
#         return
    
#     # Plotting the stacked bar chart for the key skills over time
#     plt.figure(figsize=(14, 8))
#     skill_counts_over_time.plot(kind='bar', stacked=True, colormap='tab10')
#     plt.title('Trending Key Skills Over Time')
#     plt.xlabel('Year-Month')
#     plt.ylabel('Number of Postings')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.legend(title='Skills', loc='upper left')
#     plt.savefig('data/results/trending_key_skills_over_time.png')
#     plt.show()

# # Run the skills analysis function
# analyze_trending_skills(df)

import pandas as pd
import plotly.express as px
import re

# Load the cleaned data
df = pd.read_csv('data/processed/cleaned_with_date.csv')

# Ensure 'date' column exists and is in datetime format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
else:
    print("The dataset lacks a 'date' column. Trending analysis requires dates for time series plotting.")
    exit(1)

# Define the list of key skills to analyze
key_skills = [
    'java', 'html5', 'css', 'bootstrap', 'problem solving', 'decision making',
    'backend developer', 'js', 'javascript', 'python', 'sql', 'react', 'node.js'
]

# Function to extract skills from text
def extract_skills(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    skills = []
    for skill in key_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            skills.append(skill)
    return skills

# Trending Skills Analysis
def analyze_trending_skills(df):
    if 'description' not in df.columns:
        print("The dataset lacks a 'description' column. Trending skills analysis requires description data.")
        return

    # Extract skills from descriptions
    df['skills'] = df['description'].apply(extract_skills)
    
    # Create a 'year_month' column for grouping by month
    df['year_month'] = df['date'].dt.to_period('M')
    
    # Create a DataFrame to store skill counts over time
    skill_time_series = df.explode('skills').dropna(subset=['skills'])
    skill_time_series['skill'] = skill_time_series['skills'].apply(lambda x: x.strip())  # Clean skill names
    
    # Print a sample of skills after extraction
    print("Sample of skills after extraction:")
    print(skill_time_series[['skill']].dropna().head(10))
    
    # Filter to include only the key skills
    skill_time_series = skill_time_series[skill_time_series['skill'].isin(key_skills)]
    
    # Check if there are any skills left after filtering
    if skill_time_series.empty:
        print("No key skills found in the data after filtering.")
        return
    
    # Aggregate counts by skill
    skill_counts = skill_time_series['skill'].value_counts().reset_index()
    skill_counts.columns = ['skill', 'count']
    
    # Print the skill counts for checking
    print("Skill counts:")
    print(skill_counts)
    
    # Create a pie chart for the skill distribution
    fig = px.pie(
        skill_counts,
        names='skill',
        values='count',
        title='Distribution of Key Skills',
        labels={'skill': 'Key Skill', 'count': 'Number of Postings'}
    )
    
    # Show the plot
    fig.show()
    
    # Save the plot as a PNG file
    fig.write_image('data/results/trending_key_skills_distribution.png')
    print('Saved pie chart as data/results/trending_key_skills_distribution.png')

# Run the skills analysis function
analyze_trending_skills(df)
