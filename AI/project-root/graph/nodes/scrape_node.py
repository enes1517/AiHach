from scraper.trendyol_scraper import scrape_trendyol

def scrape_node(state: dict):
    filters = state["filters"]
    query = filters.get("query", "")
    max_price = filters.get("max_price")
    products = scrape_trendyol(query)
    if max_price:
        products = [p for p in products if p["price"] <= max_price]
    return {**state, "products": products}
