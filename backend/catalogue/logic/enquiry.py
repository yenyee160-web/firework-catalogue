"""Pure price calculation. The browser never supplies trusted prices."""
from urllib.parse import quote

MAX_LINES = 20
MAX_QUANTITY = 25

def build_enquiry(items, products, number):
    if not isinstance(items, list) or not 1 <= len(items) <= MAX_LINES:
        raise ValueError("Choose between 1 and 20 products")
    lookup = {item["id"]: item for item in products}
    seen = set()
    lines = ["Hello! I would like to enquire about these catalogue items:"]
    total_sen = 0
    summary = []
    for entry in items:
        if not isinstance(entry, dict):
            raise ValueError("Each cart entry must be an object")
        product_id, quantity = entry.get("id"), entry.get("quantity")
        if not isinstance(product_id, str) or product_id not in lookup:
            raise ValueError("Unknown product")
        if product_id in seen:
            raise ValueError("Duplicate product")
        if type(quantity) is not int or not 1 <= quantity <= MAX_QUANTITY:
            raise ValueError("Quantity must be an integer between 1 and 25")
        product = lookup[product_id]
        if not product["available"]:
            raise ValueError("Product is unavailable")
        seen.add(product_id)
        line_total = product["price_sen"] * quantity
        total_sen += line_total
        summary.append({"id": product_id, "quantity": quantity, "line_total_sen": line_total})
        lines.append(f"- {product['name']} x{quantity}: RM {line_total / 100:.2f}")
    lines.extend([f"Estimated total: RM {total_sen / 100:.2f}",
                  "This is an enquiry only. No order is placed or payment taken.",
                  "Please confirm availability, eligibility and applicable regulations."])
    message = "\n".join(lines)
    return {
        "url": f"https://wa.me/{number}?text={quote(message, safe='')}",
        "total_sen": total_sen,
        "currency": "MYR",
        "items": summary,
    }
