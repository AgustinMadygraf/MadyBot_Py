
"""
# Path: src/model/database_connector_interface.py
Este archivo define la interfaz DatabaseConnectorInterface, 
que es una interfaz para los conectores de bases de datos.
"""
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class DatabaseConnectorInterface(ABC):
    """Interfaz para los conectores de bases de datos."""
    @abstractmethod
    def get_session(self) -> Session:
        """Obtiene una nueva sesión de la base de datos."""
        pass

    @abstractmethod
    def close_engine(self):
        """Cierra el motor de la base de datos."""
        pass
