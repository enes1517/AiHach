🧠 Hakkında
Bu proje, doğal dil işleme (NLP) ve yapay zeka destekli filtreleme yöntemleriyle çalışan bir ürün öneri sistemidir. Kullanıcılar serbest biçimde (örneğin: “3000 TL altı hızlı bir laptop”) isteklerini yazabilir. Sistem bu girdileri analiz eder, anlamlı filtrelere çevirir ve Trendyol'dan ürünleri çekerek en uygun sonuçları önerir.

🔍 Temel Özellikler
Gemini AI ile doğal dil anlayışı

LangChain & LangGraph ile akıllı mantık akışı

Selenium ile Trendyol scraping

ASP.NET MVC ile modern web arayüzü

Hash algoritması ile şifreleme

Çok adımlı konuşma desteği (session_id)

Modüler yapı (LLM node'ları ayrı ayrı
Proje iki ana bileşenden oluşur:

1. `AI/` klasörü → **Python tabanlı Flask API** (LLM, scraping, öneri mantığı burada)
2. `UserAuthMvc.Web/` → **ASP.NET Core MVC** (Frontend, kullanıcı arayüzü, authentication)

---

## 🚀 Başlatma Talimatları

### 1. AI Backend (Python - Flask)

```bash
cd AI
python -m venv venv
venv\\Scripts\\activate        # MacOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```
.env dosyasını oluştur:
```bash
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```
Flask API'yi başlat:
```bash
Kopyala
Düzenle
python flask_api.py
```
Web Arayüzü (ASP.NET Core MVC)
```bash
cd UserAuthMvc.Web
dotnet run
```
```bash
root/
├── AI/                        # Python AI mantığı burada
│   ├── graph/                # LangGraph flow mantığı
│   ├── nodes/                # AI node'ları (filter, memory, analyze vs.)
│   ├── scraper/              # Trendyol Scraper (Selenium)
│   ├── filters/              # LLM filtre çıkarımı
│   ├── llm/                  # Gemini AI fonksiyonları
│   ├── flask_api.py          # Flask entry point
│   └── requirements.txt      # Python bağımlılıkları
│
├── UserAuthMvc.Web/          # ASP.NET Core MVC frontend
├── UserAuthMvc.BLL/          # İş mantığı
├── UserAuthMvc.DAL/          # Veri erişim katmanı
├── UserAuthMvc.Entities/     # Veri modelleri
├── UserAuthMvc.sln           # Visual Studio çözüm dosyası
└── .env                      # Gemini API anahtarı (AI klasörü içinde)
```
⚙️ Kullanılan Teknolojiler
Backend (AI tarafı)
Python 3.10+

Flask

Gemini API (Google AI)

LangChain

LangGraph

Selenium

BeautifulSoup4

python-dotenv

Frontend (Web tarafı)
ASP.NET Core MVC

C#

Razor Pages

Bootstrap 5

JavaScript
🔧 Teknik Detaylar
AI tarafında LangChain RunnableSequence ile Filter → Memory → Scrape → Analyze node akışı oluşturulmuştur.

Her node bağımsız ve test edilebilir şekilde yazılmıştır (modüler yapı).

session_id ile kullanıcı bazlı geçmiş konuşma hatırlanabilir.

Flask API, POST /analyze endpoint’i ile çalışır.

Web UI, AI API’ye HTTP istek atarak sonuçları JSON formatında alır ve kullanıcıya sunar.

👨‍💻 Geliştirici Notları
Filter, Memory, Scrape ve Analyze node'ları modüler olarak geliştirildi.

Her bir LLM çıktısı LangChain ile yapılandırılmıştır.

session_id sayesinde çok adımlı konuşmalar desteklenir.
| İsim              | Görev                          |
| ----------------- | ------------------------------ |
| Enes ÜLKÜ         | AI, Backend, LangChain, Gemini |
| Hüseyin Enes İPEK | Web UI, ASP.NET MVC            |

🖼 Web Arayüzü
![Web Arayüz Ekranı](https://your_image_hosting_link.com/screenshot.png)
