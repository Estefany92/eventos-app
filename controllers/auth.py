from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.tablas import db, Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('eventos.dashboard'))
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        rol = request.form['rol']

        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            flash("Ese correo ya está registrado. Por favor, inicia sesión.")
            return redirect(url_for('auth.registro'))

        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("¡Registro exitoso! Ahora puedes iniciar sesión.")
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('eventos.dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
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


# ==========================================
# RUTAS API (JSON) - Para que React inicie sesión
# ==========================================

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.password, password):
        login_user(usuario)  # Flask-Login guarda la sesión en una cookie
        return jsonify(usuario.to_dict())

    return jsonify({'error': 'Credenciales incorrectas'}), 401


@auth_bp.route('/api/registro', methods=['POST'])
def api_registro():
    data = request.get_json(silent=True) or {}
    nombre = (data.get('nombre') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    rol = data.get('rol', 'cliente')

    if not nombre or not email or not password:
        return jsonify({'error': 'nombre, email y password son requeridos'}), 400

    if len(password) < 6:
        return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'Ese correo ya está registrado'}), 409

    if Usuario.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'Ese nombre de usuario ya está en uso'}), 409

    # Por seguridad, nunca confiamos en que el cliente se auto-asigne "admin"
    if rol not in ('cliente',):
        rol = 'cliente'

    nuevo_usuario = Usuario(
        nombre=nombre,
        email=email,
        password=generate_password_hash(password),
        rol=rol
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    login_user(nuevo_usuario)  # lo dejamos logueado de una vez
    return jsonify(nuevo_usuario.to_dict()), 201


@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return '', 204


@auth_bp.route('/api/me', methods=['GET'])
def api_me():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    return jsonify({'error': 'No autenticado'}), 401
