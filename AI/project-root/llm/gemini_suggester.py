import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence

load_dotenv()

# 🔑 LLM başlatılıyor
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# ✅ Daha net ve örnekli prompt
filter_prompt = PromptTemplate.from_template("""
Kullanıcının isteği: "{user_input}"

Lütfen aşağıdaki gibi geçerli bir JSON üret. Aşağıdaki örnekleri incele:

İstek: "30000 altı saat öner"
Yanıt:
{{
  "query": "saat",
  "max_price": 30000,
  "category": "saat"
}}

İstek: "5000 TL altı televizyon arıyorum"
Yanıt:
{{
  "query": "televizyon",
  "max_price": 5000,
  "category": "televizyon"
}}

İstek: "telefon istiyorum"
Yanıt:
{{
  "query": "telefon",
  "max_price": null,
  "category": "telefon"
}}

Eğer anlamlı bir ürün sorgusu değilse sadece:
{{
  "error": "Geçersiz sorgu"
}}

Cevabın SADECE geçerli JSON formatında olsun. Açıklama veya ekstra metin ekleme.
""")

# ✅ Çıktıyı JSON'a çevirecek parser
parser = JsonOutputParser()

# ✅ Zinciri tanımla
chain: RunnableSequence = filter_prompt | llm | parser

# ✅ Ana fonksiyon

def extract_filters_from_prompt(user_input: str) -> dict:
    try:
        result = chain.invoke({"user_input": user_input})

        if isinstance(result, dict) and "error" in result:
            print("❌ Geçersiz kullanıcı isteği:", user_input)
            return None

        return result  # Doğrudan filtre dict'i dön

    except Exception as e:
        print("⚠️ LangChain işleme hatası:", e)
        return None



import google.generativeai as genai
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel(model_name="models/gemini-2.5-flash-lite")

def analyze_products_with_gemini(product_list: list, user_input: str) -> list:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    import os
    import json
    import re

    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0.7,
        convert_system_message_to_human=True
    )

    product_list_text = "\n".join([f"{i+1}. {p['name']} - {p['price']} TL" for i, p in enumerate(product_list)])

    prompt = PromptTemplate.from_template("""
Aşağıda bazı ürünler listelenmiştir. Kullanıcının isteğine göre en uygun 10 ürünü seçip, her biri için aşağıdaki formatta JSON objesi oluştur.

Format: 
[
  {{
    "name": "ürün adı",
    "price": 1500,
    "link": "https://....",
    "reason": "neden bu ürünü önerdin?"
  }},
  ...
]

Kullanıcı isteği: {user_input}

Ürünler:
{product_list}
""")

    chain = (
        {"user_input": RunnablePassthrough(), "product_list": lambda x: product_list_text}
        | prompt
        | model
    )

    response = chain.invoke(user_input)
    
    # JSON dışındaki karakterleri temizle
    json_start = response.content.find("[")
    json_end = response.content.rfind("]") + 1
    json_data = response.content[json_start:json_end]

    try:
        parsed = json.loads(json_data)
        return parsed if isinstance(parsed, list) else []
    except Exception as e:
        print("⚠️ JSON parse hatası:", e)
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
