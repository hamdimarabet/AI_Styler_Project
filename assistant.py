from recommender import get_recommendations
from shopify_api import get_products_by_tags  # your Shopify API code

def format_products(items):
    if not items:
        return "No recommendations available"
    # If Shopify products (dicts with title & url)
    if isinstance(items[0], dict) and "title" in items[0]:
        return "\n".join(f"{p['title']} - {p['price']} {p['currency']} ({p.get('url', 'no link')})" for p in items)
    # Otherwise, plain text
    return ", ".join(items)

def chat_with_assistant(user_message, morphotype, head_shape):
    event = None
    if "wedding" in user_message.lower():
        event = "wedding"
    elif "beach" in user_message.lower():
        event = "beach"
    elif "business" in user_message.lower():
        event = "business"

    # Get the initial recommendations from your rules
    recs = get_recommendations(morphotype, head_shape, event)

    # For each category (clothing, event_style), fetch actual Shopify products
    shopify_products = {}
    for key in ["clothing", "event_style"]:
        if key in recs:
            shopify_products[key] = []
            for tag in recs[key]:
                products = get_products_by_tags([tag])
                shopify_products[key].extend(products)

    response = f"Based on your body type ({morphotype}) and head shape ({head_shape}), I suggest:\n"
    if "clothing" in shopify_products:
        response += f"- Clothing:\n{format_products(shopify_products['clothing'])}\n"
    if "glasses" in recs:
        response += f"- Glasses: {format_products(recs['glasses'])}\n"
    if event and "event_style" in shopify_products:
        response += f"- For {event}:\n{format_products(shopify_products['event_style'])}\n"

    return response
