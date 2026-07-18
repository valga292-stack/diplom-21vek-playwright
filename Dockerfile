FROM python:3.12-slim

WORKDIR /app

# Копируем список зависимостей и ставим бинарные сборки
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --only-binary :all:

# Скачиваем браузер Chromium для Playwright
RUN python -m playwright install --with-deps chromium

# Переносим весь наш код внутрь контейнера
COPY . .

# Команда по умолчанию для запуска тестов
CMD ["python", "-m", "pytest"
