# graph/nodes/formatter_node.py - Memory ile uyumlu formatter

def formatter_node(state: dict):
    """
    Final sonucu formatla - memory response ve ürünleri birleştir
    """
    try:
        memory_response = state.get("memory_response", "")
        explanation = state.get("explanation", "")
        products = state.get("products", [])
        analysis_result = state.get("result", [])
        
        print(f"📝 Formatter - Memory response: {bool(memory_response)}")
        print(f"📝 Formatter - Products: {len(products)}")
        print(f"📝 Formatter - Analysis result: {len(analysis_result) if isinstance(analysis_result, list) else bool(analysis_result)}")
        
        # Eğer analyze node'dan sonuç varsa onu kullan
        if isinstance(analysis_result, list) and analysis_result:
            final_result = analysis_result
            print("✅ Analyze result kullanılıyor")
        elif products:
            # Eğer sadece products varsa onu kullan
            final_result = products
            print("✅ Raw products kullanılıyor")
        else:
            final_result = []
            print("❌ Hiç ürün yok")
        
        # Final state'i hazırla
        final_state = {
            **state,
            "result": final_result,
            "memory_response": memory_response,
            "explanation": explanation
        }
        
        print(f"📤 Final result: {len(final_result)} ürün")
        print(f"📤 Memory response: {memory_response[:50]}..." if memory_response else "📤 Memory response: YOK")
        
        return final_state
        
    except Exception as e:
        print(f"❌ Formatter node hatası: {e}")
        return {
            **state,
            "result": [],
            "error": f"Formatter hatası: {str(e)}"
        }