from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

# Importamos nuestros patrones de diseño
from factories.producto_factory import ProductoFactory
from repositories.producto_repository import ProductoRepository

productos_bp = Blueprint('productos', __name__)


# ==========================================
# RUTAS WEB TRADICIONALES (Para tus templates HTML)
# ==========================================

@productos_bp.route('/productos')
@login_required
def listar_productos():
    productos = ProductoRepository.obtener_todos()
    return render_template('productos.html', productos=productos)

@productos_bp.route('/crear_producto', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if current_user.rol != 'admin':
        return "No autorizado", 403

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        tipo = request.form.get('tipo')

        nuevo_producto = ProductoFactory.crear(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            tipo=tipo
        )
        ProductoRepository.guardar(nuevo_producto)

        flash("Producto creado exitosamente.")
        return redirect(url_for('productos.listar_productos'))

    return render_template('crear_producto.html')

@productos_bp.route('/eliminar_producto/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    if current_user.rol != 'admin':
        return "No autorizado", 403

    producto = ProductoRepository.obtener_por_id(id)
    ProductoRepository.eliminar(producto)

    flash("Producto eliminado.")
    return redirect(url_for('productos.listar_productos'))


# ==========================================
# RUTAS API REST (Para consumir desde React)
# ==========================================

@productos_bp.route('/api/productos', methods=['GET'])
def api_listar_productos():
    productos = ProductoRepository.obtener_todos()
    return jsonify([p.to_dict() for p in productos])


@productos_bp.route('/api/productos/<int:id>', methods=['GET'])
def api_obtener_producto(id):
    producto = ProductoRepository.obtener_por_id(id)
    return jsonify(producto.to_dict())


@productos_bp.route('/api/productos', methods=['POST'])
@login_required
def api_crear_producto():
    if current_user.rol != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json(silent=True) or {}
    if not data.get('nombre') or data.get('precio') is None:
        return jsonify({'error': 'nombre y precio son requeridos'}), 400

    nuevo_producto = ProductoFactory.crear(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion', ''),
        precio=data.get('precio'),
        tipo=data.get('tipo')
    )
    ProductoRepository.guardar(nuevo_producto)
    return jsonify(nuevo_producto.to_dict()), 201


@productos_bp.route('/api/productos/<int:id>', methods=['PUT'])
@login_required
def api_actualizar_producto(id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    producto = ProductoRepository.obtener_por_id(id)
    data = request.get_json(silent=True) or {}
    ProductoRepository.actualizar(producto, data)
    return jsonify(producto.to_dict())


@productos_bp.route('/api/productos/<int:id>', methods=['DELETE'])
@login_required
def api_eliminar_producto(id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    producto = ProductoRepository.obtener_por_id(id)
    ProductoRepository.eliminar(producto)
    return '', 204
