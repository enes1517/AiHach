from scraper.trendyol_scraper import scrape_trendyol
from llm.gemini_suggester import extract_filters_from_prompt, analyze_products_with_gemini
import re

def main():
    user_input = input("🧠 Ne istiyorsun? (örnek: 3000 TL altı kulaklık arıyorum): ")

    filters = extract_filters_from_prompt(user_input)
    print(f"\n🎯 Gemini'den filtreler alındı: {filters}")

    query = filters.get("query", user_input).lower().strip()
    max_price = filters.get("max_price", None)

    # ❗ Query içinden fiyat ifadesini çıkar, sadece ürün türünü bırak (örnek: "kulaklık")
    match = re.search(r"(?:\d+\s*TL\s*(?:altı|üstü)?\s*)?(.*)", query, flags=re.IGNORECASE)
    if match:
        query = match.group(1).strip()

    print(f"📦 Trendyol'a gönderilen arama terimi: '{query}'")
    print(f"💰 Fiyat filtresi: {max_price} TL")

    all_products = scrape_trendyol(query, max_pages=2, max_results=100)

    if not all_products:
        print("❌ Ürün bulunamadı.")
        return

    # 🔻 Fiyat filtresi uygula
    if max_price:
        all_products = [p for p in all_products if p["price"] <= max_price]

    if not all_products:
        print("❌ Fiyat filtresinden sonra ürün kalmadı.")
        return

    print(f"✅ {len(all_products)} ürün bulundu. Gemini’ye gönderiliyor...\n")

    response = analyze_products_with_gemini(all_products, user_input)
    print("📋 Gemini Cevabı:\n")
    print(response)

if __name__ == "__main__":
    main()
