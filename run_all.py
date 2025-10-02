# run_all.py
import threading
import uvicorn
from main import app, API_HOST, API_PORT
from bot import main as bot_main

# Импортируем скрипт добавления пользователей
from helpers import add_user

def run_api():
    print(f"🚀 Запуск API на {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)

def run_bot():
    print("🤖 Запуск Telegram бота...")
    bot_main()

if __name__ == "__main__":
    # 1️⃣ Добавляем пользователей в базу
    print("👥 Добавляем пользователей перед стартом API и бота...")
    add_user.main()  # вызывает функцию main() из helpers/add_user.py

    # 2️⃣ Запускаем API в отдельном потоке
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    # 3️⃣ Запускаем Telegram бота в основном потоке
    run_bot()
