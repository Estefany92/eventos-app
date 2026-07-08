import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargamos el .env del proyecto de forma explícita
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-fallback')
    
    # DATABASE_URL es la variable estándar que inyecta Render para PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # En caso de que no haya DATABASE_URL, usamos SQLite de manera local temporalmente
        database_url = f"sqlite:///{os.path.join(BASE_DIR, 'local.db')}"
        print("ADVERTENCIA: No se encontró DATABASE_URL. Usando SQLite local.")
    
    # SQLAlchemy (desde 1.4+) requiere que la URL empiece con 'postgresql://'
    # pero Render a veces la pasa como 'postgres://'.
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False