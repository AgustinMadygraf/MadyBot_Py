import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def init_db():
    """Inicializa la base de datos y las tablas necesarias si no existen."""
    try:
        # Conexión inicial sin especificar la base de datos para crearla si es necesario
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Verificar si la base de datos existe; si no, crearla
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
            print("Base de datos verificada/creada exitosamente.")
        
        # Conectar ahora especificando la base de datos para crear las tablas
        connection.database = os.getenv("DB_NAME")
        
        # Crear tabla usuarios si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                email VARCHAR(255),
                phone_number VARCHAR(20),
                first_connection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla mensajes si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
            )
        """)
        
        print("Tablas verificadas/creadas exitosamente.")

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
