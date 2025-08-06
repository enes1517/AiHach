# memory/memory.py - SADECE context tutan versiyon

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 🔑 Son filtreleri saklamak için yeni alan
last_filters_store = {}  # session_id -> filters

def set_last_filters(session_id: str, filters: dict):
    """Son kullanılan filtreleri kaydet"""
    last_filters_store[session_id] = filters
    print(f"📌 Son filtreler güncellendi: {filters}")

def get_last_filters(session_id: str) -> dict:
    """Son kullanılan filtreleri getir"""
    return last_filters_store.get(session_id, {})

# Ortam değişkenlerini yükle
load_dotenv()

# 🔑 Gemini modelini başlat
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3  # ✅ Daha tutarlı olsun
)

# 💬 GLOBAL session store
session_store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """Session ID'ye göre chat history döndür - eğer yoksa oluştur"""
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
        print(f"🆕 Yeni session oluşturuldu: {session_id}")
    else:
        print(f"📚 Mevcut session kullanılıyor: {session_id}")
    return session_store[session_id]

# ✅ DÜZELTME: Prompt önceki ürünleri hatırlasın ve follow-up soruları tanısın
explanation_prompt = PromptTemplate.from_template("""Sen bir ürün asistanısın. Önceki konuşmayı hatırla ve KISA context cevabı ver.

Kullanıcı sorusu: "{input}"
Kategori: "{category}"

KURALLAR:
1. Maksimum 1-2 cümle ile cevap ver
2. Eğer "bunlardan", "daha ucuz" gibi kelimeler varsa önceki ürünlere atıf yap
3. Her durumda "arıyorum/kontrol ediyorum" ifadesi kullan
4. ASLA "yeterli", "başka bir şey" gibi aramayı durduracak ifadeler kullanma

ÖRNEKLER:
- "Gaming bilgisayarları arıyorum, bekle."
- "Önceki önerdiğim bilgisayarlardan daha ucuz olanlarını kontrol ediyorum."
- "30000 TL altı kaliteli seçenekleri arıyorum."

✅ HER DURUMDA ürün araması yapılacak!

Cevabın:""")

def run_llm(input_data: dict):
    """LLM'i çalıştır - önceki context ile birlikte"""
    user_input = input_data.get("input", "")
    category = input_data.get("category", "")
    
    # Prompt'u formatla - kategori ile birlikte
    formatted_prompt = explanation_prompt.format_prompt(
        input=user_input, 
        category=category
    ).to_string()
    
    # LLM'den yanıt al
    response = llm.invoke(formatted_prompt)
    
    # Content'i çıkar
    if hasattr(response, "content"):
        content = response.content.strip()
    else:
        content = str(response).strip()
    
    # ✅ Her zaman kısa tut
    if len(content) > 150:
        content = content[:150] + "..."
    
    # ✅ Eğer "yeterli" gibi kelimeler varsa düzelt
    problematic_words = ["yeterli", "başka", "tamamdır", "bitir"]
    if any(word in content.lower() for word in problematic_words):
        content = "Ürün araması yapıyorum, lütfen bekle."
    
    print(f"🤖 LLM Response: {content}")
    
    return {
        "memory_response": content,
        "explanation": content
    }

# 📦 Conversation chain
conversation_chain = RunnableWithMessageHistory(
    RunnableLambda(run_llm),
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 🔧 Session yönetimi fonksiyonları (aynı)
def clear_session(session_id: str):
    """Belirli bir session'ı temizle"""
    if session_id in session_store:
        del session_store[session_id]
        print(f"🧹 Session temizlendi: {session_id}")

def get_conversation_history(session_id: str) -> list:
    """Session'ın konuşma geçmişini döndür"""
    if session_id in session_store:
        messages = session_store[session_id].messages
        print(f"📋 Session {session_id} geçmişi: {len(messages)} mesaj")
        return messages
    return []

def debug_session_store():
    """Session store'u debug et"""
    print(f"🔍 Aktif session sayısı: {len(session_store)}")
    for session_id, history in session_store.items():
        print(f"  📱 {session_id}: {len(history.messages)} mesaj")