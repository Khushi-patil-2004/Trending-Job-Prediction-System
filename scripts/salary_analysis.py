import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
cleaned_data_path = 'data/processed/cleaned_job_data_v2.csv'
df = pd.read_csv(cleaned_data_path)

# Print column names to verify
print("Column names in the dataset:")
print(df.columns)

# Filter for a specific job title, e.g., "Full Stack Developer"
job_title = "Full Stack Developer"
filtered_df = df[df['positionName'].str.contains(job_title, case=False, na=False)].copy()

# Print the filtered data to check if there are any rows
print("Filtered data:")
print(filtered_df.head())

# Ensure the 'salary' column exists
if 'salary' not in filtered_df.columns:
    print("Salary column is not available in the dataset.")
else:
    # Drop rows where salary is NaN
    filtered_df = filtered_df.dropna(subset=['salary'])
    
    # Clean salary column
    filtered_df['salary'] = filtered_df['salary'].str.replace(r'[₹,$]', '', regex=True)
    filtered_df['salary'] = filtered_df['salary'].str.replace(' - ', '-', regex=False)

    # Split salary into min and max
    filtered_df[['min_salary', 'max_salary']] = filtered_df['salary'].str.split('-', expand=True)
    filtered_df['min_salary'] = pd.to_numeric(filtered_df['min_salary'], errors='coerce')
    filtered_df['max_salary'] = pd.to_numeric(filtered_df['max_salary'], errors='coerce')

    # Calculate average salary
    filtered_df['average_salary'] = filtered_df[['min_salary', 'max_salary']].mean(axis=1)

    # Drop rows where average_salary is NaN
    filtered_df = filtered_df.dropna(subset=['average_salary'])

    # Group by company and calculate statistics
    salary_analysis = filtered_df.groupby('company')['average_salary'].agg(['mean', 'min', 'max', 'count']).reset_index()

    # Print the salary analysis data
    print("Salary analysis data:")
    print(salary_analysis)

    # Sort by mean salary in descending order
    salary_analysis = salary_analysis.sort_values(by='mean', ascending=False)

    # Save the salary analysis data
    output_salary_analysis_path = 'data/processed/salary_analysis_v2.csv'
    os.makedirs(os.path.dirname(output_salary_analysis_path), exist_ok=True)
    salary_analysis.to_csv(output_salary_analysis_path, index=False)
    print(f'Salary analysis saved to {output_salary_analysis_path}')

    # Create a pivot table for the heatmap
    pivot_table = salary_analysis.pivot_table(
        index='company', 
        values='mean'
    )

    if pivot_table.empty:
        print("The pivot table is empty. Check the data for issues.")
    else:
        # Plotting the heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Average Salary'})
        plt.title('Average Salary for Full Stack Developer Across Companies')
        plt.xlabel('Mean Salary')
        plt.ylabel('Company')

        # Save the heatmap image to a file
        output_image_path = 'data/results/salary_v2.png'
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        plt.savefig(output_image_path, bbox_inches='tight')

        # Show the heatmap
        plt.show()

        print(f'Heatmap saved to {output_image_path}')
