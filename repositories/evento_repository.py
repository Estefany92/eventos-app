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
    def eliminar(evento):
        """Maneja la lógica de borrado en cascada de forma segura"""
        # Borramos primero los servicios hijos para que la base de datos no dé error de relación
        EventoDetalle.query.filter_by(evento_id=evento.id).delete()
        
        # Luego borramos el evento padre
        db.session.delete(evento)
        db.session.commit()