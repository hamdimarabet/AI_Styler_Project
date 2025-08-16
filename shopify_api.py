import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")
SHOPIFY_STOREFRONT_TOKEN = os.getenv("SHOPIFY_STOREFRONT_TOKEN")

def get_products_by_tags(tags):
    # Format tags as query string, e.g. "V-neck A-line"
    tag_query = " ".join(tags)

    graphql_query = f"""
    {{
      products(first: 10, query: "{tag_query}") {{
        edges {{
          node {{
            id
            title
            tags
            onlineStoreUrl
            images(first: 1) {{
              edges {{
                node {{
                  transformedSrc
                }}
              }}
            }}
            priceRange {{
              minVariantPrice {{
                amount
                currencyCode
              }}
            }}
          }}
        }}
      }}
    }}
    """

    url = f"https://{SHOPIFY_STORE_URL}/api/2023-04/graphql.json"
    headers = {
        "X-Shopify-Storefront-Access-Token": SHOPIFY_STOREFRONT_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json={"query": graphql_query}, headers=headers)
    response.raise_for_status()
    data = response.json()

    products = []
    for edge in data.get("data", {}).get("products", {}).get("edges", []):
        node = edge["node"]
        image_url = None
        if node["images"]["edges"]:
            image_url = node["images"]["edges"][0]["node"]["transformedSrc"]

        products.append({
            "id": node["id"],
            "title": node["title"],
            "tags": node["tags"],
            "url": node.get("onlineStoreUrl", "#"),
            "image": image_url,
            "price": node["priceRange"]["minVariantPrice"]["amount"],
            "currency": node["priceRange"]["minVariantPrice"]["currencyCode"]
        })

    return products

# Example usage:
if __name__ == "__main__":
    sample_tags = ["V-neck", "A-line"]
    products = get_products_by_tags(sample_tags)
    for p in products:
        print(f"{p['title']} - {p['price']} {p['currency']} - Tags: {p['tags']}")
