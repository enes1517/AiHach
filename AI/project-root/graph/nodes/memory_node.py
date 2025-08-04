from memory.memory import conversation_chain

def memory_node(state: dict):
    try:
        user_input = state.get("input", "")
        session_id = state.get("session_id", "default")
        category = state.get("filters", {}).get("category", "")
        
        print(f"🧠 Memory node - User input: {user_input}, Category: {category}")
        memory_result = conversation_chain.invoke(
            {"input": user_input, "category": category},  # Kategori bilgisini ekle
            config={"configurable": {"session_id": session_id}}
        )
        
        memory_response = memory_result.get("memory_response", "")
        explanation = memory_result.get("explanation", "")
        
        return {
            **state,
            "memory_response": memory_response,
            "explanation": explanation,
            "category": category  # Kategoriyi state'e taşı
        }
    except Exception as e:
        print(f"❌ Memory node hatası: {e}")
        return {
            **state,
            "memory_response": f"Memory hatası: {str(e)}",
            "explanation": f"Memory hatası: {str(e)}"
        }