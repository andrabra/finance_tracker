FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app/data
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV DEBUG=False

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# создаём папку data прямо в контейнере
RUN mkdir -p /app/data && chown -R root:root /app

EXPOSE 8000

CMD ["python", "main.py"]
