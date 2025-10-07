# 📊 Finance Tracker Bot

Telegram-бот для учёта личных расходов с интеграцией **Google Sheets**.  
Поддерживает нескольких пользователей, хранит данные в базе и синхронизирует траты с Google-таблицами.

---

## 📦 Оглавление

- [Описание](#описание)  
- [Функционал](#функционал)  
- [Структура проекта](#структура-проекта)  
- [Требования](#требования)  
- [Конфигурация окружения](#конфигурация-окружения)  
- [Шаблон .env](#шаблон-env)  
- [Запуск локально](#запуск-локально)  
- [Запуск через Docker](#запуск-через-docker)  
- [Деплой на Render](#деплой-на-render)  
- [Документация API](#документация-api)  
- [Использование бота](#использование-бота)  
- [Поддержка](#поддержка)

---

## 📝 Описание

**Finance Tracker Bot** — это удобный способ вести учёт расходов прямо в Telegram.  
Вы пишете в бота траты (например: `150 кофе`), а он сохраняет их в вашу Google-таблицу.  

Бот поддерживает несколько пользователей: у каждого своя таблица, свои расходы и API-ключ.

---

## ✅ Функционал

- 📥 Добавление расходов через бота  
- 📊 Автоматическая запись в Google Sheets  
- 👥 Поддержка нескольких пользователей (через базу и API-ключи)  
- 🔑 API для интеграции (добавление трат, создание пользователей)  
- 🩺 Healthcheck для мониторинга  
- ⚙️ Поддержка локального запуска и деплоя на Render  
- 🔔 Возможность «будить» Render через GitHub Actions или UptimeRobot  

---

## 📂 Структура проекта

```
.
├── bot.py                  # Telegram бот
├── main.py                 # API на FastAPI
├── run_all.py              # запускает API и бота вместе
├── database.py             # управление пользователями и данными
├── helpers/
│   └── add_user.py         # скрипт добавления пользователей в базу
├── requirements.txt
├── Dockerfile
├── .env.example
└── .github/workflows/
    └── ping.yml            # GitHub Actions для "пробуждения" Render
```

---

## ⚙️ Требования

- Python **3.10+**  
- Установленные зависимости:  
  ```bash
  pip install -r requirements.txt
  ```  
- Аккаунт Telegram-бота (токен от **@BotFather**)  
- Сервисный аккаунт Google (JSON-ключ) с доступом к Sheets  

---

## 🛠 Конфигурация окружения

Сначала скопируй `.env.example` → `.env`:

```bash
cp .env.example .env
```

---

## 📑 Шаблон .env

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Основной пользователь
YOUR_TELEGRAM_ID=123456789
YOUR_NAME=Andrew
YOUR_SPREADSHEET_ID=spreadsheet_id_from_google
YOUR_API_KEY=supersecretkey

# Дополнительный пользователь (пример)
VIKTORIA_TELEGRAM_ID=987654321
VIKTORIA_NAME=Viktoria
VIKTORIA_SPREADSHEET_ID=another_spreadsheet_id
VIKTORIA_API_KEY=anothersecretkey

# Настройки API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Google credentials (для Render — в одну строку)
GOOGLE_CREDENTIALS={"type":"service_account","project_id":"...","private_key":"..."}
```

---

## 🖥 Запуск локально

1. Установи зависимости:

   ```bash
   pip install -r requirements.txt
   ```

2. Добавь пользователей в базу:

   ```bash
   python helpers/add_user.py
   ```

3. Запусти всё вместе (API + бот):

   ```bash
   python run_all.py
   ```

- API → `http://localhost:8000`  
- Бот готов к приёму сообщений  

---

## 🐳 Запуск через Docker

```bash
docker build -t finance-tracker .
docker run -p 8000:8000 --env-file .env finance-tracker
```

Для локальной разработки с базой и ботом можно использовать `docker-compose`.

---

## 🌐 Деплой на Render

1. Подключи репозиторий к **Render** как Web Service.  
2. В настройках укажи:
   - **Docker environment**  
   - **Docker Command**: `python run_all.py`  
3. Добавь переменные окружения (из `.env`).  
   - `GOOGLE_CREDENTIALS` скопируй в одну строку.  
4. Деплой — и API + бот готовы 🎉  

Чтобы Render не засыпал, можно:  
- настроить GitHub Actions (см. `.github/workflows/ping.yml`),  
- или использовать UptimeRobot для пинга `/health`.

---

## 📚 Документация API

| Метод | URL             | Тело JSON                                                | Заголовки               | Описание |
|-------|-----------------|----------------------------------------------------------|--------------------------|----------|
| POST  | `/api/users`    | `{ "telegram_id":123, "name":"Andrew", "spreadsheet_id":"...", "api_key":"..." }` | —                        | Создать пользователя |
| POST  | `/api/expense`  | `{ "amount":150, "category":"еда", "description":"кофе" }` | `X-API-Key: your_key`   | Добавить расход |
| GET   | `/api/users`    | —                                                        | —                        | Список пользователей |
| GET   | `/health`       | —                                                        | —                        | Проверка статуса |

---

## 💬 Использование бота

- `/start` — запуск  
- `150 кофе` → добавит расход в категорию "кофе"  
- `/categories` — список категорий  
- `/myid` — показать свой Telegram ID  
- `/help` — помощь  

---

## 🛠 Поддержка

- Если Render засыпает — настрой GitHub Actions (см. `.github/workflows/ping.yml`)  
- Храни ключи и токены только в `.env`  
- Для продакшена можно подключить PostgreSQL вместо SQLite  

---

✍️ Автор: [@andrabra](https://github.com/andrabra)  
🚀 Pull Requests приветствуются!
