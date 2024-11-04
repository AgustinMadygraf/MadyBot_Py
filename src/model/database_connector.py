"""
Path: src/model/database_connector.py

"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv, find_dotenv
from src.logs.config_logger import LoggerConfigurator
from src.model.database_connector_interface import DatabaseConnectorInterface

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

# Cargar variables de entorno desde el archivo .env
try:
    if not find_dotenv():
        raise FileNotFoundError(".env file not found")
    load_dotenv()
except FileNotFoundError as e:
    logger.error("Error loading .env file: %s", e)
    print(".env file not found. Please create a .env file with the necessary environment variables.")
    exit()

class DatabaseConnector(DatabaseConnectorInterface):
    """Clase para manejar la conexión a la base de datos MySQL utilizando SQLAlchemy."""
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800
        )
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """Obtiene una nueva sesión de la base de datos."""
        return self.Session()

    def close_engine(self):
        """Cierra el motor de la base de datos."""
        self.engine.dispose()
