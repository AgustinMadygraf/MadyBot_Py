"""
Path: src/model/db_setup.py
Este script se encarga de inicializar la base de datos y las tablas necesarias si no existen,
utilizando las clases DatabaseConnector y DatabaseInitializer.
"""

import os
import time
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class DatabaseConnector:
    """Clase para manejar la conexión a la base de datos MySQL."""

    def __init__(self, host=None, user=None, password=None, port=None,
                 database=None, retries=3, delay=5):
        self.host = host or os.getenv("DB_HOST")
        self.user = user or os.getenv("DB_USER")
        self.password = password or os.getenv("DB_PASSWORD")
        self.port = port or os.getenv("DB_PORT")
        self.database = database
        self.retries = retries
        self.delay = delay
        self.connection = None

    def connect(self):
        """Establece una conexión al servidor MySQL, con manejo de reintentos."""
        attempt = 0
        while attempt < self.retries:
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    database=self.database
                )
                if self.connection.is_connected():
                    logger.info("Conexión al servidor MySQL establecida.")
                    return self.connection
            except Error as e:
                logger.error("Error al conectar con MySQL (Intento %d): %s", attempt + 1, e)
                attempt += 1
                time.sleep(self.delay)
        logger.error("No se pudo establecer conexión con MySQL después de %d intentos.",
                     self.retries)
        return None

    def close_connection(self):
        """Cierra la conexión con el servidor MySQL."""
        if self.connection and self.connection.is_connected():
            try:
                self.connection.close()
                logger.info("Conexión con el servidor MySQL cerrada.")
            except Error as e:
                logger.error("Error al cerrar la conexión con MySQL: %s", e)


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
