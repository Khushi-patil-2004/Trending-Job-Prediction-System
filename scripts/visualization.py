import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

# # Create the directory if it doesn't exist
# if not os.path.exists('data/results'):
#     os.makedirs('data/results')

# Load the data
df = pd.read_csv('data/processed/cleaned_with_date.csv')

# Ensure the date column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Extract year-month from the date column
df['year_month'] = df['date'].dt.to_period('M').astype(str)  # Convert to string for Plotly

# Group by year-month and job title to count occurrences
job_trends = df.groupby(['year_month', 'positionName']).size().reset_index(name='count')

# Find the top 10 job titles by total occurrences
top_titles = job_trends.groupby('positionName')['count'].sum().nlargest(10).index

# Filter the job_trends DataFrame to include only the top 10 job titles
top_job_trends = job_trends[job_trends['positionName'].isin(top_titles)]

# Create a vertical bar graph with Plotly
def plot_top_trending_jobs_bar(df, save_path=None):
    # Create a vertical bar plot
    fig = px.bar(
        df,
        x='year_month',
        y='count',
        color='positionName',
        title='Top 10 Trending Jobs Over Time',
        labels={'year_month': 'Year-Month', 'count': 'Number of Postings'},
        barmode='stack'  # Stack bars to show trends over time
    )
    
    fig.update_layout(
        xaxis_title='Year-Month',
        yaxis_title='Number of Postings',
        legend_title='Job Titles',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        hovermode='x unified'
    )
    
    # Show the plot
    fig.show()
    
    # Save the plot as a PNG file if save_path is provided
    if save_path:
        pio.write_image(fig, save_path, format='png')
        print(f'Saved bar chart as {save_path}')

# Specify the path where you want to save the bar chart
save_path = 'data/results/trending_job_titles_over_time.png'

# Plot the top 10 trending jobs as a vertical bar graph and save it
plot_top_trending_jobs_bar(top_job_trends, save_path)
