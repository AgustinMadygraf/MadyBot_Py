"""
Path: src/model/database_initializer.py

"""

import sqlalchemy
from src.logs.config_logger import LoggerConfigurator
from src.model.database_connector import DatabaseConnector

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

class DatabaseInitializer:
    """Clase para inicializar la base de datos y las tablas necesarias."""
    def __init__(self, connector: DatabaseConnector):
        self.connector = connector
        self.session = None

    def initialize_database(self):
        """Inicializa la base de datos y las tablas necesarias."""
        self.session = self.connector.get_session()
        try:
            self.create_tables()
        finally:
            self.session.close()

    def create_tables(self):
        """Crea las tablas necesarias en la base de datos."""
        try:
            # Crear tabla 'usuarios'
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255),
                    email VARCHAR(255),
                    phone_number VARCHAR(20),
                    first_connection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Crear tabla 'mensajes'
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    message_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
                )
            """)
            self.session.commit()
            logger.info("Tablas verificadas/creadas exitosamente.")
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.OperationalError) as e:
            self.session.rollback()
            logger.error("Error al crear las tablas: %s", e)
        finally:
            self.session.close()
