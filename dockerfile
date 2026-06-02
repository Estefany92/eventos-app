# 1. Usar explícitamente la versión Debian 12 (Bookworm)
FROM python:3.10-slim-bookworm

# 2. Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Crear el directorio de trabajo
WORKDIR /app

# 4. Instalar dependencias con el nuevo estándar de seguridad de Microsoft
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    build-essential \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalar librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 6. Copiar el código
COPY . .

# 7. Exponer el puerto
EXPOSE 5000

# 8. Encender el servidor
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
