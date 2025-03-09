# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt и setup.py в рабочую директорию
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения в рабочую директорию
COPY . .

# Запускаем приложение с помощью uvicorn через sleep 180 секунд (чтобы сначала спарсились данные)
CMD ["sh", "-c", "sleep 180 && uvicorn main:app --host 0.0.0.0 --port 80"]