FROM python:3.12-slim
WORKDIR /app

# 1) deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) código
COPY . .
ENV PYTHONUNBUFFERED=1

# 3) servidor dev (ajustaremos a gunicorn luego si querés)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

