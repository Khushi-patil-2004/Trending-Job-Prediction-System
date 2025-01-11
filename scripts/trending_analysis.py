# scripts/trending_analysis.py
import pandas as pd
from collections import Counter
import ast
import json

def analyze_trending_jobs_and_skills(input_path):
    # Load the dataset
    df = pd.read_csv(input_path)

    # Analyze job titles
    if 'positionName' in df.columns:
        job_title_counts = df['positionName'].value_counts().head(10)
        print("Top 10 Job Titles:\n", job_title_counts)
    else:
        print("Column 'positionName' not found in the dataset.")
        job_title_counts = pd.Series()  # Empty series as fallback

    # Analyze skills
    if 'skills' in df.columns:
        def extract_skills(skill_list):
            try:
                skills = ast.literal_eval(skill_list)
                if not isinstance(skills, list):
                    skills = []
            except (ValueError, SyntaxError):
                skills = []
            return skills

        df['extracted_skills'] = df['skills'].dropna().apply(extract_skills)
        
        # Filter out NaN values
        df = df.dropna(subset=['extracted_skills'])
        
        all_skills = [skill for sublist in df['extracted_skills'] for skill in sublist]
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(10)
        print("Top 10 Skills:\n", top_skills)
    else:
        print("Column 'skills' not found in the dataset.")
        top_skills = []

    # Save results to JSON files
    job_title_counts_df = job_title_counts.reset_index()
    job_title_counts_df.columns = ['positionName', 'count']
    job_title_counts_list = job_title_counts_df.to_dict(orient='records')
    
    with open('data/results/top_job_titles.json', 'w') as f:
        json.dump(job_title_counts_list, f)

    top_skills_list = [{'skill': skill, 'count': count} for skill, count in top_skills]
    with open('data/results/top_skills.json', 'w') as f:
        json.dump(top_skills_list, f)

    return job_title_counts, top_skills

if __name__ == "__main__":
    analyze_trending_jobs_and_skills('data/processed/cleaned_indeed_job_data.csv')
