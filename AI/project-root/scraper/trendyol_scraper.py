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
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    all_results = []
    
    for page in range(1, max_pages + 1):
        print(f"🔍 Sayfa {page} taranıyor...")
        
        # ✅ URL düzeltmesi
        url = f"https://www.trendyol.com/sr?q={query.replace(' ', '%20')}&pi={page}"
        print(f"🌐 URL: {url}")
        
        driver.get(url)
        time.sleep(4)  # Biraz daha bekle
        
        # ✅ Güncel selector'lar - farklı seçenekleri dene
        selectors = [
            "div.p-card-wrppr",
            "div[data-testid='product-card']", 
            "div.product-item",
            ".p-card-chldrn-cntnr"
        ]
        
        product_cards = []
        for selector in selectors:
            product_cards = driver.find_elements(By.CSS_SELECTOR, selector)
            if product_cards:
                print(f"✅ Selector çalıştı: {selector} ({len(product_cards)} ürün)")
                break
        
        if not product_cards:
            print("❌ Hiçbir selector çalışmadı")
            continue
            
        for card in product_cards[:max_results]:
            try:
                # İsim çıkarma - çoklu selector
                name = ""
                name_selectors = [
                    ".prdct-desc-cntnr-name",
                    "[data-testid='product-name']",
                    ".product-name",
                    ".p-card-wrppr .name"
                ]
                
                for sel in name_selectors:
                    try:
                        name_elem = card.find_element(By.CSS_SELECTOR, sel)
                        name = name_elem.text.strip()
                        if name:
                            break
                    except:
                        continue
                
                if not name:
                    continue
                
                # Fiyat çıkarma
                price = 0
                price_selectors = [
                    ".prc-box-dscntd",
                    ".price-item", 
                    "[data-testid='price-current-price']"
                ]
                
                for sel in price_selectors:
                    try:
                        price_elem = card.find_element(By.CSS_SELECTOR, sel)
                        price_text = price_elem.text
                        price = float(price_text.replace("TL", "").replace(".", "").replace(",", ".").strip())
                        break
                    except:
                        continue
                
                # Link çıkarma
                try:
                    link_elem = card.find_element(By.CSS_SELECTOR, "a")
                    link = link_elem.get_attribute("href")
                    if not link.startswith("http"):
                        link = f"https://www.trendyol.com{link}"
                except:
                    link = ""
                
                # Resim URL - BONUS
                image_url = ""
                try:
                    img_elem = card.find_element(By.CSS_SELECTOR, "img")
                    image_url = img_elem.get_attribute("src")
                except:
                    pass
                
                all_results.append({
                    "name": name,
                    "price": price,
                    "rating": "0",
                    "rating_count": "0", 
                    "link": link,
                    "image": image_url  # ✅ Resim eklendi
                })
                
                if len(all_results) >= max_results:
                    break
                    
            except Exception as e:
                print(f"⚠️ Ürün parse hatası: {e}")
                continue
    
    driver.quit()
    print(f"🎯 Toplam {len(all_results)} ürün çekildi")
    return all_results