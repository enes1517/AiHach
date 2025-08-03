def formatter_node(state: dict):
    products = state.get("products", [])
    explanations = state.get("explanations", [])
    
    if not products:
        return {
            **state,
            "result": []
        }
    
    formatted = []
    for i, product in enumerate(products):
        # Ürün field mapping düzeltmesi - products'ta 'name' var, 'title' değil
        explanation = explanations[i] if i < len(explanations) else "Bu ürün bütçenize uygun bulundu."
        
        formatted.append({
            "title": product.get("name", product.get("title", "Bilinmeyen ürün")),  # name -> title
            "price": product.get("price"),
            "link": product.get("link"),
            "image": product.get("image", None),
            "why_recommended": explanation
        })
    
    return {
        **state,
        "result": formatted
    }