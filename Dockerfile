# users-api/Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# deps del sistema para psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

# Variables esperadas por settings.py (las pondrás vía env/ConfigMap/Secret)
# DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT
# NOTIFY_URL, SECRET_KEY, DJANGO_ALLOWED_HOSTS

EXPOSE 8000

# collectstatic si lo necesitás (no suele hacer falta en API pura)
# RUN python manage.py collectstatic --noinput

# Migraciones en entrypoint (opcional) o en un Job aparte
CMD ["/bin/sh", "-lc", "python manage.py migrate && gunicorn proyecto.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60"]
