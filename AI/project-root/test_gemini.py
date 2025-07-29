import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash-lite")

def main():
    print("🧠 Gemini ile sohbet başlatıldı! Çıkmak için 'q' yaz.")
    
    chat = model.start_chat(history=[])
    
    while True:
        user_input = input("👤 Sen: ")
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("👋 Görüşürüz!")
            break
        
        response = chat.send_message(user_input)
        print(f"🤖 Gemini: {response.text.strip()}\n")

if __name__ == "__main__":
    main()

