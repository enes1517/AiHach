from llm.gemini_suggester import explain_recommendation

def explanation_node(state: dict):
    try:
        products = state.get("products", [])
        user_input = state.get("input", "")
        
        if not products:
            return {
                **state,
                "explanations": [],
                "error": "Ürün bulunamadı"
            }
        
        # explain_recommendation fonksiyonuna user_input de gönder
        explanations = explain_recommendation(products, user_input)
        
        # Eğer explanations liste değilse veya boşsa, default açıklamalar oluştur
        if not isinstance(explanations, list) or len(explanations) == 0:
            explanations = [
                "Bu ürün fiyat ve özellikler açısından uygun bulundu." 
                for _ in products
            ]
        
        # Liste uzunluğunu eşitle
        while len(explanations) < len(products):
            explanations.append("Bu ürün bütçenize uygun bulundu.")
            
        return {
            **state,
            "explanations": explanations
        }
        
    except Exception as e:
        print(f"❌ Explanation node hatası: {e}")
        # Fallback - her ürün için basit açıklama
        products = state.get("products", [])
        fallback_explanations = [
            "Bu ürün analiz edildi ve uygun bulundu." 
            for _ in products
        ]
        return {
            **state,
            "explanations": fallback_explanations
        }