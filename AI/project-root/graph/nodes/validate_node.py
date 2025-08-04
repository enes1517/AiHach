def validate_node(state):
    filters = state.get("filters")
    
    # ✅ Daha güvenli kontrol
    if not filters:
        print("❌ Filters boş")
        return {**state, "error": "Filtre boş"}
    
    query = filters.get("query", "").strip()
    if not query:
        print("❌ Query boş") 
        return {**state, "error": "Arama sorgusu boş"}
    
    print(f"✅ Validation başarılı: {query}")
    return state