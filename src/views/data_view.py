"""
Path: src/views/data_view.py
"""

from flask import jsonify
from src.logs.config_logger import LoggerConfigurator


logger = LoggerConfigurator().configure()

def render_json_response(code, message):
    """
    Genera una respuesta JSON estándar con metadatos adicionales.
    
    :param data: Datos a incluir en la respuesta.
    :param status: Estado de la respuesta (por defecto "success").
    :param code: Código de estado HTTP (por defecto 200).
    :param message: Mensaje adicional para la respuesta.
    :param detailed: Indica si la respuesta debe ser detallada (por defecto False).
    :return: Respuesta JSON.
    """
    response = {
        "response_MadyBot": message
    }

    logger.info("response: %s", response)
    return jsonify(response), code
