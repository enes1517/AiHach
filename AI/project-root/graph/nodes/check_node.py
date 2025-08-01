def check_node(state: dict):
    if not state.get("products"):
        return {"error": "Ürün bulunamadı"}
    return state
