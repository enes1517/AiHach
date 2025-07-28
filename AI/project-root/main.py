from scraper.trendyol_scraper import scrape_trendyol
from filters.product_filter import filter_products
from llm.gemini_suggester import extract_filters_from_prompt

def main():
    user_input = input("🤖 Ne arıyorsun? ")

    print("\n📦 Gemini filtre çıkartıyor...")
    filters = extract_filters_from_prompt(user_input)

    if not filters:
        print("⚠️ Filtre çıkarılamadı.")
        return

    print(f"🔍 Sorgu: {filters['query']}")
    print(f"💰 Maks Fiyat: {filters['max_price']}")
    print(f"🔑 Anahtar Kelimeler: {filters['keywords']}\n")

    print("📡 Trendyol'dan ürünler çekiliyor...")
    products = scrape_trendyol(filters['query'])

    print(f"🔧 Ürün sayısı: {len(products)} - Filtreleniyor...")
    filtered = filter_products(products, max_price=filters["max_price"], keywords=filters["keywords"])

    if not filtered:
        print("❌ Filtreye uyan ürün bulunamadı.")
        return

    print(f"\n🎯 En iyi {min(5, len(filtered))} ürün:")
    for p in filtered[:5]:
        print(f"- {p['name']} - {p['price']} TL")
        print(f"🔗 {p['url']}\n")

if __name__ == "__main__":
    main()
