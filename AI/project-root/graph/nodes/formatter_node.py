def formatter_node(state: dict):
    try:
        memory_response = state.get("memory_response", "")
        explanation = state.get("explanation", "")
        result = state.get("result", [])
        
        if isinstance(result, list) and result:
            final_result = result
            print("✅ Analyze result kullanılıyor")
        else:
            final_result = state.get("products", [])
            print("✅ Raw products kullanılıyor")
        
        return {
            **state,
            "result": final_result,
            "memory_response": memory_response,
            "explanation": explanation
        }
    except Exception as e:
        print(f"❌ Formatter node hatası: {e}")
        return {
            **state,
            "result": [],
            "error": f"Formatter hatası: {str(e)}"
        }