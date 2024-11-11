"""
Path: src/services/response_generator.py
Este módulo contiene una clase que genera respuestas utilizando un modelo de lenguaje generativo.
"""
import time
import os
import google.generativeai as genai
from src.views.data_view import render_json_response
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger
logger = LoggerConfigurator().configure()

class ResponseGenerator:
    "ResponseGenerator is a class that generates responses using the Gemini AI model."
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        logger.info("API Key obtenida: %s", self.api_key)
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction="""
                    Sos MadyBot, un asistente virtual creado para apoyar a Madygraf, 
                    una fábrica recuperada gestionada por trabajadores en Argentina. 
                    Tu propósito es brindar soporte técnico y capacitación para implementar el sistema ERP Tryton, 
                    enfocado en reducir la jornada laboral mediante la automatización de tareas repetitivas 
                    y la optimización de procesos a través de la ciencia de datos. 
                    Siempre respondé en español y usá el "vos" en lugar del "tu"
                    para adecuarte al lenguaje argentino.""",
        )
        logger.info("Modelo generativo configurado: %s", self.model)

    def generate_response(self, message_input):
        "Genera una respuesta en base al mensaje de entrada."
        logger.info("Generando respuesta para el mensaje: %s", message_input)
        chat_session = self.model.start_chat(history=[])
        logger.info("Sesión de chat iniciada.")
        response = chat_session.send_message(message_input)
        logger.info("Respuesta generada: %s", response.text)
        return response.text

    def generate_response_streaming(self, message_input, chunk_size=30):
        "Genera una respuesta en base al mensaje de entrada, en bloques de texto."
        logger.info("Generando respuesta en modo streaming para el mensaje: %s", message_input)
        chat_session = self.model.start_chat(history=[])
        logger.info("Sesión de chat iniciada.")
        response = chat_session.send_message(message_input)
        #logger.info("Respuesta generada: %s", response.text)
        offset = 0
        full_response = ""
        while offset < len(response.text):
            chunk = response.text[offset:offset+chunk_size]
            full_response += chunk
            self.clear_console()
            #print(full_response)
            render_json_response(code=200, message=full_response, stream=True)
            offset += chunk_size
            time.sleep(0.15)
        yield full_response

    @staticmethod
    def clear_console():
        "Limpia la consola según el sistema operativo."
        os.system('cls' if os.name == 'nt' else 'clear')
