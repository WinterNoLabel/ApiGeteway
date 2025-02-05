FROM python:3.10-slim-bullseye AS builder

WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Устанавливаем права на выполнение скриптов
RUN chmod +x utils/start_*.sh

# Устанавливаем путь для Python
ENV PYTHONPATH="/app/src"
