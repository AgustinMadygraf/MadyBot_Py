"""
Path: src/controllers/data_controller.py
"""

from flask import Blueprint, request, jsonify

# Crear un blueprint para el controlador
data_controller = Blueprint('data_controller', __name__)

@data_controller.route('/receive-data', methods=['POST'])
def receive_data():
    """Obtener los datos del cuerpo de la solicitud"""
    data = request.json
    message = data.get('message', 'No message provided')
    user_id = data.get('user_id', 'Unknown user')

    # Procesamiento (puedes agregar lógica aquí según tus necesidades)
    print(f"Received message: {message} from user ID: {user_id}")

    # Respuesta JSON
    response = {
        "status": "success",
        "message": "Data received successfully",
        "received_message": message,
        "user_id": user_id
    }
    return jsonify(response)
