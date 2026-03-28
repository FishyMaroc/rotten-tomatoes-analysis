from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# --- STEP 1: THE SHOPPER (SCRAPING) ---
options = Options()
options.add_argument("--headless") 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    URL = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix"
    print("🚀 Opening Rotten Tomatoes...")
    driver.get(URL)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "js-tile-link")))
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(3)

    movie_data = []
    movies = driver.find_elements(By.CLASS_NAME, "js-tile-link")
    print(f"📦 Found {len(movies)} movies. Extracting data...")

    for movie in movies:
        try:
            title = movie.find_element(By.CSS_SELECTOR, "span.p--small").text.strip()
        except:
            title = "Unknown"

        critic = driver.execute_script("return arguments[0].querySelector('rt-text[slot=\"criticsScore\"]')?.innerText;", movie)
        audience = driver.execute_script("return arguments[0].querySelector('rt-text[slot=\"audienceScore\"]')?.innerText;", movie)

        movie_data.append({
            "Title": title, 
            "Critic_Score": critic.replace('%', '') if critic else "0", 
            "Audience_Score": audience.replace('%', '') if audience else "0"
        })

    # Save to CSV
    df = pd.DataFrame(movie_data)
    df.to_csv("movies.csv", index=False)
    print("✅ Success! Data saved to movies.csv")

    # --- STEP 2: THE CHEF (ANALYSIS) ---
    print("\n📊 --- ANALYSIS REPORT ---")
    
    # Convert scores to numbers so we can do math
    df['Critic_Score'] = pd.to_numeric(df['Critic_Score'], errors='coerce').fillna(0)
    
    # Find the movie with the highest critic score
    top_movie = df.loc[df['Critic_Score'].idxmax()]
    
    print(f"The highest rated movie is: {top_movie['Title']} with a {top_movie['Critic_Score']}%!")
    print(f"Average Critic Score for Netflix movies: {df['Critic_Score'].mean():.1f}%")
    print("---------------------------\n")

finally:
    driver.quit()