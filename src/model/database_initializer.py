"""
Path: src/model/database_initializer.py
Este módulo proporciona una clase para inicializar la base de datos y manejar la sesión.
"""

from src.logs.config_logger import LoggerConfigurator
from src.model.database_connector import DatabaseConnector
from src.model.table_creator import TableCreator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

class DatabaseInitializer:
    """Clase para inicializar la base de datos y manejar la sesión."""
    def __init__(self, connector: DatabaseConnector):
        self.connector = connector
        self.session = None
        self.table_creator = TableCreator()  # Instancia de TableCreator

    def initialize_database(self):
        """Inicializa la base de datos y las tablas necesarias."""
        self.session = self.connector.get_session()
        try:
            # Delegación de la creación de tablas a TableCreator
            self.table_creator.create_tables(self.session)
        finally:
            self.session.close()
