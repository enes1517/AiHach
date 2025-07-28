from scraper.trendyol_scraper import scrape_trendyol

urunler = scrape_trendyol("bluetooth kulaklık", max_pages=1)

print(f"Toplam ürün: {len(urunler)}")
for u in urunler[:5]:
    print(f"{u['name']} - {u['price']} TL - {u['url']}")
