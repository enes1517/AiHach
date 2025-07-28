import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict

def scrape_trendyol(query: str, max_pages: int = 3, max_results: int = 100) -> List[Dict]:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    base_url = "https://www.trendyol.com/sr?q="
    query_param = query.replace(' ', '+')
    
    all_products = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}{query_param}&pi={page}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            product_anchors = soup.select("a.p-card-chldrn-cntnr")

            for a in product_anchors:
                if len(all_products) >= max_results:
                    break
                try:
                    name = a.select_one("span.product-title")
                    price = a.select_one(".prc-box-sllng")

                    if not name or not price:
                        continue

                    name_text = name.text.strip()
                    price_text = price.text.strip()
                    price_val = float(re.findall(r"\d+\.\d+", price_text.replace(".", "").replace(",", "."))[0])
                    url = "https://www.trendyol.com" + a["href"]

                    all_products.append({
                        "name": name_text,
                        "price": price_val,
                        "url": url
                    })
                except Exception as e:
                    print("⚠️ Kart okunamadı:", e)
        except Exception as e:
            print(f"❌ Sayfa alınamadı {page}: {e}")
            continue

    return all_products
