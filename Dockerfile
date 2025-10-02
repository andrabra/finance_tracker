# Используем официальный Python
FROM python:3.11-slim

# Отключаем буферизацию stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь проект
COPY . /app

# Создаём папку для SQLite (локально)
RUN mkdir -p /app/data

# Порт для API (по умолчанию 8000 локально, 10000 на Render)
EXPOSE 8000
EXPOSE 10000

# Команда по умолчанию
# Для локалки через docker-compose можно переопределить команду
CMD ["python", "run_all.py"]
