"""
Path: src/model/database_initializer.py

"""

import os
from mysql.connector import Error
from src.logs.config_logger import LoggerConfigurator
from src.model.database_connector import DatabaseConnector

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

class DatabaseInitializer:
    """Clase para inicializar la base de datos y las tablas necesarias."""

    def __init__(self, connector: DatabaseConnector, db_name=None):
        self.connector = connector
        self.db_name = db_name or os.getenv("DB_NAME")
        self.connection = None

    def initialize_database(self):
        """Inicializa la base de datos y las tablas necesarias."""
        # Conectar sin especificar una base de datos
        self.connector.database = None
        self.connection = self.connector.connect()
        if self.connection:
            try:
                self.create_database()
                # Reconectar especificando la base de datos
                self.connector.database = self.db_name
                self.connection = self.connector.connect()
                if self.connection:
                    self.create_tables()
            finally:
                self.connector.close_connection()

    def create_database(self):
        """Crea la base de datos si no existe."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            logger.info("Base de datos '%s' verificada/creada exitosamente.", self.db_name)
        except Error as e:
            logger.error("Error al crear la base de datos: %s", e)
        finally:
            try:
                cursor.close()
            except Error as e:
                logger.error("Error al cerrar el cursor: %s", e)

    def create_tables(self):
        """Crea las tablas necesarias en la base de datos."""
        try:
            cursor = self.connection.cursor()
            # Crear tabla 'usuarios'
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255),
                    email VARCHAR(255),
                    phone_number VARCHAR(20),
                    first_connection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Crear tabla 'mensajes'
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    message_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
                )
            """)
            logger.info("Tablas verificadas/creadas exitosamente.")
        except Error as e:
            logger.error("Error al crear las tablas: %s", e)
        finally:
            try:
                cursor.close()
            except Error as e:
                logger.error("Error al cerrar el cursor: %s", e)
