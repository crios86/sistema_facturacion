from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb

from config import config
from src.models.ModelUser import ModelUser
from src.models.entities.User import User

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

# Configuración de CSRF
app.config.from_object(config['development'])
csrf = CSRFProtect(app)

# Configuración de MySQL
MYSQL_HOST = config['development'].MYSQL_HOST
MYSQL_USER = config['development'].MYSQL_USER
MYSQL_PASSWORD = config['development'].MYSQL_PASSWORD
MYSQL_DB = config['development'].MYSQL_DB
MYSQL_PORT = config['development'].MYSQL_PORT

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    return MySQLdb.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        port=MYSQL_PORT
    )

# Configuración de Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    with get_db_connection() as conn:  # Cambia aquí
        return ModelUser.get_by_id(conn, user_id)

@app.before_first_request
def initialize_database():
    with get_db_connection() as conn:  # Cambia aquí
        try:
            cursor = conn.cursor()
            with open('database/facturacion.sql', 'r') as f:
                sql_script = f.read()
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()
            print("Base de datos y tablas creadas correctamente.")
        except Exception as ex:
            print(f"Error al inicializar la base de datos: {ex}")




@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verifica que los campos no estén vacíos
        if not username or not password:
            flash("Por favor, completa todos los campos.")
            return render_template('auth/login.html')

        # Intenta obtener la conexión a la base de datos
        try:
            with get_db_connection() as conn:
                # Crea el objeto usuario con los datos proporcionados
                user = User(username=username, password=password)
                
                # Llama al método login de ModelUser
                logged_user = ModelUser.login(conn, user)

                # Si el inicio de sesión es exitoso
                if logged_user:
                    login_user(logged_user)
                    flash(f"Bienvenido {logged_user.fullname}!")
                    return redirect(url_for('home'))
                else:
                    flash("Nombre de usuario o contraseña inválidos")
        except MySQLdb.Error as e:
            flash(f"Error en la base de datos: {e}")

    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>This is a protected view, only for authenticated users.</h1>"

# Código de registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Contraseña sin hashear
        fullname = request.form['fullname']
        email = request.form['email']
        document_type = request.form['document_type']
        identity_number = request.form['identity_number']
        
        try:
            conn = get_db_connection()  # Establece la conexión a la base de datos
            # Llama al método register_user para crear un nuevo usuario
            ModelUser.register_user(conn, username, password, fullname, email, document_type, identity_number)
            flash('Usuario registrado exitosamente!')
            return redirect(url_for('login'))
        except Exception as ex:
            flash(f"Error en el registro: {ex}")  # Mensaje de error si ocurre una excepción
            return render_template('auth/register.html')  # Muestra el formulario de registro de nuevo
        finally:
            conn.close()  # Asegúrate de cerrar la conexión siempre
    
    return render_template('auth/register.html')  # Muestra el formulario de registro en método GET



@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def status_404(error):
    return "<h1>Page not found</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)  # Para facilitar la depuración







