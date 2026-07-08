import os
from flask import Flask, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user
from config import Config
from models.tablas import *
from controllers.auth import auth_bp
from controllers.productos import productos_bp
from controllers.eventos import eventos_bp
from controllers.reportes import reportes_bp

import inspect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static', 'react')

# static_folder: aquí caerá el build de React (frontend/dist copiado en el Dockerfile)
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/app")

# CORS con soporte de cookies de sesión.
# En local: React corre en :5173 y Flask en :5000, son orígenes distintos.
# En Render: React se sirve desde el MISMO servicio Flask, por lo que ni
# siquiera se dispara CORS ahí, pero dejamos el origen configurable por si acaso.
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")
CORS(app, resources={r"/api/*": {"origins": FRONTEND_ORIGIN}}, supports_credentials=True)

app.config.from_object(Config)

# Inicializamos Base de Datos
db.init_app(app)

# Configuración de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

#  REGISTRAMOS LOS CONTROLADORES (Blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(eventos_bp)
app.register_blueprint(reportes_bp)

@app.route('/')
def home():
    return redirect('/app/')


# ==========================================
# SERVIR REACT (build de producción)
# ==========================================
# La app de React vive en /app. Todo lo que no matchee una ruta de Flask
# ni un archivo estático real, cae en index.html para que React Router
# (si lo usas) resuelva la navegación del lado del cliente.

@app.route('/app')
@app.route('/app/<path:path>')
def serve_react(path=""):
    static_dir = app.static_folder
    if path and os.path.exists(os.path.join(static_dir, path)):
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, "index.html")


with app.app_context():
    print("Relaciones de Evento:")
    print(Evento.__mapper__.relationships.keys())
    # Crear las tablas automáticamente si no existen
    db.create_all()

# EL ENCENDIDO DEL SERVIDOR SIEMPRE VA AL FINAL
if __name__ == '__main__':
    app.run(debug=True)
