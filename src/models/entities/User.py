from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id=None, username='', password='', fullname=None, email=None, document_type=None, identity_number=None, role_id=1, status=1):
        self.id = id  # Cambiado de user_id a id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email
        self.document_type = document_type
        self.identity_number = identity_number
        self.role_id = role_id
        self.status = status

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)

    def get_id(self):
        """Devuelve el ID del usuario."""
        return self.id  # Asegúrate de que 'self.id' se use aquí
