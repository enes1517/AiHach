from llm.gemini_suggester import extract_filters_from_prompt
from memory.memory import get_last_filters

def filter_node(state: dict):
    user_input = state["input"]
    session_id = state.get("session_id", "default")
    
    # Yeni filtreler çıkar
    filters = extract_filters_from_prompt(user_input)
    
    if filters is None:
        # Önceki filtreleri al
        last_filters = get_last_filters(session_id)
        last_category = last_filters.get("category", "")
        
        # Fiyat sorusu mu?
        import re
        price_match = re.search(r'(\d+)\s*tl?\s*(altı|altında)', user_input.lower())
        if price_match:
            max_price = int(price_match.group(1))
            query = last_category if last_category else user_input
        else:
            max_price = None
            query = f"{last_category} {user_input}".strip() if last_category else user_input
        
        filters = {
            "query": query,
            "max_price": max_price,
            "category": last_category
        }
        print(f"⚠️ Filter fallback kullanıldı: {filters}")
    
    return {**state, "filters": filters}