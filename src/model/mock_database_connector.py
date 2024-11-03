"""
# Path: src/model/mock_database_connector.py
Este archivo define un mock del conector de base de datos para entornos de prueba.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.model.database_connector_interface import DatabaseConnectorInterface
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

class MockDatabaseConnector(DatabaseConnectorInterface):
    """Mock del conector de base de datos para entornos de prueba."""
    def __init__(self):
        # Base de datos en memoria para pruebas
        self.engine = create_engine("sqlite:///:memory:", echo=True)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("MockDatabaseConnector usando SQLite en memoria para pruebas.")

    def get_session(self) -> Session:
        """Obtiene una nueva sesión de la base de datos en memoria."""
        return self.Session()

    def close_engine(self):
        """Cierra el motor de la base de datos."""
        self.engine.dispose()
