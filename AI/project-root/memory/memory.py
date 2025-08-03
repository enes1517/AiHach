# memory/memory.py - Düzeltilmiş versiyon
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Ortam değişkenlerini yükle
load_dotenv()

# 🔑 Gemini modelini başlat
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 💬 GLOBAL session store - Bu çok önemli!
session_store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    """Session ID'ye göre chat history döndür - eğer yoksa oluştur"""
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]

# 🧠 Geliştirilmiş PromptTemplate
explanation_prompt = PromptTemplate.from_template("""
Sen Trendyol ürün önerisi yapan bir AI asistanısın. 

Kullanıcının mevcut sorusu: "{input}"

Geçmiş konuşmalarını göz önünde bulundurarak yanıt ver:
- Eğer daha önce ürün önerileri yaptıysan ve kullanıcı o önerilerle ilgili soru soruyorsa, önceki önerilerini referans al
- Kullanıcının tercihlerini hatırla
- Tutarlı ve samimi bir dille cevap ver
- Önceki konuşmalarla çelişme

Yanıt formatı:
- Hangi ürünler neden öneriliyor?
- Kullanıcıya en uygun olanlar hangileri?
- Karşılaştırmalı önerilerin varsa yaz

Samimi ama profesyonel ol.
""")

def run_llm(input_data: dict):
    """LLM'i çalıştır ve hafıza ile birlikte yanıt üret"""
    user_input = input_data.get("input", "")
    
    # Prompt'u formatla
    formatted_prompt = explanation_prompt.format_prompt(input=user_input).to_string()
    
    # LLM'den yanıt al
    response = llm.invoke(formatted_prompt)
    
    # Content'i çıkar
    if hasattr(response, "content"):
        content = response.content
    else:
        content = str(response)
    
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

# 🔧 Session temizleme fonksiyonu (isteğe bağlı)
def clear_session(session_id: str):
    """Belirli bir session'ı temizle"""
    if session_id in session_store:
        del session_store[session_id]

def get_conversation_history(session_id: str) -> list:
    """Session'ın konuşma geçmişini döndür"""
    if session_id in session_store:
        return session_store[session_id].messages
    return []