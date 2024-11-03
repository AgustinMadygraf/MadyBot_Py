"""
Path: src/model/database_initializer.py

"""

from src.logs.config_logger import LoggerConfigurator
from src.model.database_connector import DatabaseConnector
from src.model.table_creation_strategy import TableCreationStrategy

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

class DatabaseInitializer:
    """Clase para inicializar la base de datos y manejar la sesión."""
    def __init__(self, connector: DatabaseConnector, table_creator: TableCreationStrategy):
        self.connector = connector
        self.session = None
        self.table_creator = table_creator

    def initialize_database(self):
        """Inicializa la base de datos y las tablas necesarias."""
        self.session = self.connector.get_session()
        try:
            # Usar la estrategia de creación de tablas proporcionada
            self.table_creator.create_tables(self.session)
        finally:
            self.session.close()
