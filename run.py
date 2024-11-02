"""
Path: run.py

"""

from flask import Flask
from src.controllers.data_controller import data_controller

app = Flask(__name__)

# Registrar el blueprint del controlador
app.register_blueprint(data_controller)

if __name__ == '__main__':
    # Ejecuta el servidor Flask en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
