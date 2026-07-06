from sqlalchemy import func
from models.tablas import db, Evento, Producto, EventoDetalle
from collections import defaultdict

class AnaliticaService:
    
    @staticmethod
    def obtener_datos_ingresos():
        ingresos_por_estado = db.session.query(
            Evento.estado,
            func.sum(Producto.precio * EventoDetalle.cantidad * EventoDetalle.horas).label('total')
        ).join(EventoDetalle, Evento.id == EventoDetalle.evento_id)\
         .join(Producto, EventoDetalle.producto_id == Producto.id)\
         .group_by(Evento.estado).all()

        datos_ingresos = {}
        for estado, total in ingresos_por_estado:
            datos_ingresos[estado] = float(total) if total is not None else 0.0
            
        return datos_ingresos

    @staticmethod
    def obtener_top_productos():
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
            
        return nombres_prod, cantidades_prod

    @staticmethod
    def obtener_temporadas_demanda():
        eventos_todos = Evento.query.all()
        conteo_meses = defaultdict(int)

        for ev in eventos_todos:
            if isinstance(ev.fecha, str):
                try:
                    anio_mes = ev.fecha[:7]
                except:
                    anio_mes = "Desconocido"
            else:
                anio_mes = ev.fecha.strftime('%Y-%m')
            conteo_meses[anio_mes] += 1

        meses_ordenados = sorted(conteo_meses.items(), key=lambda x: x[1], reverse=True)
        
        nombres_meses = {
            '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
            '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
            '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
        }

        tabla_meses = []
        for clave, cantidad in meses_ordenados:
            if clave != "Desconocido" and len(clave) == 7:
                anio, mes = clave.split('-')
                nombre_formateado = f"{nombres_meses.get(mes, mes)} {anio}"
                tabla_meses.append({
                    'mes': nombre_formateado,
                    'cantidad': cantidad
                })
                
        return tabla_meses