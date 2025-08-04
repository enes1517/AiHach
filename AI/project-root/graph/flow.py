# graph/flow.py - Session ID desteği ile güncellenmiş

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Optional

from graph.nodes.memory_node import memory_node
from graph.nodes.filter_node import filter_node
from graph.nodes.validate_node import validate_node
from graph.nodes.scrape_node import scrape_node
from graph.nodes.check_node import check_node
from graph.nodes.analyze_node import analyze_node
from graph.nodes.explanation_node import explanation_node
from graph.nodes.formatter_node import formatter_node

class AppState(TypedDict):
    input: str
    filters: dict
    products: list
    result: str
    memory_response: str
    explanation: str
    session_id: Optional[str]
    category: Optional[str]

def should_continue_with_search(state: AppState) -> str:
    memory_response = state.get("memory_response", "")
    user_input = state.get("input", "").lower()
    category = state.get("category", "")
    
    print(f"🤔 Should continue check - Category: {category}")
    if category and any(keyword in user_input for keyword in ["öner", "göster", "alınır"]):
        print("➡️ Kategori ve ürün talebi var, aramaya devam")
        return "validate"
    if any(indicator in memory_response.lower() for indicator in ["arama", "arıyorum"]):
        print("➡️ Memory'de arama belirteci var, aramaya devam")
        return "validate"
    print("➡️ Memory cevabı yeterli")
    return "end"

def create_graph():
    builder = StateGraph(state_schema=AppState)
    
    # Node'ları ekle
    builder.add_node("Filter", filter_node)
    builder.add_node("Memory", memory_node)         # ✅ Memory node eklendi
    builder.add_node("Validate", validate_node)
    builder.add_node("Scrape", scrape_node)
    builder.add_node("Check", check_node)
    builder.add_node("Analyze", analyze_node)
    builder.add_node("Explain", explanation_node)
    builder.add_node("Format", formatter_node)
    
    # Entry point
    builder.set_entry_point("Filter")
    
    # Filter → Memory (her zaman önce memory kontrol et)
    builder.add_edge("Filter", "Memory")
    
    # Memory'den sonra karar ver: arama yap mı yoksa bitir mi?
    builder.add_conditional_edges(
        "Memory",
        should_continue_with_search,
        {
            "validate": "Validate",  # Aramaya devam et
            "end": "Format"          # Memory'den cevap yeterli, direkt formatla
        }
    )
    
    # Arama flow'u (önceki gibi)
    builder.add_conditional_edges(
        "Validate",
        RunnableLambda(
            lambda state: "error" if not state.get("filters") or not state["filters"].get("query") else "default",
            name="validate_condition"
        ),
        {
            "error": END,
            "default": "Scrape"
        }
    )
    
    builder.add_edge("Scrape", "Check")
    
    builder.add_conditional_edges(
        "Check",
        RunnableLambda(
            lambda state: "error" if not state.get("products") else "default",
            name="check_condition"
        ),
        {
            "error": "Format",  # Ürün bulunamasa bile format'a git (memory cevabı varsa)
            "default": "Analyze"
        }
    )
    
    builder.add_edge("Analyze", "Explain")
    builder.add_edge("Explain", "Format")
    builder.add_edge("Format", END)
    
    return builder.compile()

# Test fonksiyonu
def test_memory_flow():
    """Memory flow'unu test et"""
    graph = create_graph()
    
    test_cases = [
        ("laptop öner", "İlk ürün arama"),
        ("daha ucuz olanları göster", "Follow-up soru"),
        ("hangi markaları var?", "Marka sorusu"),
        ("kulaklık arıyorum", "Yeni ürün türü")
    ]
    
    session_id = "test-memory-123"
    
    for user_input, description in test_cases:
        print(f"\n{'='*60}")
        print(f"🧪 Test: {description}")
        print(f"📝 Input: {user_input}")
        print('='*60)
        
        try:
            result = graph.invoke({
                "input": user_input,
                "session_id": session_id
            })
            
            print(f"📤 Memory Response: {result.get('memory_response', 'YOK')}")
            print(f"📤 Products: {len(result.get('result', []))} ürün" if isinstance(result.get('result'), list) else f"📤 Result: {result.get('result', 'YOK')}")
            
        except Exception as e:
            print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_memory_flow()