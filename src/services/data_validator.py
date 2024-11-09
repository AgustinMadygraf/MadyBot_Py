"""
Path: src/services/data_validator.py
Este módulo contiene un esquema de validación de datos
y un validador para los datos recibidos en el controlador.
"""

from marshmallow import Schema, fields

class BrowserDataSchema(Schema):
    "Esquema de validación para los datos del navegador."
    userAgent = fields.String(required=True, error_messages={"required":
    "El campo 'userAgent' es obligatorio."})
    screenResolution = fields.String(required=True, error_messages={"required":
    "El campo 'screenResolution' es obligatorio."})
    language = fields.String(required=True, error_messages={"required":
    "El campo 'language' es obligatorio."})
    platform = fields.String(required=True, error_messages={"required":
    "El campo 'platform' es obligatorio."})

class UserDataSchema(Schema):
    "Esquema de validación para los datos del usuario."
    id = fields.String(required=True, error_messages={"required": "El campo 'id' es obligatorio."})
    browserData = fields.Nested(BrowserDataSchema, required=True, error_messages={"required":
    "El campo 'browserData' es obligatorio."})

class DataSchema(Schema):
    "Esquema de validación para los datos recibidos en el controlador."
    prompt_user = fields.String(
        required=True,
        validate=lambda m: len(m) <= 255,
        error_messages={"required": "El campo 'prompt_user' es obligatorio.", "validator_failed":
        "El campo 'prompt_user' no debe exceder los 255 caracteres."}
    )
    user_data = fields.Nested(UserDataSchema, required=True, error_messages={"required":
    "El campo 'user_data' es obligatorio."})

class DataSchemaValidator:
    "Validador de datos."
    def __init__(self):
        self.schema = DataSchema()

    def validate(self, data):
        "Valida los datos usando el esquema."
        return self.schema.load(data)
