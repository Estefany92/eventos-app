from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from models.tablas import db, Evento, Producto, EventoDetalle
from collections import defaultdict # NUEVO IMPORT

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/analitica')
@login_required
def analitica():
    if current_user.rol != 'admin':
        return "No autorizado", 403

    # 1. Ingresos
    ingresos_por_estado = db.session.query(
        Evento.estado,
        func.sum(Producto.precio * EventoDetalle.cantidad * EventoDetalle.horas).label('total')
    ).join(EventoDetalle, Evento.id == EventoDetalle.evento_id)\
     .join(Producto, EventoDetalle.producto_id == Producto.id)\
     .group_by(Evento.estado).all()

    datos_ingresos = {}
    for estado, total in ingresos_por_estado:
        datos_ingresos[estado] = float(total) if total is not None else 0.0

    # 2. Top Productos
    top_productos = db.session.query(
        Producto.nombre,
        func.sum(EventoDetalle.cantidad).label('veces_alquilado')
    ).join(EventoDetalle, Producto.id == EventoDetalle.producto_id)\
     .group_by(Producto.nombre)\
     .order_by(func.sum(EventoDetalle.cantidad).desc())\
     .limit(5).all()

    nombres_prod = []
    cantidades_prod = []
    for p in top_productos:
        nombres_prod.append(p.nombre)
        cantidades_prod.append(int(p.veces_alquilado) if p.veces_alquilado else 0)

    # 3. NUEVO: Lógica de Meses con Mayor Demanda
    eventos_todos = Evento.query.all()
    conteo_meses = defaultdict(int)

    for ev in eventos_todos:
        # Blindaje para leer la fecha sin importar si la BD la guardó como Texto o como Fecha
        if isinstance(ev.fecha, str):
            try:
                anio_mes = ev.fecha[:7] # Corta "YYYY-MM-DD" para dejar solo "YYYY-MM"
            except:
                anio_mes = "Desconocido"
        else:
            anio_mes = ev.fecha.strftime('%Y-%m')

        conteo_meses[anio_mes] += 1

    # Ordenar de mayor cantidad de eventos a menor
    meses_ordenados = sorted(conteo_meses.items(), key=lambda x: x[1], reverse=True)

    # Diccionario para traducir el número del mes a texto
    nombres_meses = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
    }

    tabla_meses = []
    for clave, cantidad in meses_ordenados:
        if clave != "Desconocido" and len(clave) == 7:
            anio, mes = clave.split('-')
            # Formatea como "Junio 2026"
            nombre_formateado = f"{nombres_meses.get(mes, mes)} {anio}"
            tabla_meses.append({
                'mes': nombre_formateado,
                'cantidad': cantidad
            })

    return render_template('reportes.html', 
                           datos_ingresos=datos_ingresos,
                           nombres_prod=nombres_prod,
                           cantidades_prod=cantidades_prod,
                           tabla_meses=tabla_meses) # Pasamos los datos a la vista