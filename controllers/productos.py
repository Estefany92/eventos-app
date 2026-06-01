from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required
from models.tablas import db, Producto

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if not current_user.is_authenticated:
        session['next'] = '/crear_producto'
        return redirect(url_for('auth.login'))

    if current_user.rol != 'admin':
        return "No tienes permiso"

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        precio = request.form.get('precio')

        if not nombre or not tipo or not precio:
            return "Faltan datos"

        nuevo = Producto(nombre=nombre, tipo=tipo, precio=float(precio))
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('productos.ver_productos'))
    return render_template('crear_producto.html')

@productos_bp.route('/productos')
@login_required
def ver_productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)