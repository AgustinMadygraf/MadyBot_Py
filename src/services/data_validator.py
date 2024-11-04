"""
Path: src/services/data_validator.py
Este módulo contiene un esquema de validación de datos y un validador para los datos recibidos en el controlador.
"""

from marshmallow import Schema, fields

class DataSchema(Schema):
    user_id = fields.String(required=True, error_messages={"required": "El campo 'user_id' es obligatorio."})
    prompt_user = fields.String(
        required=True,
        validate=lambda m: len(m) <= 255,
        error_messages={"required": "El campo 'prompt_user' es obligatorio.", "validator_failed": "El campo 'prompt_user' no debe exceder los 255 caracteres."}
    )

class DataSchemaValidator:
    def __init__(self):
        self.schema = DataSchema()

    def validate(self, data):
        "Valida los datos usando el esquema."
        return self.schema.load(data)
