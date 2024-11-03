"""
Path: src/views/data_view.py
"""

import uuid
from datetime import datetime
from flask import jsonify

def render_json_response(data, status="success", code=200, message=""):
    """Genera una respuesta JSON estándar con metadatos adicionales."""
    response = {
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z",  # Formato UTC ISO-8601
        "request_id": str(uuid.uuid4())  # Genera un identificador único para cada solicitud
    }
    # Añadir un código de error si el estado es de fallo
    if status == "error":
        response["error_code"] = code

    return jsonify(response), code
