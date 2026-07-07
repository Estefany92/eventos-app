from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.tablas import db, Evento, Producto, EventoDetalle
from repositories.evento_repository import EventoRepository

eventos_bp = Blueprint('eventos', __name__)

# ==========================================
# RUTAS WEB (Para tus templates HTML)
# ==========================================

@eventos_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol == 'admin':
        lista_eventos = Evento.query.all()
    else:
        lista_eventos = Evento.query.filter_by(usuario_id=current_user.id).all()

    return render_template('dashboard.html', eventos=lista_eventos)

@eventos_bp.route('/crear_evento', methods=['GET', 'POST'])
@login_required
def crear_evento():
    if request.method == 'POST':
        nuevo_evento = Evento(
            fecha=request.form['fecha'],
            direccion=request.form['direccion'],
            estado='pendiente',
            usuario_id=current_user.id
        )
        db.session.add(nuevo_evento)
        db.session.flush()

        productos_ids = request.form.getlist('productos')
        for p_id in productos_ids:
            cantidad = request.form.get(f'cantidad_{p_id}', 1)
            horas = request.form.get(f'horas_{p_id}', 1)

            nuevo_detalle = EventoDetalle(
                evento_id=nuevo_evento.id,
                producto_id=int(p_id),
                cantidad=int(cantidad),
                horas=int(horas)
            )
            db.session.add(nuevo_detalle)

        db.session.commit()
        flash("¡Tu evento ha sido creado!")
        return redirect(url_for('eventos.dashboard'))

    productos = Producto.query.all()
    return render_template('crear_evento.html', productos=productos)

@eventos_bp.route('/eliminar_evento/<int:id>', methods=['POST'])
@login_required
def eliminar_evento(id):
    if current_user.rol != 'admin': return "No autorizado", 403
    evento = Evento.query.get_or_404(id)
    EventoDetalle.query.filter_by(evento_id=id).delete()
    db.session.delete(evento)
    db.session.commit()
    flash("Evento eliminado.")
    return redirect(url_for('eventos.dashboard'))

@eventos_bp.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    if current_user.rol != 'admin': return "No autorizado", 403
    evento = Evento.query.get_or_404(id)
    productos = Producto.query.all()
    if request.method == 'POST':
        evento.fecha = request.form['fecha']
        evento.direccion = request.form['direccion']
        evento.estado = request.form['estado']
        EventoDetalle.query.filter_by(evento_id=evento.id).delete()
        productos_ids = request.form.getlist('productos')
        for p_id in productos_ids:
            nuevo_detalle = EventoDetalle(evento_id=evento.id, producto_id=int(p_id))
            db.session.add(nuevo_detalle)
        db.session.commit()
        flash("¡Evento actualizado!")
        return redirect(url_for('eventos.dashboard'))
    return render_template('editar_evento.html', evento=evento, productos=productos)

# ==========================================
# RUTAS API (Para React)
# ==========================================

@eventos_bp.route('/api/eventos', methods=['GET'])
@login_required
def api_listar_eventos():
    # Ya no está abierto a todo el mundo: cada usuario ve lo suyo, admin ve todo.
    if current_user.rol == 'admin':
        eventos = EventoRepository.obtener_todos()
    else:
        eventos = EventoRepository.obtener_por_usuario(current_user.id)

    return jsonify([evento.to_dict() for evento in eventos])


@eventos_bp.route('/api/eventos/<int:id>', methods=['GET'])
@login_required
def api_obtener_evento(id):
    evento = EventoRepository.obtener_por_id(id)
    if current_user.rol != 'admin' and evento.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    return jsonify(evento.to_dict())


@eventos_bp.route('/api/eventos', methods=['POST'])
@login_required
def api_crear_evento():
    data = request.get_json(silent=True) or {}
    if not data.get('fecha') or not data.get('direccion'):
        return jsonify({'error': 'fecha y direccion son requeridos'}), 400

    nuevo_evento = EventoRepository.crear(
        fecha=data.get('fecha'),
        direccion=data.get('direccion'),
        usuario_id=current_user.id,
        hora=data.get('hora'),
        estado=data.get('estado', 'pendiente'),
        detalles=data.get('detalles', [])
    )
    return jsonify(nuevo_evento.to_dict()), 201


@eventos_bp.route('/api/eventos/<int:id>', methods=['PUT'])
@login_required
def api_actualizar_evento(id):
    evento = EventoRepository.obtener_por_id(id)
    if current_user.rol != 'admin' and evento.usuario_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403

    data = request.get_json(silent=True) or {}
    EventoRepository.actualizar(evento, data)
    return jsonify(evento.to_dict())


@eventos_bp.route('/api/eventos/<int:id>', methods=['DELETE'])
@login_required
def api_eliminar_evento(id):
    if current_user.rol != 'admin':
        return jsonify({'error': 'No autorizado'}), 403

    evento = EventoRepository.obtener_por_id(id)
    EventoRepository.eliminar(evento)
    return '', 204
