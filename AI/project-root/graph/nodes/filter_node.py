# filter_node.py - Önceki kategoriyi korur ve follow-up soruları doğru parse eder

from llm.gemini_suggester import extract_filters_from_prompt
from memory.memory import get_last_filters
import re

def filter_node(state: dict):
    user_input = state["input"]
    session_id = state.get("session_id", "default")
    
    print(f"🔍 Filter node - Input: {user_input}")
    
    # Önceki filtreleri al
    last_filters = get_last_filters(session_id)
    last_category = last_filters.get("category", "")
    last_query = last_filters.get("query", "")
    
    print(f"📚 Önceki context - Category: {last_category}, Query: {last_query}")
    
    # ✅ Follow-up sorularını tespit et
    follow_up_indicators = [
        "bunlardan", "bunların", "onlardan", "şunlardan",
        "daha ucuz", "daha pahalı", "ucuz olan", "pahalı olan",
        "kaliteli", "en iyi", "önerilen", "hangi"
    ]
    
    is_follow_up = any(indicator in user_input.lower() for indicator in follow_up_indicators)
    
    if is_follow_up and last_category:
        print(f"✅ Follow-up soru tespit edildi! Önceki kategori: {last_category}")
        
        # Fiyat aralığı var mı?
        price_match = re.search(r'(\d+)\s*(?:bin|000)?\s*(?:tl?)?\s*(?:den|dan|altı|altında|üstü|üstünde)', user_input.lower())
        if price_match:
            price_value = int(price_match.group(1))
            # "bin" kelimesi varsa veya 4 haneden az ise 1000 ile çarp
            if "bin" in user_input.lower() or price_value < 1000:
                price_value *= 1000
            max_price = price_value
            print(f"💰 Fiyat filtresi bulundu: {max_price} TL")
        else:
            max_price = None
        
        # ✅ Önceki kategori ile birleştir
        enhanced_query = f"{last_category} {user_input}".strip()
        
        filters = {
            "query": enhanced_query,
            "max_price": max_price,
            "category": last_category  # ✅ Kategoriyi koru
        }
        
        print(f"🔄 Follow-up filters: {filters}")
        
    else:
        # Normal yeni arama
        filters = extract_filters_from_prompt(user_input)
        
        if filters is None:
            # Fallback - basit parse
            price_match = re.search(r'(\d+)\s*(?:bin|000|tl)', user_input.lower())
            if price_match:
                max_price = int(price_match.group(1))
                if max_price < 1000:
                    max_price *= 1000
            else:
                max_price = None
            
            filters = {
                "query": user_input,
                "max_price": max_price,
                "category": ""
            }
            print(f"⚠️ Filter fallback kullanıldı: {filters}")
        else:
            print(f"✅ Normal filters çıkarıldı: {filters}")
    
    return {**state, "filters": filters}