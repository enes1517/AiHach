from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scroll_to_bottom(driver, pause_time=2, max_scrolls=10):
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)

def scrape_trendyol(query: str, max_pages: int = 1, max_results: int = 100) -> list:
    options = Options()
    # options.add_argument("--headless")  # Görünmez tarayıcı istersen aktif et
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    all_results = []
    page = 1

    while page <= max_pages and len(all_results) < max_results:
        print(f"🔍 Sayfa {page} taranıyor...")
        url = f"https://www.trendyol.com/sr?q={query.replace(' ', '+')}&pi={page}"
        driver.get(url)
        time.sleep(3)
        scroll_to_bottom(driver)

        # ✅ Daha genel ve sağlam selector
        product_cards = driver.find_elements(By.CSS_SELECTOR, "div.p-card-wrppr")

        if not product_cards:
            print("⚠️ Ürün kartları bulunamadı.")
            break

        for wrapper in product_cards:
            try:
                card = wrapper.find_element(By.CSS_SELECTOR, "a.p-card-chldrn-cntnr")

                brand = card.find_element(By.CLASS_NAME, "prdct-desc-cntnr-ttl").text.strip()
                model = card.find_element(By.CLASS_NAME, "prdct-desc-cntnr-name").text.strip()
                description = card.find_element(By.CLASS_NAME, "product-desc-sub-text").text.strip()
                name = f"{brand} {model} {description}"

                try:
                    price_text = card.find_element(By.CLASS_NAME, "price-item").text
                except:
                    price_text = card.find_element(By.CLASS_NAME, "prc-box-dscntd").text
                price = float(price_text.replace("TL", "").replace(".", "").replace(",", ".").strip())

                try:
                    rating = card.find_element(By.CLASS_NAME, "rating-score").text.strip()
                except:
                    rating = "0"

                try:
                    rating_count = card.find_element(By.CLASS_NAME, "ratingCount").text.strip("() ")
                except:
                    rating_count = "0"

                link = card.get_attribute("href")
                if link.startswith("/"):
                    link = "https://www.trendyol.com" + link

                all_results.append({
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "rating_count": rating_count,
                    "link": link
                })

                if len(all_results) >= max_results:
                    break
            except:
                continue

        page += 1

    driver.quit()
    return all_results
