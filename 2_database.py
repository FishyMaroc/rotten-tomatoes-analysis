import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# --- SECTION 1: DATABASE ---
# I'm loading the movie data I scraped into a Pandas "table"
df = pd.read_csv("movies.csv")

# This creates a SQL database file so the data is stored more officially
connection = sqlite3.connect("movie_data.db")
df.to_sql("rt_ratings", connection, if_exists="replace", index=False)
print("✅ SQL Database created!")
connection.close()


# --- SECTION 2: THE GRAPH ---
# 1. Cleaning the scores so they are numbers I can actually graph
df['Critic_Score'] = pd.to_numeric(df['Critic_Score'], errors='coerce').fillna(0)

# 2. Sorting to find the Top 10 movies
top_10 = df.sort_values(by='Critic_Score', ascending=False).head(10)

# 3. Setting up the style. I chose 'dark_background' because it looks modern.
plt.style.use('dark_background') 
fig, ax = plt.subplots(figsize=(10, 6))

# 4. Drawing the bars using a nice red color (Rotten Tomatoes red!)
bars = ax.barh(top_10['Title'], top_10['Critic_Score'], color='#fa320a')

# 5. Adding the actual percentage text at the end of each bar
# This makes it so people don't have to guess the score.
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{int(width)}%', va='center', fontweight='bold')

# 6. Making the chart look "clean" by removing the extra border lines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.invert_yaxis() # This puts the #1 movie at the top

# 7. Final Touches: Title and saving the high-quality image
ax.set_title('🏆 Top 10 Netflix Movies (By Critic Score)', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('movie_chart.png', dpi=300) # dpi=300 makes it look very sharp

print("🎨 Your advanced chart is saved!")