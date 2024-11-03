"""
Path: src/model/database_connector.py

"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class DatabaseConnector:
    """Clase para manejar la conexión a la base de datos MySQL utilizando SQLAlchemy."""
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
            pool_size=10,  # Tamaño del pool de conexiones
            max_overflow=20,  # Máximo número de conexiones adicionales
            pool_timeout=30,  # Tiempo de espera para obtener una conexión
            pool_recycle=1800  # Tiempo de vida de una conexión en segundos
        )
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Obtiene una nueva sesión de la base de datos."""
        return self.Session()

    def close_engine(self):
        """Cierra el motor de la base de datos."""
        self.engine.dispose()
