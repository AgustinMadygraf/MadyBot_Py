"""
Path: src/model/database_connector.py

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
