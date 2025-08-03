# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("models/gemini-2.5-flash-lite")

# def main():
#     print("🧠 Gemini ile sohbet başlatıldı! Çıkmak için 'q' yaz.")
    
#     chat = model.start_chat(history=[])
    
#     while True:
#         user_input = input("👤 Sen: ")
#         if user_input.lower() in ['q', 'quit', 'exit']:
#             print("👋 Görüşürüz!")
#             break
        
#         response = chat.send_message(user_input)
#         print(f"🤖 Gemini: {response.text.strip()}\n")

# if __name__ == "__main__":
#     main()


# test_run_llm.py
# from memory.memory import run_llm

# res = run_llm({"input": "3000 TL altı kulaklık arıyorum"})
# print(type(res))           # ✅ <class 'dict'>
# print(res.keys())          # ✅ memory_response, explanation
# print(res["memory_response"])




# test_main.py - Memory sistemini test etmek için

from graph.flow import create_graph
from memory.memory import debug_session_store, get_session_summary
import uuid

def test_memory_conversation():
    """Memory sistemini test et"""
    
    # Session ID oluştur
    session_id = str(uuid.uuid4())
    graph = create_graph()
    
    print("🤖 Trendyol AI Asistanı - Memory Test")
    print(f"🆔 Session ID: {session_id}")
    print("📝 Test senaryoları çalıştırılıyor...")
    print("-" * 60)
    
    # Test senaryoları
    test_conversations = [
        "laptop öner",                    # İlk arama
        "daha ucuz olanları göster",      # Follow-up
        "hangi markaları var?",          # Marka sorusu
        "gaming laptop var mı?",         # Özellik sorusu
        "kulaklık arıyorum",             # Yeni ürün türü
        "bluetooth olanları",            # Yeni ürün follow-up
    ]
    
    for i, user_input in enumerate(test_conversations, 1):
        print(f"\n🔄 Test {i}: {user_input}")
        print("-" * 30)
        
        try:
            # Graph'ı çalıştır
            result = graph.invoke({
                "input": user_input,
                "session_id": session_id
            })
            
            # Sonuçları göster
            memory_response = result.get("memory_response", "")
            products = result.get("result", [])
            
            if memory_response:
                print(f"🧠 Memory Cevabı: {memory_response}")
            
            if isinstance(products, list) and products:
                print(f"🛍️ Bulunan Ürünler: {len(products)} adet")
                # İlk 2 ürünü göster
                for j, product in enumerate(products[:2], 1):
                    if isinstance(product, dict):
                        title = product.get('title', product.get('name', 'Ürün'))
                        price = product.get('price', 'Fiyat?')
                        print(f"  {j}. {title[:50]}... - {price} TL")
            else:
                print("🛍️ Ürün bulunamadı")
            
            # Session özetini göster
            summary = get_session_summary(session_id)
            print(f"📊 Session Özeti: {summary}")
            
        except Exception as e:
            print(f"❌ Test hatası: {e}")
    
    # Final session durumu
    print(f"\n{'='*60}")
    print("🏁 Test Tamamlandı")
    debug_session_store()

def interactive_memory_test():
    """Interaktif memory test"""
    
    session_id = str(uuid.uuid4())
    graph = create_graph()
    
    print("🤖 Trendyol AI Asistanı - Interactive Memory Test")
    print(f"🆔 Session ID: {session_id}")
    print("📝 Komutlar: 'çıkış', 'özet', 'temizle'")
    print("-" * 60)
    
    while True:
        user_input = input("\n🧠 Ne istiyorsun?: ").strip()
        
        # Özel komutlar
        if user_input.lower() in ['çıkış', 'exit', 'quit']:
            print("👋 Görüşürüz!")
            break
        elif user_input.lower() == 'özet':
            summary = get_session_summary(session_id)
            print(f"📊 {summary}")
            continue
        elif user_input.lower() == 'temizle':
            from memory.memory import clear_session
            clear_session(session_id)
            print("🧹 Session temizlendi!")
            continue
        
        if not user_input:
            continue
        
        try:
            # Graph'ı çalıştır
            result = graph.invoke({
                "input": user_input,
                "session_id": session_id
            })
            
            # Memory cevabını göster
            if result.get("memory_response"):
                print(f"\n🧠 AI: {result['memory_response']}")
            
            # Ürünleri göster
            products = result.get("result", [])
            if isinstance(products, list) and products:
                print(f"\n🛍️ {len(products)} ürün bulundu:")
                for i, product in enumerate(products[:3], 1):  # İlk 3 ürün
                    if isinstance(product, dict):
                        title = product.get('title', product.get('name', 'Ürün'))
                        price = product.get('price', 'Fiyat?')
                        print(f"  {i}. {title[:60]}... - {price} TL")
            
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    # Önce otomatik test
    print("🔧 Otomatik test çalıştırılıyor...")
    test_memory_conversation()
    
    # Sonra interaktif test
    print("\n" + "="*60)
    input("⏸️ Enter'a basın ve interaktif teste geçin...")
    interactive_memory_test()