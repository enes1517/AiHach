# graph/nodes/memory_node.py - Bu dosyayı oluşturun

from memory.memory import conversation_chain

def memory_node(state: dict):
    """
    Hafıza tabanlı cevap üret - önceki konuşmaları hatırla
    """
    try:
        user_input = state.get("input", "")
        session_id = state.get("session_id", "default")
        
        print(f"🧠 Memory node - User input: {user_input}")
        print(f"🧠 Session ID: {session_id}")
        
        # Conversation chain'i session ID ile çalıştır
        memory_result = conversation_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        memory_response = memory_result.get("memory_response", "")
        explanation = memory_result.get("explanation", "")
        
        print(f"🧠 Memory response: {memory_response[:100]}...")
        
        # State'i güncelle
        return {
            **state,
            "memory_response": memory_response,
            "explanation": explanation
        }
        
    except Exception as e:
        print(f"❌ Memory node hatası: {e}")
        return {
            **state,
            "memory_response": "",
            "explanation": f"Memory hatası: {str(e)}"
        }