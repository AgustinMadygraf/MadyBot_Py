"""
Path: run.py
"""
import os
from flask import Flask
from dotenv import load_dotenv
from src.controllers.data_controller import data_controller
from src.model.db_setup import DatabaseManager
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")
# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Inicializar la base de datos y tablas usando DatabaseManager
db_manager = DatabaseManager()
db_manager.initialize_database()

# Registrar el blueprint del controlador
app.register_blueprint(data_controller)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    # Ejecuta el servidor Flask en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
