from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# tabla USUARIOS
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    rol = db.Column(db.String(20))  # cliente / admin
    
    # 🔥 NUEVO: Un usuario puede tener muchos eventos
    eventos = db.relationship('Evento', backref='cliente', lazy=True)


# tabla PRODUCTOS
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(50))  # maquinaria / comida
    precio = db.Column(db.Float)
    
    # 🔥 NUEVO: Conectar el producto con sus detalles de alquiler
    detalles = db.relationship('EventoDetalle', backref='producto', lazy=True)


# tabla EVENTO datos del evento
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(50))
    hora = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    estado = db.Column(db.String(50))  # pendiente / confirmado
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    # 🔥 NUEVO: Un evento tiene muchos detalles (productos seleccionados)
    detalles = db.relationship('EventoDetalle', backref='evento', lazy=True)


# tabla DETALLE DEL EVENTO (Se queda igual, los backrefs hacen el trabajo)
class EventoDetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer)
    horas = db.Column(db.Integer)