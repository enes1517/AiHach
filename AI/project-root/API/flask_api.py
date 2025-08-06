import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from scraper.trendyol_scraper import scrape_trendyol
from llm.gemini_suggester import extract_filters_from_prompt, analyze_products_with_gemini
from graph.flow import create_graph
import re
import uuid
import traceback

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
CORS(app, supports_credentials=True)  # Session için credentials gerekli

# Graph'ı bir kere oluştur
graph = create_graph()

# Flask API - /analyze endpoint düzeltmesi

# Flask API - /analyze endpoint düzeltmesi

# Flask API - /analyze endpoint düzeltmesi

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """Ana analiz endpoint'i - HER ZAMAN ürün döndür"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        print("🔍 /analyze endpoint'ine istek geldi")
        
        # Request data al
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        # Session ID yönetimi
        session_id = data.get('session_id')
        
        if not session_id:
            session_id = str(uuid.uuid4())
            print(f"🆔 Yeni session ID oluşturuldu: {session_id}")
        else:
            print(f"🆔 Mevcut session ID kullanılıyor: {session_id}")
        
        # User input kontrolü
        user_input = data.get('message', '').strip()
        if not user_input:
            user_input = data.get('user_input', '').strip()
            
        if not user_input:
            return jsonify({
                'error': 'message field is required',
                'session_id': session_id
            }), 400
        
        print(f"💬 User input: '{user_input}'")
        
        # AI Graph çalıştır
        print("🚀 AI Graph çalıştırılıyor...")
        
        try:
            result = graph.invoke({
                "input": user_input,
                "session_id": session_id
            })
            
            print(f"✅ AI sonucu alındı: {type(result)}")
            
            # ✅ DÜZELTME: Memory response + Products birlikte gönder
            products = result.get("result", [])
            memory_response = result.get("memory_response", "")
            
            # Response formatı - Client beklentisine uygun
            response_data = {
                'session_id': session_id,
                'response': memory_response,  # ✅ Memory context
                'products': products,         # ✅ Ürünler
                'explanation': result.get("explanation", ""),
                'filters': result.get("filters", {}),
                'success': True
            }
            
            # Ürün sayısı kontrolü
            if isinstance(products, list) and len(products) > 0:
                print(f"🛍️ Graph'tan {len(products)} ürün döndürülüyor")
                response_data['total_found'] = len(products)
            else:
                print(f"❌ Hiç ürün bulunamadı")
                response_data['total_found'] = 0
                # ✅ Memory response varsa onu göster
                if not memory_response:
                    response_data['response'] = "Üzgünüm, aradığınız kriterlere uygun ürün bulunamadı."
            
            # ✅ DEBUG: Console'a yazdır
            print(f"📤 Response data: response='{response_data.get('response', 'YOK')}', products={len(products)}")
            
            return jsonify(response_data)
            
        except Exception as graph_error:
            print(f"❌ Graph sistemi hatası: {graph_error}")
            print(f"📍 Hata detayı: {traceback.format_exc()}")
            
            return jsonify({
                'session_id': session_id,
                'response': "Şu anda bir teknik sorun yaşıyoruz. Lütfen daha sonra tekrar deneyin.",
                'products': [],
                'explanation': '',
                'filters': {},
                'success': False,
                'error_type': 'graph_error',
                'error_details': str(graph_error)
            })
        
    except Exception as e:
        print(f"❌ Genel hata: {str(e)}")
        print(f"📍 Hata detayı: {traceback.format_exc()}")
        
        return jsonify({
            'success': False,
            'error': f'Sunucu hatası: {str(e)}',
            'session_id': session_id if 'session_id' in locals() else None
        }), 500

@app.route('/clear-session', methods=['POST'])
def clear_session():
    """Session'ı temizle - yeni konuşma başlat"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id')
        
        if session_id:
            print(f"🧹 Session temizlendi: {session_id}")
        
        # Yeni session ID oluştur
        new_session_id = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'message': 'Konuşma geçmişi temizlendi, yeni bir oturum başlatıldı.',
            'new_session_id': new_session_id
        })
        
    except Exception as e:
        print(f"❌ Session temizleme hatası: {e}")
        return jsonify({
            'success': False,
            'error': f'Session temizlenirken hata: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Sistem sağlık kontrolü"""
    try:
        # Basit bir graph testi
        test_result = graph.invoke({
            "input": "test",
            "session_id": "health-check"
        })
        
        return jsonify({
            'status': 'healthy',
            'graph_working': True,
            'timestamp': str(uuid.uuid4())
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'graph_working': False,
            'error': str(e)
        }), 500

@app.route('/products', methods=['GET'])
def show_products():
    """Direkt ürün arama - debug için"""
    query = request.args.get('q', '')
    if not query:
        return 'Arama sorgusu giriniz', 400
    
    try:
        products = scrape_trendyol(query, max_pages=2, max_results=20)
        return render_template('products.html', products=products, query=query)
    except Exception as e:
        return f'Scraping hatası: {str(e)}', 500

@app.route('/')
def index():
    """Ana sayfa - web arayüzü"""
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint bulunamadı'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Sunucu hatası'}), 500

if __name__ == "__main__":
    print("🚀 Flask API başlatılıyor...")
    print("📡 Endpoints:")
    print("   POST /analyze - Ana AI analiz")
    print("   POST /clear-session - Session temizle")
    print("   GET /health - Sağlık kontrolü")
    print("   GET /products - Direkt ürün arama")
    print("   GET / - Ana sayfa")
    
    app.run(host="0.0.0.0", port=5000, debug=True)