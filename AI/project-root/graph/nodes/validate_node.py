def validate_node(state):
    if not state.get("filters") or not state["filters"].get("query"):
        return {"error": "Filtre boş veya geçersiz."}
    return state
