from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'

# 🔗 CONEXIÓN A AZUREY
params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:eventos-server-estefani.database.windows.net;"
    "Database=eventosdb;"
    "Uid=adminazure;"
    "Pwd=1Rufitolindo;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params

db = SQLAlchemy(app)

#logins
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#para que es?  dice cargar usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

#ruta de registro ??
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        print("POST REGISTRO OK")  #  DEBUG

        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        rol = request.form['rol']

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password,
            rol=rol
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        print("USUARIO GUARDADO")  #  DEBUG

        return redirect(url_for('login'))

    return render_template('registro.html')

#ruta login ??
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)

            # 🔥 REDIRECCIÓN CORRECTA
            next_page = session.pop('next', None)
            return redirect(next_page or url_for('dashboard'))

        else:
            return "Credenciales incorrectas"

    return render_template('login.html')

#tablas
# tabla USUARIOS
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    rol = db.Column(db.String(20))  # cliente / admin


#tabla PRODUCTOS
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(50))  # maquinaria / comida
    precio = db.Column(db.Float)


# tabla EVENTO datos del evento
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(50))
    hora = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    estado = db.Column(db.String(50))  # pendiente / confirmado
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


#tabla DETALLE DEL EVENTO datos generales conectados con los demas
class EventoDetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer)
    horas = db.Column(db.Integer)



#ruta para agregar productos

@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():

    # 🔒 Si no está logueado
    if not current_user.is_authenticated:
        session['next'] = '/crear_producto'
        return redirect(url_for('login'))

    # 🔒 Si no es admin
    if current_user.rol != 'admin':
        return "No tienes permiso"

    # 📝 Si envía formulario
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        precio = request.form.get('precio')

        if not nombre or not tipo or not precio:
            return "Faltan datos"

        nuevo = Producto(
            nombre=nombre,
            tipo=tipo,
            precio=float(precio)
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('ver_productos'))

    # 👇 SIEMPRE DEBE HABER RETURN FINAL
    return render_template('crear_producto.html')


@app.route('/crear_evento', methods=['GET', 'POST'])
def crear_evento():

    # 🔒 Si no está logueado
    if not current_user.is_authenticated:
        session['next'] = '/crear_evento'
        return redirect(url_for('login'))

    productos = Producto.query.all()

    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        direccion = request.form['direccion']

        nuevo_evento = Evento(
            fecha=fecha,
            hora=hora,
            direccion=direccion,
            estado='pendiente',
            usuario_id=current_user.id
        )

        db.session.add(nuevo_evento)
        db.session.commit()

        return "Evento creado correctamente 🎉"

    return render_template('crear_evento.html', productos=productos)
    

#metod para ver productos
@app.route('/productos')
@login_required
def ver_productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

#dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return f"Bienvenida {current_user.nombre} ({current_user.rol})"

#logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return "Conectado a Azure 🚀"

if __name__ == '__main__':
    app.run(debug=True)

