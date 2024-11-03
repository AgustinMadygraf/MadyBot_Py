"""
Path: src/views/data_view.py
"""

import uuid
from datetime import datetime
from flask import jsonify

def render_json_response(data, status="success", code=200, message="", detailed=False):
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
        "status": status,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z",  # Formato UTC ISO-8601
        "request_id": str(uuid.uuid4())  # Genera un identificador único para cada solicitud
    }

    if detailed:
        response["details"] = {
            "length": len(data) if isinstance(data, (list, dict)) else None,
            "type": type(data).__name__
        }

    # Añadir un código de error si el estado es de fallo
    if status == "error":
        response["error_code"] = code

    return jsonify(response), code
