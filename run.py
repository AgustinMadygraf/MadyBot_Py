"""
Path: run.py

"""

import os
from flask import Flask
from dotenv import load_dotenv
from src.controllers.data_controller import data_controller
from src.model.database_connector import DatabaseConnector
from src.model.database_initializer import DatabaseInitializer
from src.model.table_creator import TableCreator
from src.logs.config_logger import LoggerConfigurator

os.system('cls' if os.name == 'nt' else 'clear')
# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Crear una instancia de DatabaseConnector
db_connector = DatabaseConnector()

# Crear una instancia de DatabaseInitializer usando TableCreator
table_creator = TableCreator()
db_initializer = DatabaseInitializer(db_connector, table_creator)

# Inicializar la base de datos y las tablas
db_initializer.initialize_database()

# Registrar el blueprint del controlador
app.register_blueprint(data_controller)

if __name__ == '__main__':
    # Ejecuta el servidor Flask en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
