# memory/memory_utils.py - Ek hafıza yönetimi fonksiyonları

from memory.memory import session_store, get_session_history
import json
from datetime import datetime

def save_conversation_to_file(session_id: str, filename: str = None):
    """Konuşmayı dosyaya kaydet"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{session_id}_{timestamp}.json"
    
    messages = []
    if session_id in session_store:
        for msg in session_store[session_id].messages:
            messages.append({
                "type": msg.__class__.__name__,
                "content": msg.content,
                "timestamp": datetime.now().isoformat()
            })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Konuşma kaydedildi: {filename}")
    return filename

def load_conversation_from_file(session_id: str, filename: str):
    """Dosyadan konuşmayı yükle"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            messages = json.load(f)
        
        # Session history'yi temizle ve yükle
        history = get_session_history(session_id)
        history.clear()
        
        for msg_data in messages:
            if msg_data["type"] == "HumanMessage":
                history.add_user_message(msg_data["content"])
            elif msg_data["type"] == "AIMessage":
                history.add_ai_message(msg_data["content"])
        
        print(f"📂 Konuşma yüklendi: {filename}")
        return True
    
    except Exception as e:
        print(f"❌ Konuşma yükleme hatası: {e}")
        return False

def get_conversation_summary(session_id: str) -> str:
    """Konuşmanın özetini al"""
    if session_id not in session_store:
        return "Henüz konuşma başlamadı."
    
    messages = session_store[session_id].messages
    if not messages:
        return "Henüz mesaj yok."
    
    summary = f"Toplam {len(messages)} mesaj:\n"
    
    user_messages = [msg for msg in messages if hasattr(msg, 'content') and 'human' in msg.__class__.__name__.lower()]
    ai_messages = [msg for msg in messages if hasattr(msg, 'content') and 'ai' in msg.__class__.__name__.lower()]
    
    summary += f"- Kullanıcı mesajları: {len(user_messages)}\n"
    summary += f"- AI mesajları: {len(ai_messages)}\n"
    
    if user_messages:
        summary += f"- İlk soru: {user_messages[0].content[:50]}...\n"
        summary += f"- Son soru: {user_messages[-1].content[:50]}...\n"
    
    return summary

def clear_old_sessions(max_sessions: int = 10):
    """Eski session'ları temizle (memory management)"""
    if len(session_store) > max_sessions:
        # En eski session'ları sil
        sessions_to_remove = list(session_store.keys())[:-max_sessions]
        for session_id in sessions_to_remove:
            del session_store[session_id]
        print(f"🧹 {len(sessions_to_remove)} eski session temizlendi.")

# 🔧 Geliştirilmiş main.py için ek komutlar
COMMANDS = {
    "geçmiş": "Konuşma geçmişini göster",
    "kaydet": "Konuşmayı dosyaya kaydet", 
    "özet": "Konuşma özeti al",
    "temizle": "Mevcut session'ı temizle",
    "yardım": "Komutları göster"
}

def handle_special_commands(user_input: str, session_id: str) -> bool:
    """Özel komutları işle. True döndürürse normal flow'a geçme."""
    
    if user_input.lower() == "yardım":
        print("\n📋 Özel Komutlar:")
        for cmd, desc in COMMANDS.items():
            print(f"• {cmd}: {desc}")
        return True
    
    elif user_input.lower() == "geçmiş":
        summary = get_conversation_summary(session_id)
        print(f"\n📊 Konuşma Geçmişi:\n{summary}")
        return True
    
    elif user_input.lower() == "kaydet":
        filename = save_conversation_to_file(session_id)
        return True
    
    elif user_input.lower() == "özet":
        summary = get_conversation_summary(session_id)
        print(f"\n📋 Özet:\n{summary}")
        return True
    
    elif user_input.lower() == "temizle":
        from memory.memory import clear_session
        clear_session(session_id)
        print("🧹 Konuşma geçmişi temizlendi. Yeni session başlatıldı.")
        return True
    
    return False  # Normal flow'a devam et