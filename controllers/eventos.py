from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.tablas import db, Evento, Producto, EventoDetalle

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/dashboard')
@login_required
def dashboard():
    # Si es admin ve todos, si es cliente ve solo los suyos
    if current_user.rol == 'admin':
        lista_eventos = Evento.query.all()
    else:
        lista_eventos = Evento.query.filter_by(usuario_id=current_user.id).all()
        
    return render_template('dashboard.html', eventos=lista_eventos)

@eventos_bp.route('/crear_evento', methods=['GET', 'POST'])
@login_required
def crear_evento():
    if request.method == 'POST':
        # Guardamos el evento principal
        nuevo_evento = Evento(
            fecha=request.form['fecha'],
            hora=request.form['hora'],
            direccion=request.form['direccion'],
            estado='pendiente',
            usuario_id=current_user.id
        )
        db.session.add(nuevo_evento)
        db.session.flush() # Obliga a Azure a darnos el ID del evento antes de hacer el commit final

        # Guardamos los detalles/productos
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
        flash("¡Tu evento ha sido creado y guardado con éxito!")
        return redirect(url_for('eventos.dashboard'))
        
    productos = Producto.query.all()
    return render_template('crear_evento.html', productos=productos)

@eventos_bp.route('/eliminar_evento/<int:id>', methods=['POST'])
@login_required
def eliminar_evento(id):
    if current_user.rol != 'admin':
        return "No autorizado", 403
    
    evento = Evento.query.get_or_404(id)
    # Borramos primero los servicios hijos para que la base de datos no dé error de relación
    EventoDetalle.query.filter_by(evento_id=id).delete()
    # Luego borramos el evento padre
    db.session.delete(evento)
    db.session.commit()
    
    flash("Evento eliminado correctamente.")
    return redirect(url_for('eventos.dashboard'))

@eventos_bp.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    if current_user.rol != 'admin':
        return "No autorizado", 403
    
    evento = Evento.query.get_or_404(id)
    productos = Producto.query.all() 
    
    if request.method == 'POST':
        # 1. Actualizamos todos los datos básicos del evento
        evento.fecha = request.form['fecha']
        evento.hora = request.form['hora']
        evento.direccion = request.form['direccion']
        evento.estado = request.form['estado']
        
        # 2. Actualizamos los servicios (Borramos los viejos de este evento)
        EventoDetalle.query.filter_by(evento_id=evento.id).delete()
        
        # 3. Guardamos la nueva selección
        productos_ids = request.form.getlist('productos')
        for p_id in productos_ids:
            cantidad = request.form.get(f'cantidad_{p_id}', 1)
            horas = request.form.get(f'horas_{p_id}', 1)
            
            nuevo_detalle = EventoDetalle(
                evento_id=evento.id,
                producto_id=int(p_id),
                cantidad=int(cantidad),
                horas=int(horas)
            )
            db.session.add(nuevo_detalle)
        
        db.session.commit()
        flash("¡El evento ha sido actualizado por completo!")
        return redirect(url_for('eventos.dashboard'))
        
    return render_template('editar_evento.html', evento=evento, productos=productos)