from typing import List, Dict, Optional

def filter_products(products: List[Dict], max_price: Optional[float] = None, keywords: Optional[List[str]] = None) -> List[Dict]:
    filtered = []
    for product in products:
        try:
            price_str = product["price"].replace("TL", "").replace(".", "").replace(",", ".").strip()
            price = float(price_str)
        except:
            continue

        if max_price is not None and price > max_price:
            continue

        if keywords:
            title_lower = product["title"].lower()
            if not any(kw.lower() in title_lower for kw in keywords):
                continue

        product["numeric_price"] = price
        filtered.append(product)

    return filtered
