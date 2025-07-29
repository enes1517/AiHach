import os
import google.generativeai as genai
from dotenv import load_dotenv
import json  # eval yerine json kullanılmalı

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash-lite")

def analyze_products_with_gemini(products: list, user_request: str = "") -> str:
    prompt = f"""
Kullanıcının isteği: "{user_request}"

Aşağıda Trendyol'dan çekilen ürün listesi yer almaktadır. Her ürün sözlük olarak:
- name
- price
- rating
- rating_count
- link
şeklindedir.

Ürün listesi:
{products}

Yukarıdaki ürünleri, kullanıcının isteğine göre filtrele ve analiz et.
En iyi ürünleri öner. Türkçe, sade ve anlaşılır şekilde cevap ver.
"""
    response = model.generate_content(prompt)
    return response.text

import re

def extract_filters_from_prompt(user_input: str) -> dict:
    prompt = f"""
Kullanıcının isteği: "{user_input}"

Sadece aşağıdaki formatta geçerli bir JSON ver:
Açıklama yapma, sadece JSON ver:
{{
  "query": "...",
  "max_price": ...,
  "category": "..."
}}
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Markdown blockları temizle: ```json ... ```
    cleaned = re.sub(r"^```json|```$", "", raw, flags=re.MULTILINE).strip()

    try:
        return json.loads(cleaned)
    except Exception:
        print("⚠️ JSON çözümleme hatası.")
        print("🔎 Gelen veri:", raw)
        return {
            "query": user_input,
            "max_price": None,
            "category": ""
        }
