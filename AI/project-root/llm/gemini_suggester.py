import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=os.getenv("GEMINI_API_KEY"))

filter_prompt = PromptTemplate.from_template("""
Kullanıcının isteği: "{user_input}"

Yalnızca geçerli bir ürün isteği varsa aşağıdaki JSON formatını ver:
{{
  "query": "...",      
  "max_price": ...,    
  "category": "..."    
}}

Eğer anlamlı bir istek değilse sadece:
{{
  "error": "Geçersiz sorgu"
}}
""")

parser = JsonOutputParser()

chain: RunnableSequence = filter_prompt | llm | parser

def extract_filters_from_prompt(user_input: str) -> dict:
    try:
        result = chain.invoke({"user_input": user_input})
        if isinstance(result, dict) and "error" in result:
            print("❌ Geçersiz kullanıcı isteği:", user_input)
            return None
        return result
    except Exception as e:
        print("⚠️ LangChain işleme hatası:", e)
        return None

import google.generativeai as genai
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel(model_name="models/gemini-2.5-flash-lite")

def analyze_products_with_gemini(products: list, user_request: str = "", category: str = "") -> list:
    prompt = f"""
Kullanıcının isteği: "{user_request}"
Kategori: "{category}" (Sadece bu kategorideki ürünleri öner, başka kategoriden sapma yapma.)

Aşağıda Trendyol'dan çekilen ürün listesi yer almaktadır. Her ürün sözlük olarak:
- name
- price
- rating
- rating_count
- link
şeklindedir.

Ürün listesi:
{json.dumps(products, ensure_ascii=False)}

KURALLAR:
1. Sadece "{category}" kategorisindeki ürünleri analiz et ve öner.
2. En iyi 10 ürünü seç (fiyat, rating ve rating_count'a göre).
3. Her öneri için şu formatı kullan:
   - Ürün: [name]
     - Özellikler: [Kısa özellik tahmini, örneğin ekran boyutu, çözünürlük vb. - eğer veri yoksa "bilinmeyen" yaz]
     - Fiyat Aralığı: [price] TL
     - Neden Önerildi: [Kısa açıklama, örneğin "Yüksek rating" veya "Uygun fiyat"]
4. Eğer uygun ürün yoksa, "Bu kategoride uygun ürün bulunamadı" de.
5. Cevabı JSON listesi olarak döndür.

Cevabın:
"""
    try:
        response = gemini_model.generate_content(prompt)
        parsed = json.loads(response.text) if response.text.strip().startswith('[') else []
        return parsed if isinstance(parsed, list) else []
    except Exception as e:
        print(f"⚠️ Analyze_products_with_gemini hatası: {e}")
        return []
def explain_recommendation(products: list, query: str) -> list:
    prompt = f"""
Kullanıcının isteği: "{query}"

Aşağıda Trendyol'dan alınan ürünlerin listesi vardır. Her ürün bir sözlük şeklindedir:
- title
- price
- link
- rating
- rating_count

Amaç: Kullanıcıya her ürünün neden önerildiğini bir cümleyle açıklamaktır.

Lütfen her ürün için kısa, Türkçe, sade bir açıklama üret ve sadece açıklamaları içeren bir JSON listesi ver:
[
  "...",
  "...",
  "..."
]

Ürünler:
{json.dumps(products, ensure_ascii=False)}
"""
    try:
        response = gemini_model.generate_content(prompt)
        parsed = json.loads(response.text)
        return parsed if isinstance(parsed, list) else []
    except Exception as e:
        print("⚠️ Açıklama üretim hatası:", e)
        return ["Bu ürün uygun bulundu." for _ in products]
