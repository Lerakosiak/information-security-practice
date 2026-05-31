# Dockerfile — Оптимізована безпечна версія
FROM python:3.11-slim

# Створюємо non-root користувача для безпеки
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Спочатку копіюємо залежності та встановлюємо їх для системи
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код додатку та скрипти
COPY ./app ./app
COPY ./scripts ./scripts
COPY ./alembic ./alembic
COPY alembic.ini .

# Налаштовуємо права доступу суворо для appuser
RUN mkdir -p /app/data && chown -R appuser:appuser /app

# Перемикаємося на обмеженого користувача
USER appuser

# Автоматична перевірка працездатності (Health Check)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')" || exit 1

EXPOSE 8000

# Запуск веб-сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]