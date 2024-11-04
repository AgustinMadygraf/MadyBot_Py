"""
Path: src/controllers/data_controller.py
"""

import os
from flask import Blueprint, request
from marshmallow import Schema, fields, ValidationError
import google.generativeai as genai
from dotenv import load_dotenv
from src.views.data_view import render_json_response
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

load_dotenv()

# Crear un blueprint para el controlador
data_controller = Blueprint('data_controller', __name__)

# Definir el esquema de validación para los datos entrantes
class DataSchema(Schema):
    """
    DataSchema es una clase que define el esquema de validación para los datos de entrada.

    Atributos:
        user_id (fields.String): Campo obligatorio que representa el ID del usuario. 
                                 Devuelve un mensaje de error si no se proporciona.
        prompt_user (fields.String): Campo obligatorio que representa el mensaje del usuario. 
                                 Debe tener una longitud máxima de 255 caracteres. 
                                 Devuelve un mensaje de error si no se proporciona 
                                 o si excede los 255 caracteres.
    """
    user_id = fields.String(required=True,
        error_messages={"required":"El campo 'user_id' es obligatorio."})
    prompt_user = fields.String(required=True,
        validate=lambda m: len(m) <= 255,
        error_messages={"required": "El campo 'prompt_user' es obligatorio.",
            "validator_failed":"El campo 'prompt_user' no debe exceder los 255 caracteres."})

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
    message_input = data['prompt_user']

    # Log de recepción exitosa
    logger.info("Received message: \n| %s", data)
    code = 200
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(model_name="gemini-1.5-flash",
            generation_config=generation_config, system_instruction="""Eres un asistente virtual de
             Madygraf Bajo Gestión Obrera, tu propósito es brindar asistencia técnica y capacitaciones
             para implementar ERP Tryton.""",)
        chat_session = model.start_chat( history=[])
        response = chat_session.send_message(message_input)
        message_output = response.text
    except Exception as e:
        message_output = response.prompt_feedback
        logger.error("Error al generar mensaje: %s", e)

    logger.info("Generated: \n| %s", message_output)
    return render_json_response(code, message_output)
