# from llm.gemini_suggester import extract_filters_from_prompt, analyze_products_with_gemini
# from scraper.trendyol_scraper import scrape_trendyol

# def main():
#     user_input = input("🧠 Ne istiyorsun? (örnek: 3000 TL altı kulaklık arıyorum): ")

#     filters = extract_filters_from_prompt(user_input)
#     if not filters:
#         print("🚫 Anlamsız sorgu. Lütfen daha açık bir istek girin.")
#         return

#     print(f"🎯 Gemini'den filtreler alındı: {filters}")

#     query = filters.get("query", "")
#     max_price = filters.get("max_price", None)

#     print(f"📦 Trendyol'a gönderilen arama terimi: '{query}'")
#     print(f"💰 Fiyat filtresi: {max_price or 'Belirtilmedi'} TL")

#     products = scrape_trendyol(query)
#     if not products:
#         print("❌ Ürün bulunamadı.")
#         return

#     result = analyze_products_with_gemini(products, user_input)
#     print("\n🤖 Öneri:")
#     print(result)

# if __name__ == "__main__":
#     main()



from graph.flow import create_graph

def main():
    user_input = input("🧠 Ne istiyorsun? (örnek: 3000 TL altı kulaklık arıyorum): ")
    graph = create_graph()
    result = graph.invoke({"input": user_input})

    if isinstance(result, str):
        print("\n🤖 Öneri:")
        print(result)
    elif isinstance(result, dict) and result.get("error"):
        print(f"🚫 {result['error']}")
    else:
        print("⚠️ Beklenmeyen çıktı:", result)

if __name__ == "__main__":
    main()
