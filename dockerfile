# 1. Usar una imagen oficial de Python ligera
FROM python:3.10-slim

# 2. Configurar variables de entorno para que Python no genere basura y muestre logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Crear el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema operativo (CRÍTICO PARA LA BASE DE DATOS EN LA NUBE)
# Esto instala los certificados y el Driver ODBC 18 de Microsoft
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg2 \
    unixodbc-dev \
    build-essential \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar e instalar las librerías de Python (requirements.txt)
COPY requirements.txt .
# Nos aseguramos de instalar gunicorn aquí también por si acaso
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 6. Copiar todo el resto de tu código fuente al contenedor
COPY . .

# 7. Exponer el puerto estándar
EXPOSE 5000

# 8. Comando para encender el servidor en producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]