"""
Path: run.py
"""

import os
from flask import Flask
from src.controllers.data_controller import data_controller
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from src.model.db_setup import init_db  # Importar el nuevo módulo de inicialización de la base de datos
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")
# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Inicializar la base de datos y tablas
init_db()

# Registrar el blueprint del controlador
app.register_blueprint(data_controller)

if __name__ == '__main__':
    # Ejecuta el servidor Flask en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
