FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Esto es lo que descarga el navegador Chromium necesario para Playwright
RUN playwright install --with-deps

COPY . .

CMD gunicorn app:app --bind 0.0.0.0:$PORT
