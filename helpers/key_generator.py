from google.oauth2 import service_account
from google.auth.transport.requests import Request
import google.auth

# Путь к вашему JSON файлу
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    
    # Получаем access token
    credentials.refresh(Request())
    
    print("Access Token:", credentials.token)
    return credentials.token

if __name__ == "__main__":
    get_access_token()