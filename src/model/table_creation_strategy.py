"""
Path: src/model/table_creation_strategy.py

"""

from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class TableCreationStrategy(ABC):
    """Interfaz para estrategias de creación de tablas."""
    
    @abstractmethod
    def create_tables(self, session: Session):
        """Método para crear las tablas en la base de datos."""
        pass
