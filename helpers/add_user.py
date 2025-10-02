# helpers/add_user.py
import sys
import os
from dotenv import load_dotenv

# Добавляем корневую папку в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Загружаем переменные окружения
load_dotenv()

import database

def main():
    print("👥 Добавление пользователей в систему")
    print("=" * 40)
    
    # Получаем настройки из .env
    your_telegram_id = os.getenv('YOUR_TELEGRAM_ID')
    your_name = os.getenv('YOUR_NAME')
    your_spreadsheet_id = os.getenv('YOUR_SPREADSHEET_ID')
    your_api_key = os.getenv('YOUR_API_KEY')
    
    viktoria_telegram_id = os.getenv('VIKTORIA_TELEGRAM_ID')
    viktoria_name = os.getenv('VIKTORIA_NAME')
    viktoria_spreadsheet_id = os.getenv('VIKTORIA_SPREADSHEET_ID')
    viktoria_api_key = os.getenv('VIKTORIA_API_KEY')
    
    # Проверяем что все переменные установлены
    required_vars = {
        'YOUR_TELEGRAM_ID': your_telegram_id,
        'YOUR_NAME': your_name,
        'YOUR_SPREADSHEET_ID': your_spreadsheet_id,
        'YOUR_API_KEY': your_api_key,
        'VIKTORIA_TELEGRAM_ID': viktoria_telegram_id,
        'VIKTORIA_NAME': viktoria_name,
        'VIKTORIA_SPREADSHEET_ID': viktoria_spreadsheet_id,
        'VIKTORIA_API_KEY': viktoria_api_key
    }
    
    missing_vars = [name for name, value in required_vars.items() if not value]
    if missing_vars:
        print("❌ Отсутствуют переменные в .env:")
        for var in missing_vars:
            print(f"   - {var}")
        return
    
    # Добавляем пользователей
    users_to_add = [
        {
            'telegram_id': int(your_telegram_id),
            'name': your_name,
            'spreadsheet_id': your_spreadsheet_id,
            'api_key': your_api_key
        },
        {
            'telegram_id': int(viktoria_telegram_id),
            'name': viktoria_name,
            'spreadsheet_id': viktoria_spreadsheet_id,
            'api_key': viktoria_api_key
        }
    ]
    
    for user in users_to_add:
        success = database.add_user(
            telegram_id=user['telegram_id'],
            name=user['name'],
            spreadsheet_id=user['spreadsheet_id'],
            api_key=user['api_key']
        )
        
        if success:
            print(f"✅ {user['name']} добавлен")
        else:
            print(f"⚠️ {user['name']} уже существует")
    
    print("\n📊 Текущие пользователи:")
    users = database.get_all_users()
    for user in users:
        print(f"• {user['name']} (ID: {user['telegram_id']})")

if __name__ == "__main__":
    main()