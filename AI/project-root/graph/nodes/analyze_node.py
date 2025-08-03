from llm.gemini_suggester import analyze_products_with_gemini

def analyze_node(state: dict):
    """
    Ürünleri Gemini ile analiz eder ve sonucu state'e ekler
    """
    try:
        products = state.get("products", [])
        user_input = state.get("input", "")
        
        # Gemini ile analiz yap
        analysis_result = analyze_products_with_gemini(products, user_input)
        
        # ✅ DICT döndür, string değil!
        return {
            **state,
            "result": analysis_result,  # Analiz sonucunu result'a kaydet
            "analysis": analysis_result  # Ek olarak analysis field'ına da kaydet
        }
        
    except Exception as e:
        print(f"❌ Analyze node hatası: {e}")
        return {
            **state,
            "result": f"Analiz hatası: {str(e)}",
            "error": str(e)
        }