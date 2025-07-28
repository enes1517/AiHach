
from typing import List, Dict, Optional

def filter_products(products: List[Dict], max_price: Optional[float] = None, keywords: Optional[List[str]] = None) -> List[Dict]:
    filtered = []
    for product in products:
        if max_price is not None and product["price"] > max_price:
            continue
        if keywords:
            name_lower = product["name"].lower()
            if not any(kw.lower() in name_lower for kw in keywords):
                continue
        filtered.append(product)
    return filtered
