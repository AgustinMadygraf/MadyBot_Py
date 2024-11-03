"""
Path: src/model/table_creation_strategy.py

"""

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

class TableCreationStrategy(ABC):
    """Interfaz para estrategias de creación de tablas."""
    @abstractmethod
    def create_tables(self, session: Session):
        """Método para crear las tablas en la base de datos."""
        logger.debug("Creando tablas en la base de datos.")
        pass
