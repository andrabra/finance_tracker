# Expense Tracker Bot

Telegram бот для учета личных расходов с интеграцией Google Sheets.

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 2. Настройка окружения
Скопируйте и настройте .env файл
```bash
cp .env.example .env
```

Заполните .env своими данными:

- TELEGRAM_BOT_TOKEN - токен от @BotFather
- YOUR_TELEGRAM_ID - ваш Telegram ID (узнайте через /myid)
- SPREADSHEET_ID - ID вашей Google таблицы

### 3. Настройка Google Sheets
1. Создайте Google таблицу
2. Дайте доступ сервисному аккаунту (из service_account.json)
3. Укажите ID таблицы в .env

### 4. Запуск

```bash
# Добавьте пользователей
python helpers/add_user.py

# Запустите API сервер
python main.py

# Запустите бота (в отдельном терминале)
python bot.py
```

### 💬 Использование бота
- Добавление траты: 150 кофе
- Просмотр категорий: /categories
- Помощь: /help
- Мой ID: /myid