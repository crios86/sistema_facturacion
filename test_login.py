import MySQLdb
from config import config
from src.models.entities.User import User

# Configuración de MySQL
MYSQL_HOST = config['development'].MYSQL_HOST
MYSQL_USER = config['development'].MYSQL_USER
MYSQL_PASSWORD = config['development'].MYSQL_PASSWORD
MYSQL_DB = config['development'].MYSQL_DB
MYSQL_PORT = config['development'].MYSQL_PORT

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos MySQL."""
    try:
        conn = MySQLdb.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB,
            port=MYSQL_PORT
        )
        print("Conexión a la base de datos establecida exitosamente.")
        return conn
    except MySQLdb.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

from werkzeug.security import check_password_hash

def verify_user(username, password):
    """Verifica si el usuario existe en la base de datos y devuelve sus datos."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()

            if user_data:
                print(f"Usuario encontrado: {user_data}")
                
                # Comparar la contraseña ingresada con la almacenada (encriptada)
                if check_password_hash(user_data['password'], password):
                    print("Contraseña válida")
                else:
                    print("Contraseña incorrecta")
            else:
                print("Usuario no encontrado.")
        except MySQLdb.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            conn.close()
    else:
        print("No se pudo establecer la conexión con la base de datos.")

# Parámetros de prueba
username, password = 'crios', '123'

# Ejecuta la verificación
verify_user(username, password)
