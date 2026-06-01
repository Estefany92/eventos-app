from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required
from models.tablas import db, Evento, EventoDetalle, Producto

eventos_bp = Blueprint('eventos', __name__)

@eventos_bp.route('/dashboard')
@login_required
def dashboard():
    # Si es el administrador, ve TODOS los eventos de la empresa
    if current_user.rol == 'admin':
        lista_eventos = Evento.query.all()
    # Si es un cliente, ve SOLAMENTE sus propios eventos
    else:
        lista_eventos = Evento.query.filter_by(usuario_id=current_user.id).all()
        
    return render_template('dashboard.html', eventos=lista_eventos)

@eventos_bp.route('/crear_evento', methods=['GET', 'POST'])
def crear_evento():
    if not current_user.is_authenticated:
        session['next'] = '/crear_evento'
        return redirect(url_for('auth.login'))

    productos = Producto.query.all()

    if request.method == 'POST':
        productos_ids = request.form.getlist('productos')
        if not productos_ids:
            flash("Debes seleccionar al menos un producto para el evento.")
            return redirect(url_for('eventos.crear_evento'))
        fecha = request.form['fecha']
        hora = request.form['hora']
        direccion = request.form['direccion']

        nuevo_evento = Evento(
            fecha=fecha, hora=hora, direccion=direccion,
            estado='pendiente', usuario_id=current_user.id
        )
        db.session.add(nuevo_evento)
        db.session.commit()

        productos_ids = request.form.getlist('productos')
        for pid in productos_ids:
            cantidad = request.form.get(f'cantidad_{pid}')
            horas = request.form.get(f'horas_{pid}')

            detalle = EventoDetalle(
                evento_id=nuevo_evento.id, producto_id=int(pid),
                cantidad=int(cantidad), horas=int(horas)
            )
            db.session.add(detalle)
        db.session.commit()

        return "Evento con productos guardado 🎉"
    return render_template('crear_evento.html', productos=productos)

@eventos_bp.route('/eliminar_evento/<int:id>', methods=['POST'])
@login_required
def eliminar_evento(id):
    if current_user.rol != 'admin':
        return "No autorizado", 403
    
    evento = Evento.query.get_or_404(id)
    # Primero eliminamos los detalles asociados
    EventoDetalle.query.filter_by(evento_id=id).delete()
    # Luego el evento
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for('eventos.dashboard'))

@eventos_bp.route('/editar_evento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_evento(id):
    if current_user.rol != 'admin':
        return "No autorizado", 403
    
    evento = Evento.query.get_or_404(id)
    # Necesitamos todos los productos para listarlos en el formulario
    productos = Producto.query.all() 
    
    if request.method == 'POST':
        # 1. GUARDAMOS LOS DATOS GENERALES
        evento.fecha = request.form['fecha']
        evento.hora = request.form['hora']
        evento.direccion = request.form['direccion']
        evento.estado = request.form['estado']
        
        # 2. ACTUALIZAMOS LOS SERVICIOS
        # Primero borramos el registro viejo de servicios de este evento
        EventoDetalle.query.filter_by(evento_id=evento.id).delete()
        
        # Luego leemos qué seleccionó el admin ahora y los guardamos
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
        
        # Confirmamos los cambios en Azure
        db.session.commit()
        flash("¡El evento ha sido actualizado por completo!")
        return redirect(url_for('eventos.dashboard'))
        
    return render_template('editar_evento.html', evento=evento, productos=productos)