"""
Path: src/views/data_view.py
"""

from flask import jsonify

def render_json_response(data, status="success", code=200):
    """Genera una respuesta JSON estándar."""
    response = {
        "status": status,
        "data": data
    }
    return jsonify(response), code
