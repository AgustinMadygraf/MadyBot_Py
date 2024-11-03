"""
Path: src/controllers/data_controller.py
"""

from flask import Blueprint, request, jsonify
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
        return jsonify({"error": "Solicitud inválida. 'user_id' es obligatorio."}), 400
    # Asignar valores por defecto si 'message' está ausente
    message = data.get('message', 'No message provided')
    user_id = data['user_id']

    response_data = {
        "received_message": message,
        "user_id": user_id
    }
    logger.info("Received message: \n| %s", response_data)
    return render_json_response(response_data)
