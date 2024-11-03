"""
Path: src/model/models.py

"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Crear la clase base
Base = declarative_base()

# Definir los modelos
class Usuario(Base):
    """Modelo de usuarios"""
    __tablename__ = 'usuarios'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    first_connection_timestamp = Column(TIMESTAMP, default=datetime.utcnow)

class Mensaje(Base):
    """Modelo de mensajes"""
    __tablename__ = 'mensajes'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('usuarios.user_id'), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
