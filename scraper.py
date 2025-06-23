from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

def scrape_google_ai_overview(query, brand_keywords):
    # Setup Chrome options for headless browsing
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    # Initialize the driver
    driver = webdriver.Chrome(options=options)

    # Construct the Google search URL
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)

    # Wait for AI Overview to (hopefully) load
    time.sleep(5)

    # Try to extract all visible text from the page
    try:
        full_page_text = driver.find_element(By.TAG_NAME, "body").text
    except Exception as e:
        full_page_text = ""
        print(f"Error extracting body text: {e}")

    # DEBUG: Print what we captured to logs
    print("---- FULL PAGE TEXT ----")
    print(full_page_text)

    # Look for brand keyword mentions in the captured text
    mentions = []
    for brand in brand_keywords:
        if brand.lower() in full_page_text.lower():
            mentions.append(brand)

    # Clean up
    driver.quit()

    return {
        "overview": full_page_text,
        "mentions": mentions
    }
