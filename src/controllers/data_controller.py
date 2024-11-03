"""
Path: src/controllers/data_controller.py
"""

from flask import Blueprint, request
from marshmallow import Schema, fields, ValidationError
from src.views.data_view import render_json_response
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

# Crear un blueprint para el controlador
data_controller = Blueprint('data_controller', __name__)

# Definir el esquema de validación para los datos entrantes
class DataSchema(Schema):
    """Esquema de validación para los datos de entrada."""
    user_id = fields.String(required=True, error_messages={"required":
                                                           "El campo 'user_id' es obligatorio."})
    message = fields.String(required=True, validate=lambda m: len(m) <= 255,
                        error_messages={"required": "El campo 'message' es obligatorio.",
                                        "validator_failed":
                                        "El campo 'message' no debe exceder los 255 caracteres."})

# Instanciar el esquema
data_schema = DataSchema()

@data_controller.route('/receive-data', methods=['POST'])
def receive_data():
    """Recibe un mensaje y un ID de usuario y responde con un JSON."""
    try:
        # Validar y deserializar los datos de entrada
        data = data_schema.load(request.json)
    except ValidationError as err:
        # Loggear el error de validación
        logger.warning("Error de validación en la solicitud: %s", err.messages)
        # Responder con los detalles de los errores de validación
        return render_json_response({
            "errors": err.messages
        }, status="error", code=400, message="Datos inválidos en la solicitud.")
    # Extraer valores validados
    message = data['message']
    user_id = data['user_id']

    # Respuesta de éxito con los datos recibidos
    response_data = {
        "received_message": message,
        "user_id": user_id
    }

    # Log de recepción exitosa
    logger.info("Received message: \n| %s", response_data)
    return render_json_response(response_data, detailed=True)
