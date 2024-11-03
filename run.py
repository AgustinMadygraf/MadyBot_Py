"""
Path: run.py
"""
import os
from flask import Flask
from dotenv import load_dotenv
from src.controllers.data_controller import data_controller
from src.model.database_connector import DatabaseConnector
from src.model.database_initializer import DatabaseInitializer
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Crear una instancia de DatabaseConnector con parámetros configurables
db_connector = DatabaseConnector(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    retries=5,
    delay=2
)

# Crear una instancia de DatabaseInitializer usando el conector
db_initializer = DatabaseInitializer(connector=db_connector, db_name=os.getenv("DB_NAME"))

# Inicializar la base de datos y las tablas
db_initializer.initialize_database()

# Registrar el blueprint del controlador
app.register_blueprint(data_controller)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    # Ejecuta el servidor Flask en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
