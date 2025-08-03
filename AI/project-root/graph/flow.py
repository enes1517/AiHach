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
    session_id: Optional[str]  # Session ID eklendi

def create_graph():
    builder = StateGraph(state_schema=AppState)
    
    builder.add_node("Filter", filter_node)
    builder.add_node("Memory", memory_node)         # ✅ Önce Memory
    builder.add_node("Validate", validate_node)
    builder.add_node("Scrape", scrape_node)
    builder.add_node("Check", check_node)
    builder.add_node("Analyze", analyze_node)
    builder.add_node("Explain", explanation_node)
    builder.add_node("Format", formatter_node)
    
    builder.set_entry_point("Filter")
    builder.add_edge("Filter", "Memory")
    builder.add_edge("Memory", "Validate")          # ✅ Memory → Validate
    
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
            "error": END,
            "default": "Analyze"
        }
    )
    
    builder.add_edge("Analyze", "Explain")
    builder.add_edge("Explain", "Format")
    builder.add_edge("Format", END)
    
    return builder.compile()