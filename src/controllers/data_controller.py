"""
Path: src/controllers/data_controller.py
"""
from flask import Blueprint, request
from src.views.data_view import render_json_response
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()

# Crear un blueprint para el controlador
data_controller = Blueprint('data_controller', __name__)

@data_controller.route('/receive-data', methods=['POST'])
def receive_data():
    """Recibe un mensaje y un ID de usuario y responde con un JSON."""
    data = request.json

    # Validación de la presencia de 'user_id'
    if 'user_id' not in data:
        logger.warning("Solicitud sin 'user_id'. Respuesta con error 400.")
        return render_json_response({"error": "Solicitud inválida. 'user_id' es obligatorio."},
                                    status="error", code=400)

    # Validación del tipo de 'user_id'
    if not isinstance(data['user_id'], str):
        logger.warning("El 'user_id' no es una cadena. Respuesta con error 400.")
        return render_json_response({"error": "Solicitud inválida. 'user_id' debe ser una cadena."},
                                    status="error", code=400)

    # Validación de la presencia de 'message'
    if 'message' not in data:
        logger.warning("Solicitud sin 'message'. Respuesta con error 400.")
        return render_json_response({"error": "Solicitud inválida. 'message' es obligatorio."},
                                    status="error", code=400)

    # Validación del tipo de 'message'
    if not isinstance(data['message'], str):
        logger.warning("El 'message' no es una cadena. Respuesta con error 400.")
        return render_json_response({"error": "Solicitud inválida. 'message' debe ser una cadena."},
                                    status="error", code=400)

    # Validación de la longitud de 'message'
    if len(data['message']) > 255:
        logger.warning("El 'message' es demasiado largo. Respuesta con error 400.")
        return render_json_response({"error":
            "Solicitud inválida. 'message' no debe exceder los 255 caracteres."},
            status="error", code=400)
    message = data['message']
    user_id = data['user_id']

    response_data = {
        "received_message": message,
        "user_id": user_id
    }

    logger.info("Received message: \n| %s", response_data)
    return render_json_response(response_data, detailed=True)
