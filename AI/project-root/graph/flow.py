from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict

from graph.nodes.filter_node import filter_node
from graph.nodes.validate_node import validate_node
from graph.nodes.scrape_node import scrape_node
from graph.nodes.check_node import check_node
from graph.nodes.analyze_node import analyze_node

class AppState(TypedDict):
    input: str
    filters: dict
    products: list
    result: str

def create_graph():
    builder = StateGraph(state_schema=AppState)

    builder.add_node("Filter", filter_node)
    builder.add_node("Validate", validate_node)
    builder.add_node("Scrape", scrape_node)
    builder.add_node("Check", check_node)
    builder.add_node("Analyze", analyze_node)

    builder.set_entry_point("Filter")
    builder.add_edge("Filter", "Validate")

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

    builder.add_edge("Analyze", END)

    return builder.compile()
