# memory_node.py - Sadece context tutar, ürün aramasını engellemeez

from memory.memory import conversation_chain, set_last_filters

def memory_node(state: dict):
    try:
        user_input = state.get("input", "")
        session_id = state.get("session_id", "default")
        filters = state.get("filters", {})
        category = filters.get("category", "")

        print(f"🧠 Memory node - User input: {user_input}, Category: {category}")

        # 🔒 En son filtreleri kaydet
        set_last_filters(session_id, filters)

        # ✅ Memory sadece KISA context cevabı versin - ürün aramasını engellemeden
        memory_result = conversation_chain.invoke(
            {"input": user_input, "category": category},
            config={"configurable": {"session_id": session_id}}
        )

        memory_response = memory_result.get("memory_response", "")
        explanation = memory_result.get("explanation", "")

        # ✅ Memory response'u kısalt - UI'da göstermek için
        if len(memory_response) > 100:
            memory_response = memory_response[:100] + "..."

        print(f"💭 Memory kısa cevap: {memory_response}")
        
        return {
            **state,
            "memory_response": memory_response,
            "explanation": explanation,
            "category": category
        }

    except Exception as e:
        print(f"❌ Memory node hatası: {e}")
        return {
            **state,
            "memory_response": "Ürün araması yapılıyor...",  # ✅ Basit fallback
            "explanation": "Ürün araması yapılıyor...",
            "category": filters.get("category", "")
        }