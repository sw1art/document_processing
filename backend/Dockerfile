FROM python:3.13.9-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости ОС для Tesseract / LibreOffice / PDF
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    poppler-utils \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app

# PYTHONPATH для абсолютных импортов backend.*
ENV PYTHONPATH=/app

# Команда запуска
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
