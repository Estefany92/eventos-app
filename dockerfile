# ==========================================
# ETAPA 1: Build del frontend React
# ==========================================
FROM node:20-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
RUN npm run build
# Esto genera el build en /static/react (según la config de vite original)

# ==========================================
# ETAPA 2: Backend Flask (imagen final)
# ==========================================
FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias de sistema básicas para Python y PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la app (backend)
COPY . .

# Build de React generado en la etapa 1
COPY --from=frontend-build /static/react ./static/react

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
