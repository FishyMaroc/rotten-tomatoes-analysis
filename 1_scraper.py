from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.add_argument("--headless") # Runs in background
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    URL = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix"
    print("Opening Rotten Tomatoes...")
    driver.get(URL)

    # Wait for the movie tiles to load
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "js-tile-link")))

    # Scroll slightly to ensure everything renders
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(3)

    movie_data = []
    
    # 1. Find all movie containers
    movies = driver.find_elements(By.CLASS_NAME, "js-tile-link")
    print(f"Found {len(movies)} movies. Piercing Shadow DOM for scores...")

    for movie in movies:
        # Get Title (standard element)
        try:
            title = movie.find_element(By.CSS_SELECTOR, "span.p--small").text.strip()
        except:
            title = "Unknown"

        # 2. Get Scores using JavaScript (to bypass the Shadow DOM shown in your screenshot)
        # We target the 'rt-text' elements with specific 'slot' names
        critic = driver.execute_script("""
            return arguments[0].querySelector('rt-text[slot="criticsScore"]')?.innerText;
        """, movie)
        
        audience = driver.execute_script("""
            return arguments[0].querySelector('rt-text[slot="audienceScore"]')?.innerText;
        """, movie)

        movie_data.append({
            "Title": title, 
            "Critic_Score": critic if critic else "N/A", 
            "Audience_Score": audience if audience else "N/A"
        })

    # Save to CSV
    df = pd.DataFrame(movie_data)
    df.to_csv("movies.csv", index=False)
    print("Success! Data saved to movies_final_fixed.csv")

finally:
    driver.quit()