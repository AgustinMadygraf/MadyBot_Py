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
    message = data.get('message', 'No message provided')
    user_id = data.get('user_id', 'Unknown user')

    response_data = {
        "received_message": message,
        "user_id": user_id
    }
    logger.info("Received message: \n| %s", response_data)
    return render_json_response(response_data)
