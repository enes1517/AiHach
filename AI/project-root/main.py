# main.py - Session ID ile sürekli konuşma
from graph.flow import create_graph
import uuid

def main():
    # 🆔 Bir kere session ID oluştur - bu çok önemli!
    session_id = str(uuid.uuid4())
    graph = create_graph()
    
    print("🤖 Trendyol AI Asistanı - Sürekli Konuşma Modu")
    print("📝 'çıkış' yazarak programdan çıkabilirsiniz.")
    print("-" * 50)
    
    while True:
        user_input = input("\n🧠 Ne istiyorsun?: ")
        
        # Çıkış kontrolü
        if user_input.lower() in ['çıkış', 'exit', 'quit', 'q']:
            print("👋 Görüşürüz!")
            break
        
        try:
            # Graph'ı session ID ile çalıştır
            result = graph.invoke({
                "input": user_input,
                "session_id": session_id  # Session ID'yi state'e ekle
            })
            
            print(f"\n🎯 Final Çıktı: {result}")
            
            # Hafıza cevabını göster
            if result.get("memory_response"):
                print(f"\n📚 Hafıza Cevabı: {result['memory_response']}")
            
            # Açıklamayı göster
            if result.get("explanation"):
                print(f"\n📘 Açıklama: {result['explanation']}")
            
            # Hata kontrolü
            if isinstance(result, dict) and result.get("error"):
                print(f"\n🚫 Hata: {result['error']}")
                continue
            
            # Ürün önerilerini göster
            if isinstance(result, dict) and result.get("result"):
                print("\n🤖 Ürün Önerileri:")
                for i, item in enumerate(result["result"], 1):
                    print(f"\n🔹 {i}. Ürün")
                    print(f"🛒 Başlık: {item['title']}")
                    print(f"💰 Fiyat: {item['price']} TL")
                    print(f"🔗 Link: {item['link']}")
                    if item.get("image"):
                        print(f"🖼️ Resim: {item['image']}")
                    print(f"🧠 Neden önerildi? {item['why_recommended']}")
        
        except Exception as e:
            print(f"❌ Hata oluştu: {e}")
            continue

if __name__ == "__main__":
    main()