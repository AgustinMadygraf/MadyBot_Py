"""
Path: run.py

"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from src.controllers.data_controller import data_controller
from src.model.database_connector import DatabaseConnector
from src.model.database_initializer import DatabaseInitializer
from src.model.table_creator import TableCreator
from src.logs.config_logger import LoggerConfigurator
from src.services.ssl_cert_service import create_self_signed_cert

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")

# Cargar variables de entorno desde el archivo .env
try:
    logger.debug("Intentando cargar el archivo .env")
    if not load_dotenv():
        raise FileNotFoundError(".env file not found")
    logger.debug(".env file cargado correctamente")
except FileNotFoundError as e:
    logger.error("Error loading .env file: %s", e)
    logger.debug("Asegúrate de que el archivo .env existe en el directorio raíz del proyecto")
    print("Please create a .env file with the necessary environment variables.")
    exit(1)

app = Flask(__name__)
CORS(app)


# Inicializar la base de datos y las tablas
try:
    db_connector = DatabaseConnector()
    table_creator = TableCreator()
    db_initializer = DatabaseInitializer(db_connector, table_creator)
    db_initializer.initialize_database()
    logger.info("Base de datos inicializada correctamente.")
except Exception as e:
    logger.error("Error al inicializar la base de datos: %s", e)
    exit(1)

# Registrar el blueprint del controlador
try:
    app.register_blueprint(data_controller)
    logger.info("Blueprint registrado correctamente.")
except Exception as e:
    logger.error("Error al registrar el blueprint: %s", e)
    exit(1)

# Verificar y crear certificados SSL si no existen
cert_file = 'cert.pem'
key_file = 'key.pem'
if not os.path.isfile(cert_file) or not os.path.isfile(key_file):
    logger.info("Certificados SSL no encontrados. Creando nuevos certificados...")
    create_self_signed_cert(cert_file, key_file)
    logger.info("Certificados SSL creados correctamente.")

if __name__ == '__main__':
    is_https = os.getenv('IS_HTTPS', 'false').lower() == 'true'

    try:
        if is_https:
            # Iniciar el servidor HTTPS
            app.run(host='0.0.0.0', port=5000, ssl_context=(cert_file, key_file))
            logger.info("Servidor configurado para HTTPS.")
        else:
            # Iniciar el servidor HTTP
            app.run(host='0.0.0.0', port=5000)
            logger.info("Servidor configurado para HTTP.")
    except FileNotFoundError as e:
        logger.error("Error al cargar los archivos SSL: %s", e)
        print("Please ensure 'cert.pem' and 'key.pem' files are present.")
    except Exception as e:
        logger.error("Error al iniciar el servidor Flask: %s", e)