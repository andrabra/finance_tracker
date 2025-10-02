# bot.py
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import database

# Загружаем переменные окружения
load_dotenv()

# Конфигурация из .env
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_URL = os.getenv('API_URL', 'http://localhost:8000/api/expense')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = database.get_user_by_telegram_id(user_id)
    
    if not user:
        await update.message.reply_text(
            "❌ <b>Доступ запрещен</b>\n\n"
            "Вы не зарегистрированы в системе.",
            parse_mode='HTML'
        )
        return
    
    await update.message.reply_text(
        f"💰 <b>Бот для учета трат</b>\n\n"
        f"Привет, {user['name']}!\n\n"
        "Просто напишите трату в формате:\n"
        "• <code>150 кофе</code>\n"
        "• <code>300 обед</code>\n" 
        "• <code>500 такси</code>\n\n"
        "Или используйте команды:\n"
        "/categories - список категорий\n"
        "/help - помощь\n"
        "/myid - показать мой ID",
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📝 <b>Форматы ввода:</b>\n\n"
        "• <code>150 кофе</code> - добавит трату 150 руб\n"
        "• <code>500 такси работа</code> - добавит трату 500 руб\n\n"
        "💡 Категория определяется автоматически",
        parse_mode='HTML'
    )

async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /categories"""
    categories_text = (
        "📂 <b>Доступные категории:</b>\n\n"
        "• 🍕 <b>Еда</b> - кофе, обед, ужин, продукты\n"
        "• 🚗 <b>Транспорт</b> - такси, метро, бензин\n" 
        "• 🎬 <b>Развлечения</b> - кино, концерт\n"
        "• 🏠 <b>Дом</b> - коммуналка, ремонт\n"
        "• 👕 <b>Одежда</b> - одежда, обувь\n"
        "• 💊 <b>Здоровье</b> - лекарства, врач\n"
        "• ❓ <b>Прочее</b> - все остальное"
    )
    await update.message.reply_text(categories_text, parse_mode='HTML')

async def myid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для показа Telegram ID"""
    user = update.effective_user
    await update.message.reply_text(
        f"🆔 <b>Ваш Telegram ID:</b> <code>{user.id}</code>\n\n"
        f"👤 <b>Имя:</b> {user.first_name}\n"
        f"📛 <b>Username:</b> @{user.username if user.username else 'не установлен'}\n\n"
        f"💡 <i>Сообщите этот ID администратору для добавления в систему</i>",
        parse_mode='HTML'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_id = update.effective_user.id
    
    # Проверяем пользователя в базе данных
    user = database.get_user_by_telegram_id(user_id)
    if not user:
        await update.message.reply_text("❌ Доступ запрещен")
        return
    
    text = update.message.text
    if text.startswith('/'):
        return
    
    try:
        parts = text.split(' ', 1)
        if len(parts) < 2:
            await update.message.reply_text("❌ Неверный формат. Пример: 150 кофе")
            return
        
        amount = float(parts[0])
        description = parts[1].strip()
        category = categorize_expense(description)
        
        # Отправляем в API с API ключом из базы данных
        headers = {"X-API-Key": user['api_key']}
        response = requests.post(
            API_URL, 
            json={
                "amount": amount,
                "category": category,
                "description": description
            },
            headers=headers
        )
        
        if response.status_code == 200:
            await update.message.reply_text(
                f"✅ <b>Трата добавлена!</b>\n\n"
                f"💵 <b>{amount} руб</b>\n"
                f"📁 <b>{category}</b>\n" 
                f"📝 <i>{description}</i>",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text("❌ Ошибка при сохранении")
            
    except ValueError:
        await update.message.reply_text("❌ Сумма должна быть числом")
    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text("❌ Произошла ошибка")

def categorize_expense(description):
    """Определяем категорию по описанию"""
    description_lower = description.lower()
    
    categories = {
        'Еда': ['кофе', 'обед', 'ужин', 'завтрак', 'еда', 'продукты', 'столовая', 'кафе', 'ресторан'],
        'Транспорт': ['такси', 'метро', 'автобус', 'трамвай', 'бензин', 'заправка'],
        'Развлечения': ['кино', 'концерт', 'театр', 'клуб', 'бар'],
        'Дом': ['коммуналка', 'квартплата', 'электричество', 'вода', 'ремонт'],
        'Одежда': ['одежда', 'обувь', 'куртка', 'футболка'],
        'Здоровье': ['аптека', 'лекарства', 'врач', 'больница'],
        'Прочее': []
    }
    
    for category, keywords in categories.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    return 'Прочее'

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    print(f"Ошибка в боте: {context.error}")

def main():
    # Проверяем что токен бота установлен
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == 'your_telegram_bot_token_here':
        print("❌ TELEGRAM_BOT_TOKEN не установлен в .env файле")
        return
    
    print("🤖 Запускаем Telegram бота...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("categories", categories_command))
    application.add_handler(CommandHandler("myid", myid_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    print("✅ Бот запущен! Ожидаем сообщения...")
    application.run_polling()

if __name__ == "__main__":
    main()