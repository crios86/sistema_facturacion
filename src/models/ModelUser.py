import MySQLdb
from .entities.User import User
from werkzeug.security import  check_password_hash, generate_password_hash

class ModelUser:

    @classmethod
    def register_user(cls, conn, username, password, fullname, email, document_type, identity_number):
        """Registra un nuevo usuario en la base de datos."""
        cursor = conn.cursor()
        try:
            # Hash de la contraseña
            hashed_password = generate_password_hash(password)  # Genera el hash de la contraseña
            cursor.execute("""
                INSERT INTO users (username, password, fullname, email, document_type, identity_number, role_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, hashed_password, fullname, email, document_type, identity_number, 1, 1))  # role_id y status por defecto
            conn.commit()
            print("Usuario registrado exitosamente.")
        except MySQLdb.Error as e:
            print(f"Error al registrar el usuario: {e}")
            raise  # Lanza el error para que se gestione en app.py
        finally:
            cursor.close()



    @classmethod
    def get_by_id(cls, conn, id):
        """Obtiene un usuario por su ID."""
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
            user = cursor.fetchone()
            return User(**user) if user else None
        except MySQLdb.Error as e:
            print(f"Error al obtener el usuario: {e}")
            return None
        finally:
            cursor.close()

    @classmethod
    def login(cls, conn, user):
        """Valida el nombre de usuario y la contraseña al iniciar sesión."""
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Busca al usuario por nombre de usuario
            cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
            user_data = cursor.fetchone()

            # Si se encuentra el usuario, se procede a verificar la contraseña
            if user_data:
                # Verificación de la contraseña encriptada
                if check_password_hash(user_data['password'], user.password):
                    # Retorna una instancia del usuario si las credenciales son correctas
                    return User(
                        id=user_data['id'],  # Obtén el id de la base de datos
                        username=user_data['username'],
                        password=user_data['password'],  # Puedes dejar el hash o no incluirlo
                        fullname=user_data['fullname'],
                        email=user_data['email'],
                        document_type=user_data['document_type'],
                        identity_number=user_data['identity_number'],
                        role_id=user_data['role_id'],
                        status=user_data['status']
                    )
                else:
                    print("Contraseña incorrecta")
                    return None
            else:
                print("Usuario no encontrado")
                return None
        except MySQLdb.Error as e:
            print(f"Error al obtener el usuario: {e}")
            return None
        finally:
            cursor.close()