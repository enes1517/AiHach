from llm.gemini_suggester import analyze_products_with_gemini

def analyze_node(state: dict):
    try:
        products = state.get("products", [])
        user_input = state.get("input", "")
        category = state.get("category", "")
        
        analysis_result = analyze_products_with_gemini(products, user_input, category)
        
        return {
            **state,
            "result": analysis_result,
            "analysis": analysis_result
        }
    except Exception as e:
        print(f"❌ Analyze node hatası: {e}")
        return {
            **state,
            "result": [],
            "error": str(e)
        }