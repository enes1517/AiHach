from llm.gemini_suggester import analyze_products_with_gemini

def analyze_node(state: dict):
    return analyze_products_with_gemini(state["products"], state["filters"]["query"])
