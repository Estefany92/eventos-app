from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120))
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default="cliente")

    eventos = db.relationship(
        "Evento",
        back_populates="usuario",
        lazy=True
    )

# tabla PRODUCTOS
class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    precio = db.Column(db.Float)
    
    detalles = db.relationship('EventoDetalle', back_populates="producto", lazy=True)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre, 'tipo': self.tipo, 'precio': float(self.precio)}


# tabla EVENTO
class Evento(db.Model):
    __tablename__ = "evento"

    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    estado = db.Column(db.String(20))

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id")
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="eventos"
    )

    detalles = db.relationship(
        "EventoDetalle",
        back_populates="evento",
        cascade="all, delete-orphan"
    )


# tabla DETALLE DEL EVENTO
class EventoDetalle(db.Model):
    __tablename__ = 'evento_detalle'
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer)
    horas = db.Column(db.Integer)
    producto = db.relationship(
        "Producto",
        back_populates="detalles"
    )

    evento = db.relationship(
        "Evento",
        back_populates="detalles"
    )
    
    def to_dict(self):
        return {
            'id': self.id, 
            'evento_id': self.evento_id, 
            'producto_id': self.producto_id, 
            'cantidad': self.cantidad, 
            'horas': self.horas
        }