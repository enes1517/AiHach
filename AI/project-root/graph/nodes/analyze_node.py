from llm.gemini_suggester import analyze_products_with_gemini

def analyze_node(state: dict):
    """Ürünleri Gemini ile analiz eder"""
    try:
        products = state.get("products", [])
        user_input = state.get("input", "")
        
        if not products:
            return {
                **state,
                "result": [],
                "analysis": "Ürün bulunamadı"
            }
        
        print(f"🧠 Analyze node: {len(products)} ürün analiz ediliyor")
        
        # ✅ Sadece 2 parametre gönder
        analysis_text = analyze_products_with_gemini(products, user_input)
        
        # ✅ PRODUCTS'I döndür, analysis'i ayrı kaydet
        return {
            **state,
            "result": products,  # ← Ürünleri döndür
            "analysis": analysis_text  # ← Analiz metni ayrı
        }
        
    except Exception as e:
        print(f"❌ Analyze node hatası: {e}")
        return {
            **state,
            "result": state.get("products", []),  # Fallback - raw products
            "analysis": f"Analiz hatası: {str(e)}"
        }