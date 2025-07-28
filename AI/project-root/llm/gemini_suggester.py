import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash-lite")

def extract_filters_from_prompt(user_input: str) -> dict:
    prompt = f"""
Kullanıcının isteği: "{user_input}"

Aşağıdaki JSON formatına sıkı sıkıya uyarak cevap ver. Açıklama yapma, sadece JSON olarak dön:

{{
  "query": "...",        
  "category": "...",     
  "max_price": ...,      
  "keywords": ["...", "..."]
}}

Lütfen sadece geçerli bir JSON çıktısı ver. Kod bloğu veya başka bir şey olmasın.
"""

    response = model.generate_content(prompt)

    try:
        response_text = response.text if hasattr(response, "text") else response.parts[0].text

        cleaned = response_text.strip().replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(cleaned)
        except Exception as e:
            print("❌ JSON parsing after cleanup da başarısız:", e)
            print("Yanıt (temizlenmiş):", cleaned)
        return {}

    except Exception as e:
        print("❌ JSON çözümleme hatası:", e)
        print("Yanıt:", response_text)
        return {}
