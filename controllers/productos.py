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
    # Usamos el repositorio para consultar todo el inventario
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

        # 1. La Fábrica CREA el objeto aplicando las reglas de negocio
        nuevo_producto = ProductoFactory.crear(
            nombre=nombre, 
            descripcion=descripcion, 
            precio=precio, 
            tipo=tipo
        )

        # 2. El Repositorio GUARDA el objeto en la base de datos Azure SQL
        ProductoRepository.guardar(nuevo_producto)

        flash("Producto creado exitosamente.")
        return redirect(url_for('productos.listar_productos'))

    return render_template('crear_producto.html')

@productos_bp.route('/eliminar_producto/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    if current_user.rol != 'admin':
        return "No autorizado", 403
    
    # Buscamos y eliminamos usando el repositorio
    producto = ProductoRepository.obtener_por_id(id)
    ProductoRepository.eliminar(producto)
    
    flash("Producto eliminado.")
    return redirect(url_for('productos.listar_productos'))


# ==========================================
# RUTAS API REST (Para consumir desde React/Frontend JS)
# ==========================================

@productos_bp.route('/api/productos', methods=['GET'])
def api_listar_productos():
    # 1. Pedimos los datos al repositorio de forma limpia
    productos = ProductoRepository.obtener_todos()
    
    # 2. Transformamos los objetos complejos a diccionarios
    lista_json = [producto.to_dict() for producto in productos]
    
    # 3. Retornamos la respuesta en formato JSON puro
    return jsonify(lista_json)