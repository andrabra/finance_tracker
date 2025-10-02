# run_all.py
import threading
import uvicorn
from main import app, API_HOST, API_PORT
from bot import main as bot_main

def run_api():
    print(f"🚀 Запуск API на {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)

def run_bot():
    print("🤖 Запуск Telegram бота...")
    bot_main()

if __name__ == "__main__":
    # API в отдельном потоке
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    # Бот в основном потоке
    run_bot()
