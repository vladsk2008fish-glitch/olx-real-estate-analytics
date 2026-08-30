import re
import time
import pandas as pd
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Setup Chrome Browser
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

print("Starting browser...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

URL = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/lodz/"
driver.get(URL)

# Wait 5 seconds for page load
time.sleep(5)

# Close cookie consent pop-up if present
try:
    cookie_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_btn.click()
    print("Accepted cookies.")
    time.sleep(2)
except Exception:
    print("No cookie popup found or already accepted.")

# Scroll down gradually to trigger lazy loading
driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, (document.body.scrollHeight / 3) * 2);")
time.sleep(2)

# 2. Extract Listing Cards
# Try finding links to individual offers directly
links = driver.find_elements(By.XPATH, '//a[contains(@href, "/d/oferta/")]')
print(f"Found {len(links)} raw offer links on page.")

data = []
seen_titles = set()

for link in links:
    try:
        title = link.text.strip()
        # Filter out empty or duplicate titles
        if not title or len(title) < 5 or title in seen_titles:
            continue

        # Move to parent elements to get price text
        parent = link
        for _ in range(4):
            parent = parent.find_element(By.XPATH, "..")

        card_text = parent.text

        # Extract price using regex looking for numbers before zł
        price_match = re.search(r'([\d\s]+)\s*zł', card_text)
        if price_match:
            price_clean = re.sub(r"[^\d]", "", price_match.group(1))
            price = float(price_clean) if price_clean else None

            if price and price > 100:  # Filter out unrealistic prices
                seen_titles.add(title)
                data.append({
                    "title": title,
                    "price": price,
                    "location": "Łódź"
                })
    except Exception:
        continue

driver.quit()

df = pd.DataFrame(data)
print(f"Successfully scraped {len(df)} listings from OLX Łódź!")

# 3. Upload to Neon PostgreSQL
if not df.empty:
    DB_URL = "postgresql://neondb_owner:npg_Vt4DHRSPN2Ls@ep-hidden-poetry-b2q1bxzv-pooler.c-6.eu-central-1.aws.neon.tech/olxdata2026?sslmode=require"
    engine = create_engine(DB_URL)

    df.to_sql("raw_olx_houses", con=engine, if_exists="replace", index=False)
    print("Data successfully uploaded to Neon Postgres in table 'raw_olx_houses'!")
else:
    print("No data extracted. Please retry.")