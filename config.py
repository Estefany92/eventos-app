import urllib
import os
from dotenv import load_dotenv

# 👇 Esto carga las variables de tu archivo .env a la memoria
load_dotenv()

class Config:
    # 🔒 Traemos las credenciales de forma segura
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    server = os.environ.get('AZURE_SERVER')
    database = os.environ.get('AZURE_DATABASE')
    username = os.environ.get('AZURE_USER')
    password = os.environ.get('AZURE_PASSWORD')
    
    # 🔗 Armamos la conexión a Azure inyectando las variables
    params = urllib.parse.quote_plus(
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{server};"
        f"Database={database};"
        f"Uid={username};"
        f"Pwd={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    
    # URL de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
    SQLALCHEMY_TRACK_MODIFICATIONS = False