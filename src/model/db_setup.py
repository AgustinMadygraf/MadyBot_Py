"""
Path: src/model/db_setup.py
Este script se encarga de inicializar la base de datos y las tablas necesarias si no existen.
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

def connect_without_db(retries=3, delay=5):
    """Establece conexión con el servidor MySQL sin especificar la base de datos.
    Intenta reconectarse en caso de fallo temporal."""
    attempt = 0
    while attempt < retries:
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
            if connection.is_connected():
                logger.info("Conexión al servidor MySQL establecida.")
                return connection
        except Error as e:
            logger.error("Error al conectar con MySQL (Intento %d): %s", attempt + 1, e)
            attempt += 1
            time.sleep(delay)  # Esperar antes de reintentar
    logger.error("No se pudo establecer conexión con MySQL después de %d intentos.", retries)
    return None

def create_database(connection):
    """Crea la base de datos si no existe."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
        logger.info("Base de datos verificada/creada exitosamente.")
    except Error as e:
        logger.error("Error al crear la base de datos: %s", e)
    finally:
        cursor.close()

def create_tables(connection):
    """Crea las tablas necesarias en la base de datos."""
    try:
        connection.database = os.getenv("DB_NAME")
        cursor = connection.cursor()
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
        cursor.close()

def init_db():
    """Inicializa la base de datos y las tablas necesarias si no existen."""
    connection = connect_without_db()
    if connection:
        try:
            create_database(connection)
            create_tables(connection)
        finally:
            if connection.is_connected():
                connection.close()
                logger.info("Conexión con el servidor MySQL cerrada.")
