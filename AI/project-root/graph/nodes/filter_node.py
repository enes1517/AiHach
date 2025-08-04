from llm.gemini_suggester import extract_filters_from_prompt

def filter_node(state: dict):
    user_input = state["input"].lower()
    filters = extract_filters_from_prompt(user_input)
    
    if filters is None:
        # Kategori tahmini
        category_map = {
            "televizyon": "televizyon",
            "tv": "televizyon",
            "laptop": "laptop",
            "telefon": "telefon",
            # ... (diğer kategoriler eklenebilir)
        }
        category = next((cat for cat in category_map.keys() if cat in user_input), "")
        filters = {
            "query": user_input,
            "max_price": None,
            "category": category_map.get(category, "")
        }
        print(f"⚠️ Filter fallback ile kategori tahmini: {filters}")
    
    return {**state, "filters": filters}