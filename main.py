import os
from flask import Flask, render_template, request, jsonify
from utils_detection import analyze_body_and_face
from assistant import chat_with_assistant
from shopify_api import get_products_by_tags  # import your Shopify API code

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

user_profile = {"morphotype": None, "head_shape": None}

# Define mapping of morphotype to product tags
MORPHOTYPE_TAGS = {
    "Inverted Triangle": ["v-neck", "boat-neck", "fitted", "a-line", "bootcut", "linen", "tailored", "maxi", "striped"],
    "Pear": ["wide-neck", "off-shoulder", "flared", "straight-leg", "structured-jacket", "denim", "layered", "floral", "cotton"],
    "Rectangle": ["peplum", "belted-dress", "layered-outfit", "wrap", "sheath", "minimalist", "silk", "tailored", "loose-fit"],
    "Oval/Apple":["loose-fit", "draped", "empire-waist", "soft-fabric"],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    if file:
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        # Analyze image
        result = analyze_body_and_face(path)
        user_profile.update(result)

        # Get product tags for morphotype
        morphotype = result.get("morphotype", "Unknown")
        tags = MORPHOTYPE_TAGS.get(morphotype, [])

        # Get products from Shopify API (query each tag separately)
        products = []
        for tag in tags:
            tag_products = get_products_by_tags([tag])
            products.extend(tag_products)

        # Remove duplicate products by ID
        seen = set()
        unique_products = []
        for p in products:
            if p["id"] not in seen:
                seen.add(p["id"])
                unique_products.append(p)

        return jsonify({"status": "ok", "analysis": result, "products": unique_products})

    return jsonify({"status": "error", "message": "No image uploaded"})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    morphotype = user_profile.get("morphotype", "Unknown")
    head_shape = user_profile.get("head_shape", "Unknown")
    response = chat_with_assistant(user_message, morphotype, head_shape)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ✅ use Render's assigned port
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host="0.0.0.0", port=port, debug=True)
