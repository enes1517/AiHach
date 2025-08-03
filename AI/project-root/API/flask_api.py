import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# web_api.py - ASP.NET Controller'ına uygun format
from flask import Flask, request, jsonify
from flask_cors import CORS
from graph.flow import create_graph
import uuid

app = Flask(__name__)
CORS(app, origins="*")

# Session'ları saklamak için basit dictionary
user_sessions = {}

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """ASP.NET Controller'ının beklediği format"""
    
    # OPTIONS request için CORS
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        print("🔍 /analyze endpoint'ine istek geldi")
        
        # JSON data al
        data = request.get_json()
        print(f"📥 Gelen data: {data}")
        
        if not data:
            print("❌ JSON data yok!")
            return jsonify({'error': 'JSON data gerekli'}), 400
        
        # ASP.NET Controller "user_input" bekliyor
        user_input = data.get('user_input', '')
        print(f"💬 User input: '{user_input}'")
        
        if not user_input:
            print("❌ user_input boş!")
            return jsonify({'error': 'user_input alanı gerekli'}), 400
        
        # Her istek için yeni session (basit yaklaşım)
        session_id = str(uuid.uuid4())
        
        # Session oluştur
        if session_id not in user_sessions:
            print(f"📝 Yeni session oluşturuluyor: {session_id}")
            user_sessions[session_id] = {
                'graph': create_graph(),
                'message_count': 0
            }
        
        user_sessions[session_id]['message_count'] += 1
        graph = user_sessions[session_id]['graph']
        
        print(f"🚀 Graph invoke başlatılıyor...")
        
        # Ana AI mantığını çalıştır
        result = graph.invoke({
            "input": user_input,
            "session_id": session_id
        })
        
        print(f"✅ Graph result alındı: {type(result)}")
        print(f"📤 Result: {result}")
        
        # ASP.NET Controller'ının beklediği formata çevir
        products = []
        
        if isinstance(result, dict):
            # Ürün listesi varsa
            if result.get('result') and isinstance(result['result'], list):
                for item in result['result']:
                    product = {
                        'name': item.get('title', 'Ürün adı yok'),
                        'price': extract_price(item.get('price', '0')),
                        'image': item.get('image', '')
                    }
                    products.append(product)
            
            # Sadece açıklama varsa (memory response vs.)
            elif result.get('memory_response') or result.get('explanation'):
                # Açıklama varsa sahte bir ürün ekle
                explanation = result.get('memory_response') or result.get('explanation') or str(result)
                product = {
                    'name': f"Açıklama: {explanation[:100]}...",
                    'price': 0.0,
                    'image': ''
                }
                products.append(product)
        
        # ASP.NET Controller'ının beklediği format
        response = {
            'products': products
        }
        
        print(f"📤 Response gönderiliyor: {len(products)} ürün")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ HATA OLUŞTU: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Hata durumunda boş ürün listesi döndür
        return jsonify({
            'products': []
        }), 200  # 500 yerine 200 döndür ki Controller hata almasın

def extract_price(price_str):
    """Fiyat string'ini float'a çevir"""
    try:
        # "150 TL" -> 150.0
        # "150.50 TL" -> 150.5
        if isinstance(price_str, (int, float)):
            return float(price_str)
        
        if isinstance(price_str, str):
            # TL, ₺ gibi para birimlerini temizle
            price_clean = price_str.replace('TL', '').replace('₺', '').replace(',', '.').strip()
            return float(price_clean)
        
        return 0.0
    except:
        return 0.0

@app.route('/health', methods=['GET'])
def health():
    """API sağlık kontrolü"""
    return jsonify({
        'status': 'healthy',
        'message': 'Trendyol AI API - ASP.NET Uyumlu',
        'active_sessions': len(user_sessions),
        'endpoint': '/analyze'
    })

@app.route('/test', methods=['POST'])
def test():
    """Test endpoint"""
    try:
        data = request.get_json()
        return jsonify({
            'products': [
                {
                    'name': 'Test Gaming Mouse',
                    'price': 299.99,
                    'image': 'https://example.com/mouse.jpg'
                },
                {
                    'name': 'Test Keyboard',
                    'price': 199.99,
                    'image': 'https://example.com/keyboard.jpg'
                }
            ]
        })
    except Exception as e:
        return jsonify({'products': []}), 200

@app.route('/', methods=['GET'])
def home():
    """Ana sayfa"""
    return jsonify({
        'title': 'Trendyol AI API - ASP.NET Compatible',
        'message': 'API çalışıyor',
        'endpoint': '/analyze',
        'expected_request': {
            'method': 'POST',
            'url': '/analyze',
            'body': {
                'user_input': 'gaming mouse öner'
            }
        },
        'expected_response': {
            'products': [
                {
                    'name': 'Ürün adı',
                    'price': 299.99,
                    'image': 'https://...'
                }
            ]
        }
    })

if __name__ == "__main__":
    print("🚀 Trendyol AI API (ASP.NET Uyumlu) Başlatılıyor...")
    print("📍 http://localhost:5000")
    print("🔍 Health: http://localhost:5000/health") 
    print("🧪 Test: POST http://localhost:5000/test")
    print("💬 Chat: POST http://localhost:5000/analyze")
    print("-" * 50)
    
    # ASP.NET Controller port 5000 bekliyor
    app.run(host="0.0.0.0", port=5000, debug=True)