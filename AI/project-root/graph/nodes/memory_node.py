# graph/nodes/memory_node.py - Session ID desteği ile
from memory.memory import conversation_chain

def memory_node(state: dict):
    """
    Kullanıcının geçmiş tercihlerini analiz eder ve hafıza response'u üretir
    """
    try:
        user_input = state.get("input", "")
        
        # 🆔 Session ID'yi state'den al, yoksa default kullan
        session_id = state.get("session_id", "default-user")
        
        # Conversation chain'i session ID ile çalıştır
        response = conversation_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        # 🧠 Eğer LLM cevabı string ise dict'e sar
        if isinstance(response, str):
            return {
                **state,
                "memory_response": response,
                "explanation": response,
                "session_id": session_id  # Session ID'yi koru
            }
        
        # 🧠 Eğer dict ise, gerekli alanları state'e doğrudan yaz
        if isinstance(response, dict):
            return {
                **state,
                "memory_response": response.get("memory_response", ""),
                "explanation": response.get("explanation", ""),
                "session_id": session_id  # Session ID'yi koru
            }
        
        # 🔚 Diğer tüm türler için fallback
        return {
            **state,
            "memory_response": str(response),
            "explanation": str(response),
            "session_id": session_id  # Session ID'yi koru
        }
        
    except Exception as e:
        print(f"❌ Memory node hatası: {e}")
        return {
            **state,
            "memory_response": f"Hafıza hatası: {str(e)}",
            "explanation": f"Hafıza hatası: {str(e)}",
            "session_id": state.get("session_id", "default-user")  # Session ID'yi koru
        }