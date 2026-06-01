from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.tablas import db, Usuario

# Definimos el Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        rol = request.form['rol']

        # Verificamos si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        
        if usuario_existente:
            flash("Ese correo ya está registrado. Por favor, inicia sesión.")
            return redirect(url_for('auth.registro'))

        # Creamos y guardamos el nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("¡Registro exitoso! Ahora puedes iniciar sesión.")
        return redirect(url_for('auth.login'))
        
    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Obtenemos el usuario por email
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            
            # Capturamos la página a la que quería ir (si existe)
            next_page = request.form.get('next')
            return redirect(next_page or url_for('eventos.dashboard'))
        else:
            flash("Credenciales incorrectas. Intenta de nuevo.")
            return redirect(url_for('auth.login'))
            
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('auth.login'))