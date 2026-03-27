import sqlite3
import pandas as pd

# 1. Load the data we scraped in Step 2
df = pd.read_csv("movies.csv")

# 2. Connect to a SQL database (it will create this file automatically)
connection = sqlite3.connect("movie_data.db")

# 3. Move the data into a SQL table called 'rt_ratings'
df.to_sql("rt_ratings", connection, if_exists="replace", index=False)

print("SQL Database 'movie_data.db' created and populated!")
connection.close()