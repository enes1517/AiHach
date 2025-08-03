import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# web_api.py - ASP.NET Controller'ına uygun format

from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from scraper.trendyol_scraper import scrape_trendyol
from llm.gemini_suggester import extract_filters_from_prompt, analyze_products_with_gemini
from graph.flow import create_graph  # Graph sistemi import et
import re
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Session için gerekli
CORS(app)

# Graph'ı bir kere oluştur - performans için
graph = create_graph()

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        print("🔍 /analyze endpoint'ine istek geldi")
        
        # Session ID kontrolü - yoksa oluştur
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            print(f"🆔 Yeni session ID oluşturuldu: {session['session_id']}")
        else:
            print(f"🆔 Mevcut session ID kullanılıyor: {session['session_id']}")
        
        data = request.get_json()
        user_input = data.get('user_input', '').strip()
        
        print(f"💬 User input: '{user_input}'")
        
        if not user_input:
            return jsonify({'error': 'user_input is required'}), 400
        
        print("🚀 AI Graph çalıştırılıyor...")
        
        # ÖNCELİKLE GRAPH SİSTEMİNİ DENE
        try:
            result = graph.invoke({
                "input": user_input,
                "session_id": session['session_id']  # Session ID'yi ekle
            })
            
            print(f"✅ AI sonucu alındı: {type(result)}")
            
            # Eğer graph'tan ürün gelirse, onu döndür
            if result.get("result") and isinstance(result["result"], list) and len(result["result"]) > 0:
                print(f"🛍️ Graph'tan {len(result['result'])} ürün döndürülüyor")
                return jsonify({
                    'products': result["result"],
                    'memory_response': result.get("memory_response", ""),
                    'explanation': result.get("explanation", ""),
                    'source': 'ai_graph'
                })
            
            # Eğer hafıza cevabı varsa ama ürün yoksa
            if result.get("memory_response"):
                print(f"📚 Hafıza cevabı döndürülüyor: {result['memory_response']}")
                return jsonify({
                    'products': [],
                    'memory_response': result["memory_response"],
                    'explanation': result.get("explanation", ""),
                    'message': result["memory_response"],
                    'source': 'memory'
                })
            
            # Eğer graph'tan hata gelirse
            if result.get("error"):
                print(f"🚫 Graph'tan hata: {result['error']}")
                # Hata durumunda da eski sisteme düş
                
        except Exception as graph_error:
            print(f"❌ Graph sistemi hatası: {graph_error}")
            # Graph hatası durumunda eski sisteme düş
        
        print("🔄 AI'dan ürün gelmedi, scraper'ı çalıştırıyoruz")
        
        # ESKİ SİSTEM - SCRAPER + FİLTRELER
        filters = extract_filters_from_prompt(user_input)
        query = filters.get("query", user_input).lower().strip()
        max_price = filters.get("max_price", None)

        match = re.search(r"(?:\d+\s*TL\s*(?:altı|üstü)?\s*)?(.*)", query, flags=re.IGNORECASE)
        if match:
            query = match.group(1).strip()

        print(f"🕷️ Trendyol scraper çalıştırılıyor...")
        all_products = scrape_trendyol(query, max_pages=2, max_results=100)
        
        if not all_products:
            print("❌ Scraper'dan ürün bulunamadı")
            return jsonify({'error': 'Ürün bulunamadı.'}), 404

        if max_price:
            all_products = [p for p in all_products if p["price"] <= max_price]
            
        if not all_products:
            print("❌ Fiyat filtresinden sonra ürün kalmadı")
            return jsonify({'error': 'Fiyat filtresinden sonra ürün kalmadı.'}), 404

        print(f"📤 Toplam {len(all_products)} ürün döndürülüyor")
        return jsonify({
            'products': all_products,
            'source': 'scraper'
        })
        
    except Exception as e:
        print(f"❌ Genel hata: {str(e)}")
        return jsonify({'error': f'Beklenmeyen bir hata oluştu: {str(e)}'}), 500

@app.route('/clear-session', methods=['POST'])
def clear_session():
    """Session'ı temizle - yeni konuşma başlat"""
    try:
        session.clear()
        print("🧹 Session temizlendi")
        return jsonify({
            'success': True,
            'message': 'Konuşma geçmişi temizlendi, yeni bir oturum başlatıldı.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Session temizlenirken hata: {str(e)}'
        })

@app.route('/products', methods=['GET'])
def show_products():
    query = request.args.get('q', '')
    if not query:
        return 'Arama sorgusu giriniz', 400
    products = scrape_trendyol(query, max_pages=2, max_results=20)
    return render_template('products.html', products=products, query=query)

@app.route('/')
def index():
    """Ana sayfa - web arayüzü"""
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)