"""
Path: src/controllers/data_controller.py
"""

from flask import Blueprint, request
from marshmallow import ValidationError
from dotenv import load_dotenv
from src.views.data_view import render_json_response
from src.logs.config_logger import LoggerConfigurator
from src.services.data_validator import DataSchemaValidator
from src.services.response_generator import ResponseGenerator

# Configuración del logger
logger = LoggerConfigurator().configure()

load_dotenv()

# Crear un blueprint para el controlador
data_controller = Blueprint('data_controller', __name__)

# Instancias de servicios
data_validator = DataSchemaValidator()
response_generator = ResponseGenerator()

@data_controller.route('/receive-data', methods=['POST'])
def receive_data():
    "Recibe un mensaje y un ID de usuario y responde con un JSON."
    try:
        logger.info("Request JSON: \n| %s \n", request.json)
        data = data_validator.validate(request.json)
    except ValidationError as err:
        logger.warning("Error de validación en la solicitud: %s", err.messages)
        code = 400
        return render_json_response(code, "Datos inválidos en la solicitud.")

    # Procesar el mensaje de entrada y generar la respuesta
    try:
        message_output = response_generator.generate_response(data['prompt_user'])
        code = 200
    except (ConnectionError, TimeoutError) as e:
        message_output = "Error de conexión al generar la respuesta."
        logger.error("Error de conexión: %s", e)
        code = 503  # Servicio no disponible
    except RuntimeError as e:  # Ejemplo de error de ejecución específico
        message_output = "Error de ejecución en el generador de respuesta."
        logger.error("Error de ejecución: %s", e)
        code = 500
    except Exception as e:  # Captura de respaldo para errores no anticipados
        message_output = "Error desconocido en la generación de la respuesta."
        logger.error("Error no anticipado: %s", e)
        code = 500

    logger.info("Generated: \n| %s", message_output)
    return render_json_response(code, message_output)
