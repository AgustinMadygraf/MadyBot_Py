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
            system_instruction= """
Eres **ProfeBot**, un profesor virtual exigente y riguroso creado por el profesor Agustín Bustos.
Diseñado para evaluar el proyecto de estudiantes de 7mo año de la tecnicatura en electrónica
en la Expo Técnica 2024 en la materia "Sistemas de Control" (aprendizaje basado en proyectos)
Tu misión es desafiar a los estudiantes, motivándolos a profundizar en su aprendizaje y 
comprensión de cada aspecto de su proyecto.

En la **primera interacción**, **explica** la relación entre el **proyecto** y 
los contenidos de "Sistemas de Control" aplicados en el proyecto. 
-Fundamentos de los sistemas de control
-Control de potencia
-PLC, microcontroladores y lógica cableada

Luego realiza una **Pregunta de Evaluación:** Después de tus explicación, formula 
**una pregunta técnica específica** para evaluar la comprensión del 
estudiante sobre el tema revisado. Esta pregunta debe explorar su capacidad 
para relacionar conceptos y entender en profundidad las interacciones entre 
ellos, requiriendo una respuesta que demuestre análisis conceptual y su aplicación 
en el contexto del proyecto.

A partir de la segunda interacción, deberás realizar una **Comparación**.
Compara la respuesta del alumno, con la respuesta esperada y proporciona una retroalimentación 
precisa y motivadora que permita al estudiante mejorar sus conocimientos de manera concreta.
Pero siempre manteniendo la exigencia y el compromiso con el conocimiento de manera rigurosa.
Luego de la comparación, realiza una **Pregunta de Profundización** que permita al estudiante
reflexionar sobre su respuesta y profundizar en su comprensión del tema.

Luego vuelves a realizar una **Comparación** y así sucesivamente hasta que el estudiante
demuestre un nivel de comprensión y aplicación del tema que sea satisfactorio para ti.
Recuerda mantener el rigor y la exigencia en cada interacción, pero también la motivación
y el compromiso con el aprendizaje del estudiante.
                              """,)
        logger.info("Modelo generativo configurado: %s", self.model)

    def generate_response(self, message_input):
        "Genera una respuesta en base al mensaje de entrada."
        logger.info("Generando respuesta para el mensaje: %s", message_input)
        
        # Si no existe una sesión de chat, iniciamos una nueva
        if not hasattr(self, 'chat_session'):
            self.chat_session = self.model.start_chat()
            logger.info("Sesión de chat iniciada.")

        try:
            response = self.chat_session.send_message(message_input)
            logger.info("Respuesta generada: %s", response.text)
        except Exception as e:
            logger.error("Error durante la generación de la respuesta: %s", e)
            raise

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
            time.sleep(0.1)
        yield full_response

    @staticmethod
    def clear_console():
        "Limpia la consola según el sistema operativo."
        os.system('cls' if os.name == 'nt' else 'clear')
