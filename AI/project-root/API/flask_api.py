from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.trendyol_scraper import scrape_trendyol
from llm.gemini_suggester import extract_filters_from_prompt, analyze_products_with_gemini
import re

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        user_input = data.get('user_input', '')
        if not user_input:
            return jsonify({'error': 'user_input is required'}), 400

        filters = extract_filters_from_prompt(user_input)
        query = filters.get("query", user_input).lower().strip()
        max_price = filters.get("max_price", None)

        match = re.search(r"(?:\d+\s*TL\s*(?:altı|üstü)?\s*)?(.*)", query, flags=re.IGNORECASE)
        if match:
            query = match.group(1).strip()

        all_products = scrape_trendyol(query, max_pages=2, max_results=100)
        if not all_products:
            return jsonify({'error': 'Ürün bulunamadı.'}), 404

        if max_price:
            all_products = [p for p in all_products if p["price"] <= max_price]
        if not all_products:
            return jsonify({'error': 'Fiyat filtresinden sonra ürün kalmadı.'}), 404

        response = analyze_products_with_gemini(all_products, user_input)
        return jsonify({'result': response})
    except Exception as e:
        return jsonify({'error': f'Beklenmeyen bir hata oluştu: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 