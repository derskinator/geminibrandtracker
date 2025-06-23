from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

def scrape_google_ai_overview(query, brand_keywords):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")

    time.sleep(4)  # Wait for AI block to load

    # Try to find AI Overview block — this selector may need tweaking
    try:
        overview_block = driver.find_element(By.XPATH, "//div[contains(text(),'Here’s a summary') or contains(text(),'Here is a summary')]")
        overview_text = overview_block.text
    except:
        overview_text = ""

    driver.quit()

    mentions = [brand for brand in brand_keywords if re.search(rf"\b{re.escape(brand)}\b", overview_text, re.IGNORECASE)]

    return {
        "overview": overview_text,
        "mentions": mentions
    }
