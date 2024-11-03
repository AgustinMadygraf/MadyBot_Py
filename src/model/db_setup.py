"""
Path: src/model/db_setup.py
Este script se encarga de inicializar la base de datos y las tablas necesarias si no existen,
utilizando una clase DatabaseManager.
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

class DatabaseManager:
    """Clase para manejar la conexión, creación de base de datos y tablas."""
    def __init__(self, retries=3, delay=5):
        self.retries = retries
        self.delay = delay
        self.connection = None

    def connect_without_db(self):
        """Establece conexión con el servidor MySQL sin especificar la base de datos."""
        attempt = 0
        while attempt < self.retries:
            try:
                self.connection = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    port=os.getenv("DB_PORT")
                )
                if self.connection.is_connected():
                    logger.info("Conexión al servidor MySQL establecida.")
                    return True
            except Error as e:
                logger.error("Error al conectar con MySQL (Intento %d): %s", attempt + 1, e)
                attempt += 1
                time.sleep(self.delay)  # Esperar antes de reintentar
        logger.error("No se pudo establecer conexión con MySQL después de %d intentos.", self.retries)
        return False

    def create_database(self):
        """Crea la base de datos si no existe."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
                logger.info("Base de datos verificada/creada exitosamente.")
            except Error as e:
                logger.error("Error al crear la base de datos: %s", e)
            finally:
                try:
                    cursor.close()
                except Error as e:
                    logger.error("Error al cerrar el cursor: %s", e)

    def create_tables(self):
        """Crea las tablas necesarias en la base de datos."""
        if self.connection:
            try:
                self.connection.database = os.getenv("DB_NAME")
                cursor = self.connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255),
                        email VARCHAR(255),
                        phone_number VARCHAR(20),
                        first_connection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
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

    def initialize_database(self):
        """Inicializa la base de datos y las tablas necesarias."""
        if self.connect_without_db():
            try:
                self.create_database()
                self.create_tables()
            finally:
                if self.connection.is_connected():
                    try:
                        self.connection.close()
                        logger.info("Conexión con el servidor MySQL cerrada.")
                    except Error as e:
                        logger.error("Error al cerrar la conexión con MySQL: %s", e)