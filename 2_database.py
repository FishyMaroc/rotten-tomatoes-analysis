import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


# 1. Load the data we scraped in Step 2
df = pd.read_csv("movies.csv")

# 2. Connect to a SQL database (it will create this file automatically)
connection = sqlite3.connect("movie_data.db")

# 3. Move the data into a SQL table called 'rt_ratings'
df.to_sql("rt_ratings", connection, if_exists="replace", index=False)

print("SQL Database 'movie_data.db' created and populated!")
connection.close()

# Load the data
df = pd.read_csv('movies.csv')

# Clean the scores (remove % and make them numbers)
df['Critic_Score'] = pd.to_numeric(df['Critic_Score'].str.replace('%', ''), errors='coerce')

# Sort by top 10 movies
top_10 = df.sort_values(by='Critic_Score', ascending=False).head(10)

# Create the Chart
plt.figure(figsize=(10, 6))
plt.barh(top_10['Title'], top_10['Critic_Score'], color='tomato')
plt.xlabel('Critic Score (%)')
plt.title('Top 10 Netflix Movies on Rotten Tomatoes')
plt.gca().invert_yaxis() # Put the #1 movie at the top

# Save the picture!
plt.savefig('movie_chart.png')
print("🎨 Chart saved as movie_chart.png!")