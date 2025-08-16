from shopify_api import get_products_by_tags

# Expanded tags mapping for better recommendations
MORPHOTYPE_TAGS = {
    "Inverted Triangle": ["v-neck", "boat-neck", "fitted", "a-line", "bootcut", "linen", "tailored", "maxi", "striped"],
    "Pear": ["wide-neck", "off-shoulder", "flared", "straight-leg", "structured-jacket", "denim", "layered", "floral", "cotton"],
    "Rectangle": ["peplum", "belted-dress", "layered-outfit", "wrap", "sheath", "minimalist", "silk", "tailored", "loose-fit"],
    "Oval/Apple":["loose-fit", "draped", "empire-waist", "soft-fabric"],

}

GLASSES_TAGS = {
    "Round": ["rectangle-frames", "wayfarers", "browline", "cat-eye"],
    "Oval": ["aviators", "classic-frames", "oversized", "round-frames"],
    "Long": ["oversized-round", "square-glasses", "wayfarers", "cat-eye"],
}

EVENT_TAGS = {
    "wedding": ["elegant-dress", "classic-suit", "pastel-tone", "formal", "silk", "lace"],
    "beach": ["light-fabric", "bright-color", "hat", "casual", "summer", "linen"],
    "business": ["blazer", "dress-shirt", "neutral-color", "tailored", "formal"],
}

def get_recommendations(morphotype, head_shape, event=None):
    # Get Shopify products by morphotype
    clothing_products = []
    for tag in MORPHOTYPE_TAGS.get(morphotype, []):
        clothing_products.extend(get_products_by_tags([tag]))

    # Get Shopify products for glasses
    glasses_products = []
    for tag in GLASSES_TAGS.get(head_shape, []):
        glasses_products.extend(get_products_by_tags([tag]))

    # Get Shopify products for event (optional)
    event_products = []
    if event and event.lower() in EVENT_TAGS:
        for tag in EVENT_TAGS[event.lower()]:
            event_products.extend(get_products_by_tags([tag]))

    return {
        "clothing": clothing_products,
        "glasses": glasses_products,
        "event_style": event_products
    }
