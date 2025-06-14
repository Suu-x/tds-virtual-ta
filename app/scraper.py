import requests
from bs4 import BeautifulSoup
import json
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By                          # ✅ Add this
from selenium.webdriver.support.ui import WebDriverWait              # ✅ Add this
from selenium.webdriver.support import expected_conditions as EC 


# --- Discourse Scraper ---
def scrape_discourse():
    print("🔍 Scraping Discourse with Selenium...")

    base_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(base_url)

    try:
        # Wait for the topic list container to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.topic-list"))
        )
    except Exception as e:
        driver.save_screenshot("discourse_page.png")
        print("⚠️ Timeout waiting for topic list. Screenshot saved as 'discourse_page.png'")
        driver.quit()
        return

    # Extract thread links
    links = []
    threads = driver.find_elements(By.CSS_SELECTOR, "a.title")
    for a in threads:
        href = a.get_attribute("href")
        if href and "/t/" in href and href not in links:
            links.append(href)

    print(f"🔗 Found {len(links)} thread links.")

    posts = []
    for url in links:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "p"))
            )
            title = driver.title.strip()
            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            content = " ".join(p.text for p in paragraphs)
            posts.append({
                "url": url,
                "title": title,
                "content": content
            })
        except Exception as e:
            print(f"⚠️ Error scraping {url}: {e}")
            continue

    with open("data/discourse_data.json", "w", encoding='utf-8') as f:
        json.dump(posts, f, indent=2)

    driver.quit()
    print(f"✅ Scraped {len(posts)} Discourse threads and saved to data/discourse_data.json")


# --- Course Notes Scraper ---
def scrape_course():
    print("📘 Scraping Course Notes (JavaScript-rendered)...")
    url = "https://tds.s-anand.net/#/2025-01/"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # allow JavaScript to load

    body_text = driver.find_element("tag name", "body").text

    course_data = [
        {
            "title": "TDS Course Notes",
            "content": body_text
        }
    ]

    with open("data/course_data.json", "w", encoding='utf-8') as f:
        json.dump(course_data, f, indent=2)

    driver.quit()
    print("✅ Course notes saved to data/course_data.json")


# --- Run Both ---
if __name__ == "__main__":
    scrape_discourse()
    scrape_course()
