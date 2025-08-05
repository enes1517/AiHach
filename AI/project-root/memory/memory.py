# memory/memory.py - Geliştirilmiş versiyon

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
    temperature=0.7  # Biraz daha yaratıcı ama tutarlı
)

# 💬 GLOBAL session store - Bu çok önemli!
session_store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """Session ID'ye göre chat history döndür - eğer yoksa oluştur"""
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
        print(f"🆕 Yeni session oluşturuldu: {session_id}")
    else:
        print(f"📚 Mevcut session kullanılıyor: {session_id}")
    return session_store[session_id]

# 🧠 Kısa ve etkili PromptTemplate
explanation_prompt = PromptTemplate.from_template("""Sen Trendyol ürün asistanısın. KISA ve DOĞRUDAN cevap ver.

Kullanıcı sorusu: "{input}"

KURALLAR:
1. Maksimum 2-3 cümle ile cevap ver
2. Eğer önceki konuşmada ürün önerisi yaptıysan, o ürünlere atıfta bulun
3. "Daha ucuz", "başka renk" gibi sorularda önceki önerileri hatırla
4. Yeni ürün türü sorulursa "ürün araması yapıyorum" de
5. Gereksiz uzun açıklamalar yapma

Örnekler:
- Önceki önerdiğim laptoplardan hangisini beğendin?
- Daha ucuz laptop seçenekleri arıyorum, bekle.
- Şimdi kulaklık araması yapıyorum.

Cevabın:""")

def run_llm(input_data: dict):
    """LLM'i çalıştır ve hafıza ile birlikte yanıt üret"""
    user_input = input_data.get("input", "")
    
    # Prompt'u formatla
    formatted_prompt = explanation_prompt.format_prompt(input=user_input).to_string()
    
    # LLM'den yanıt al
    response = llm.invoke(formatted_prompt)
    
    # Content'i çıkar
    if hasattr(response, "content"):
        content = response.content.strip()
    else:
        content = str(response).strip()
    
    # Çok uzunsa kısalt
    if len(content) > 300:
        content = content[:300] + "..."
    
    print(f"🤖 LLM Response: {content}")
    
    return {
        "memory_response": content,
        "explanation": content
    }

# 📦 Conversation chain - session store ile
conversation_chain = RunnableWithMessageHistory(
    RunnableLambda(run_llm),
    get_session_history,  # Function reference, çağırma değil!
    input_messages_key="input",
    history_messages_key="history"
)

# 🔧 Session yönetimi fonksiyonları
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

def get_session_summary(session_id: str) -> str:
    """Session özetini al"""
    messages = get_conversation_history(session_id)
    if not messages:
        return "Henüz konuşma yok."
    
    user_count = len([m for m in messages if hasattr(m, 'content') and 'Human' in str(type(m))])
    ai_count = len([m for m in messages if hasattr(m, 'content') and 'AI' in str(type(m))])
    
    return f"Toplam: {user_count} kullanıcı, {ai_count} AI mesajı"

# Debug fonksiyonu
def debug_session_store():
    """Session store'u debug et"""
    print(f"🔍 Aktif session sayısı: {len(session_store)}")
    for session_id, history in session_store.items():
        print(f"  📱 {session_id}: {len(history.messages)} mesaj")

# Otomatik temizlik (çok fazla session birikirse)
def cleanup_old_sessions(max_sessions: int = 50):
    """Eski session'ları temizle"""
    if len(session_store) > max_sessions:
        # İlk yarısını sil
        sessions_to_remove = list(session_store.keys())[:len(session_store)//2]
        for session_id in sessions_to_remove:
            del session_store[session_id]
        print(f"🧹 {len(sessions_to_remove)} eski session temizlendi")