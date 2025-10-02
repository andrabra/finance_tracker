# database.py
import sqlite3
from datetime import datetime

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            spreadsheet_id TEXT NOT NULL,
            api_key TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица для хранения категорий (опционально)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            keywords TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

def add_user(telegram_id: int, name: str, spreadsheet_id: str, api_key: str):
    """Добавление пользователя"""
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (telegram_id, name, spreadsheet_id, api_key)
            VALUES (?, ?, ?, ?)
        ''', (telegram_id, name, spreadsheet_id, api_key))
        
        conn.commit()
        print(f"✅ Пользователь {name} добавлен")
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ Пользователь с telegram_id {telegram_id} уже существует")
        return False
    finally:
        conn.close()

def get_user_by_telegram_id(telegram_id: int):
    """Получение пользователя по Telegram ID"""
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, telegram_id, name, spreadsheet_id, api_key 
        FROM users WHERE telegram_id = ?
    ''', (telegram_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'telegram_id': user[1],
            'name': user[2],
            'spreadsheet_id': user[3],
            'api_key': user[4]
        }
    return None

def get_user_by_api_key(api_key: str):
    """Получение пользователя по API ключу"""
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, telegram_id, name, spreadsheet_id, api_key 
        FROM users WHERE api_key = ?
    ''', (api_key,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'telegram_id': user[1],
            'name': user[2],
            'spreadsheet_id': user[3],
            'api_key': user[4]
        }
    return None

def get_all_users():
    """Получение всех пользователей"""
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, telegram_id, name, spreadsheet_id, api_key 
        FROM users
    ''')
    
    users = []
    for row in cursor.fetchall():
        users.append({
            'id': row[0],
            'telegram_id': row[1],
            'name': row[2],
            'spreadsheet_id': row[3],
            'api_key': row[4]
        })
    
    conn.close()
    return users

# Инициализируем базу при импорте
init_db()