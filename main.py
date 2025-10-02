# main.py
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv
import database

# Загружаем переменные окружения
load_dotenv()

app = FastAPI(title="Multi-User Expense Tracker API")

# Конфигурация из .env
SERVICE_ACCOUNT_FILE = 'service_account.json'
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8000'))

# Модель данных для траты
class Expense(BaseModel):
    amount: float
    category: str
    description: str

# Модель для добавления пользователя
class UserCreate(BaseModel):
    telegram_id: int
    name: str
    spreadsheet_id: str
    api_key: str

def get_google_sheet(spreadsheet_id):
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, 
            scopes=scopes
        )
        gc = gspread.authorize(creds)
        spreadsheet = gc.open_by_key(spreadsheet_id)
        sheet = spreadsheet.sheet1
        return sheet
    except Exception as e:
        print(f"❌ Ошибка подключения к таблице {spreadsheet_id}: {e}")
        return None

@app.post("/api/expense")
async def add_expense(
    expense: Expense,
    x_api_key: str = Header(..., description="API Key для аутентификации")
):
    user = database.get_user_by_api_key(x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный API ключ")
    
    sheet = get_google_sheet(user["spreadsheet_id"])
    if not sheet:
        raise HTTPException(status_code=500, detail="Google Sheets недоступна")
    
    try:
        new_row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            expense.amount,
            expense.category,
            expense.description,
            # "API",
            # user["name"]
        ]
        
        print(f"📝 {user['name']} добавляет запись: {new_row}")
        sheet.append_row(new_row)
        
        return {
            "status": "success", 
            "message": f"Трата добавлена в таблицу {user['name']}",
            "user": user["name"],
            "data": expense.model_dump()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка записи: {str(e)}")

@app.post("/api/users")
async def create_user(user_data: UserCreate):
    success = database.add_user(
        telegram_id=user_data.telegram_id,
        name=user_data.name,
        spreadsheet_id=user_data.spreadsheet_id,
        api_key=user_data.api_key
    )
    
    if success:
        return {"status": "success", "message": "Пользователь создан"}
    else:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

@app.get("/api/users")
async def get_users():
    users = database.get_all_users()
    return {"users": users}

@app.get("/health")
async def health_check():
    users = database.get_all_users()
    if users:
        first_user = users[0]
        sheet = get_google_sheet(first_user["spreadsheet_id"])
        if sheet:
            return {
                "status": "healthy", 
                "users_count": len(users),
                "database": "ok",
                "sheets": "ok"
            }
    
    return {"status": "unhealthy", "database": "error"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Запускаем Multi-User Expense Tracker API...")
    print(f"📊 Зарегистрировано пользователей: {len(database.get_all_users())}")
    print(f"🌐 Сервер запущен на {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)