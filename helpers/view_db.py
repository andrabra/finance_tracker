# view_db.py
import sqlite3
import os

def view_database():
    """Просмотр содержимого базы данных"""
    
    if not os.path.exists('expense_tracker.db'):
        print("❌ База данных не найдена!")
        return
    
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    print("📊 СОДЕРЖИМОЕ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    # Получаем список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"📋 Найдено таблиц: {len(tables)}")
    
    for table in tables:
        table_name = table[0]
        print(f"\n🗂️ ТАБЛИЦА: {table_name}")
        print("-" * 30)
        
        # Получаем структуру таблицы
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print(f"Структура: {', '.join(column_names)}")
        
        # Получаем данные из таблицы
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if rows:
            print(f"📝 Записей: {len(rows)}")
            for i, row in enumerate(rows, 1):
                print(f"{i}. {row}")
        else:
            print("📭 Таблица пуста")
    
    conn.close()

def view_users_detailed():
    """Детальный просмотр пользователей"""
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    print("\n👥 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЯХ")
    print("=" * 60)
    
    cursor.execute('''
        SELECT id, telegram_id, name, spreadsheet_id, api_key, created_at 
        FROM users
    ''')
    
    users = cursor.fetchall()
    
    if not users:
        print("❌ Пользователи не найдены")
        return
    
    for user in users:
        print(f"\n👤 ПОЛЬЗОВАТЕЛЬ ID: {user[0]}")
        print(f"   Telegram ID: {user[1]}")
        print(f"   Имя: {user[2]}")
        print(f"   Google Sheets ID: {user[3]}")
        print(f"   API Key: {user[4]}")
        print(f"   Дата создания: {user[5]}")
    
    conn.close()

if __name__ == "__main__":
    view_database()
    view_users_detailed()