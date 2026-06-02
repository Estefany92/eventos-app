from flask import Flask
from flask_login import LoginManager
from flask import redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from models.tablas import db, Usuario
from controllers.auth import auth_bp
from controllers.productos import productos_bp
from controllers.eventos import eventos_bp
from controllers.reportes import reportes_bp 



app = Flask(__name__)
app.config.from_object(Config)

# Inicializamos Base de Datos
db.init_app(app)

# Configuración de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Apuntamos al blueprint

@login_manager.user_loader
def load_user(user_id):
    # Usamos db.session.get para asegurar que buscamos en la DB actual
    return db.session.get(Usuario, int(user_id))

# 🔥 REGISTRAMOS LOS CONTROLADORES (Blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(eventos_bp)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('eventos.dashboard'))
    
    # Si no ha iniciado sesión, va al login
    return redirect(url_for('auth.login'))
    # En lugar de texto plano, redirigimos al login
    
app.register_blueprint(reportes_bp) 

if __name__ == '__main__':
    app.run(debug=True)
