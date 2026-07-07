from models.tablas import db, Evento, EventoDetalle


class EventoRepository:

    @staticmethod
    def obtener_todos():
        """Devuelve todos los eventos (Para el admin)"""
        return Evento.query.all()

    @staticmethod
    def obtener_por_usuario(usuario_id):
        """Devuelve solo los eventos de un cliente específico"""
        return Evento.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def obtener_por_id(evento_id):
        """Busca un evento por su ID o lanza error 404"""
        return Evento.query.get_or_404(evento_id)

    @staticmethod
    def crear(fecha, direccion, usuario_id, hora=None, estado='pendiente', detalles=None):
        """Crea un evento y sus detalles (usado por la API)"""
        nuevo_evento = Evento(
            fecha=fecha,
            hora=hora,
            direccion=direccion,
            estado=estado,
            usuario_id=usuario_id
        )
        db.session.add(nuevo_evento)
        db.session.flush()  # para obtener nuevo_evento.id antes del commit

        for d in (detalles or []):
            db.session.add(EventoDetalle(
                evento_id=nuevo_evento.id,
                producto_id=d['producto_id'],
                cantidad=d.get('cantidad', 1),
                horas=d.get('horas', 1)
            ))

        db.session.commit()
        return nuevo_evento

    @staticmethod
    def actualizar(evento, datos):
        """Actualiza campos simples de un evento (usado por la API)"""
        for campo in ('fecha', 'hora', 'direccion', 'estado'):
            if campo in datos:
                setattr(evento, campo, datos[campo])
        db.session.commit()
        return evento

    @staticmethod
    def eliminar(evento):
        """Maneja la lógica de borrado en cascada de forma segura"""
        EventoDetalle.query.filter_by(evento_id=evento.id).delete()
        db.session.delete(evento)
        db.session.commit()
