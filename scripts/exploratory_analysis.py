# import pandas as pd
# import matplotlib.pyplot as plt
# from collections import Counter

# # Load the cleaned data
# df = pd.read_csv('data/processed/cleaned_indeed_job_data.csv')

# # Top job titles
# top_job_titles = df['positionName'].value_counts().head(10)
# print("Top 10 Job Titles:\n", top_job_titles)

# # Plotting top job titles
# top_job_titles.plot(kind='bar', title='Top 10 Job Titles', xlabel='Job Title', ylabel='Number of Postings')
# plt.xticks(rotation=45)
# plt.savefig('data/results/top_job_titles.png')
# plt.show()

# # Aggregate all skills into a single list
# all_skills = [skill for skills_list in df['skills'] for skill in skills_list]
# top_skills = Counter(all_skills).most_common(10)
# skills, counts = zip(*top_skills)

# # Plotting top skills
# plt.bar(skills, counts)
# plt.title('Top 10 Skills')
# plt.xlabel('Skills')
# plt.ylabel('Frequency')
# plt.xticks(rotation=45)
# plt.savefig('data/results/top_skills.png')
# plt.show()



import pandas as pd
import json
from collections import Counter

# Load the cleaned data
df = pd.read_csv('data/processed/cleaned_indeed_job_data.csv')

# Top job titles
top_job_titles = df['positionName'].value_counts().head(10)
top_job_titles_list = top_job_titles.reset_index().to_dict(orient='records')

# Save the top job titles to a JSON file
with open('data/results/top_job_titles.json', 'w') as f:
    json.dump(top_job_titles_list, f)

# Convert 'skills' column from comma-separated strings to lists
df['skills'] = df['skills'].apply(lambda x: [skill.strip() for skill in x.split(',')] if pd.notna(x) else [])

# Aggregate all skills into a single list
all_skills = [skill for skills_list in df['skills'] for skill in skills_list]
top_skills = Counter(all_skills).most_common(10)
skills, counts = zip(*top_skills)

# Save the top skills to a JSON file
top_skills_list = [{'skill': skill, 'count': count} for skill, count in zip(skills, counts)]
with open('data/results/top_skills.json', 'w') as f:
    json.dump(top_skills_list, f)
