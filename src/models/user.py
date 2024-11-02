# Path: src/models/user.py

from datetime import datetime
from run import db  # Asegúrate de que 'db' está importado desde tu archivo de configuración

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def serialize(self):
        """Serializa los datos del usuario para enviarlos en respuestas JSON."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }
