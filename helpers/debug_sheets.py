import gspread
import os

SERVICE_ACCOUNT_FILE = 'service_account.json'

def debug_sheets():
    print("🔍 Начинаем отладку подключения...")
    
    # 1. Проверяем файл сервисного аккаунта
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Файл {SERVICE_ACCOUNT_FILE} не найден!")
        return
    
    print("✅ Файл сервисного аккаунта найден")
    
    try:
        # 2. Пробуем подключиться
        print("🔗 Подключаемся к Google Sheets API...")
        gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
        print("✅ Успешное подключение к API")
        
        # 3. Получаем список всех доступных таблиц
        print("📋 Получаем список доступных таблиц...")
        spreadsheets = gc.list_spreadsheet_files()
        
        if not spreadsheets:
            print("❌ Нет доступных таблиц!")
            print("Проверьте что сервисному аккаунту дали доступ к таблице")
            return
        
        print(f"✅ Найдено таблиц: {len(spreadsheets)}")
        
        # 4. Выводим названия всех таблиц
        print("\n📚 Доступные таблицы:")
        for i, sheet in enumerate(spreadsheets[:10]):  # первые 10
            print(f"  {i+1}. {sheet['name']} (id: {sheet['id']})")
        
        # 5. Проверяем конкретную таблицу
        target_name = "finance-tracker"  # Замените на ваше название
        print(f"\n🔎 Ищем таблицу: '{target_name}'")
        
        found = False
        for sheet in spreadsheets:
            if sheet['name'] == target_name:
                print(f"✅ Таблица найдена! ID: {sheet['id']}")
                found = True
                
                # Пробуем открыть
                try:
                    spreadsheet = gc.open_by_key(sheet['id'])
                    worksheet = spreadsheet.sheet1
                    print("✅ Успешно открыли таблицу!")
                    
                    # Пробуем прочитать данные
                    data = worksheet.get_all_values()
                    print(f"✅ Данные таблицы: {len(data)} строк")
                    if data:
                        print("Первые строки:")
                        for row in data[:3]:
                            print(f"  {row}")
                    
                except Exception as e:
                    print(f"❌ Ошибка при открытии: {e}")
                
                break
        
        if not found:
            print(f"❌ Таблица с названием '{target_name}' не найдена!")
            print("Проверьте название или дайте доступ сервисному аккаунту")
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    debug_sheets()