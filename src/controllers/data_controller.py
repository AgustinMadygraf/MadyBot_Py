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
    """
    DataSchema es una clase que define el esquema de validación para los datos de entrada.

    Atributos:
        user_id (fields.String): Campo obligatorio que representa el ID del usuario. 
                                 Devuelve un mensaje de error si no se proporciona.
        message (fields.String): Campo obligatorio que representa el mensaje del usuario. 
                                 Debe tener una longitud máxima de 255 caracteres. 
                                 Devuelve un mensaje de error si no se proporciona 
                                 o si excede los 255 caracteres.
    """
    user_id = fields.String(required=True,
        error_messages={"required":"El campo 'user_id' es obligatorio."})
    message = fields.String(required=True,
        validate=lambda m: len(m) <= 255,
        error_messages={"required": "El campo 'message' es obligatorio.",
            "validator_failed":"El campo 'message' no debe exceder los 255 caracteres."})

# Instanciar el esquema
data_schema = DataSchema()

@data_controller.route('/receive-data', methods=['POST'])
def receive_data():
    """
    Recibe un mensaje y un ID de usuario y responde con un JSON.
    Este método realiza las siguientes acciones:
    1. Valida y deserializa los datos de entrada utilizando `data_schema`.
    2. Si hay un error de validación, lo registra y responde con los detalles del error.
    3. Extrae los valores validados del mensaje y el ID de usuario.
    4. Responde con un JSON que contiene el mensaje recibido y el ID de usuario.
    5. Registra la recepción exitosa del mensaje.
    Returns:
        JSON: Una respuesta JSON que contiene el mensaje recibido y el ID de usuario, 
        o detalles de errores de validación si los datos de entrada son inválidos.
    """
    try:
        logger.info("Request JSON: \n| %s \n", request.json)
        data = data_schema.load(request.json)
    except ValidationError as err:
        logger.warning("Error de validación en la solicitud: %s", err.messages)
        code = 400
        message_output = "Datos inválidos en la solicitud."
        return render_json_response(code, message_output)
    # Extraer valores validados
    message_input = data['message']

    # Log de recepción exitosa
    logger.info("Received message: \n| %s", data)
    code = 200
    message_output = generacion_de_respuesta(message_input)
    return render_json_response(code, message_output)


def generacion_de_respuesta(message_input):
    """
    Genera una respuesta aleatoria basada en el mensaje de entrada.
    """
    message_output = f"Respuesta generada para el mensaje: {message_input}"
    logger.info("Generated response: \n| %s", message_output)
    
    return message_output
