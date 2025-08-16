import requests

SHOPIFY_STORE_URL = "wcmr5m-fm.myshopify.com"  # your store URL
SHOPIFY_STOREFRONT_TOKEN = "6a6b3edd5ddea5ee734aff5c7690d973"  # your storefront API token

def test_storefront_api():
    graphql_query = """
    {
      products(first: 5) {
        edges {
          node {
            id
            title
            tags
            onlineStoreUrl
            priceRange {
              minVariantPrice {
                amount
                currencyCode
              }
            }
          }
        }
      }
    }
    """

    url = f"https://{SHOPIFY_STORE_URL}/api/2023-04/graphql.json"
    headers = {
        "X-Shopify-Storefront-Access-Token": SHOPIFY_STOREFRONT_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json={"query": graphql_query}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        products = data.get("data", {}).get("products", {}).get("edges", [])
        print(f"✅ Retrieved {len(products)} products:")
        for p in products:
            node = p["node"]
            print(f"- {node['title']} (Tags: {node['tags']}) Price: {node['priceRange']['minVariantPrice']['amount']} {node['priceRange']['minVariantPrice']['currencyCode']}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_storefront_api()
