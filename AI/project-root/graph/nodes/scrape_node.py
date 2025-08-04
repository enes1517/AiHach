from scraper.trendyol_scraper import scrape_trendyol

def scrape_node(state: dict):
    try:
        filters = state.get("filters", {})
        query = filters.get("query", "")
        max_price = filters.get("max_price")
        
        print(f"🕷️ Scraping başlıyor: {query}")
        
        # Scraper çalıştır
        products = scrape_trendyol(query, max_pages=2, max_results=50)
        
        print(f"📦 Scraper sonucu: {len(products)} ürün")
        
        # Fiyat filtresi uygula  
        if max_price and products:
            products = [p for p in products if p.get("price", 0) <= max_price]
            print(f"💰 Fiyat filtresi sonrası: {len(products)} ürün")
        
        return {**state, "products": products}
        
    except Exception as e:
        print(f"❌ Scrape node hatası: {e}")
        return {**state, "products": [], "error": str(e)}