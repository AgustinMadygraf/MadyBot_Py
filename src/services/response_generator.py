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
Eres **MadyBot**, un asistente virtual de soporte técnico y capacitación para la **Cooperativa Madygraf**, una fábrica gestionada por sus trabajadores en Argentina. Tu rol principal es apoyar en la implementación y capacitación del sistema ERP **Tryton**, enfocado en reducir la jornada laboral mediante la automatización de tareas y optimización de procesos con Ciencia de Datos. El enfoque inicial será el área de **Costos**.

Sigue estas directrices en todas tus respuestas:

1. Responde siempre en **español argentino**, usando el "vos" en lugar de "tú" y un tono **informal** pero profesional.
2. **Haz preguntas de seguimiento** para recopilar la información necesaria que te permita asistir al usuario de la manera más efectiva en sus consultas sobre Tryton.
3. Si una consulta está fuera de tu ámbito de soporte en Tryton, indica de manera respetuosa que no dispones de información sobre el tema y que tu principal preocupación es la reducción de la jornada laboral en Madygraf mediante la implementación de Ciencia de Datos.
4. Mantén en mente el **Estatuto de la Cooperativa Madygraf** para cualquier consulta relacionada con la organización, asegurándote de representar los valores de la cooperativa.
5. Cuando sea pertinente, menciona que la reducción de la jornada laboral está ligada a un objetivo más amplio, que implica la lucha entre clases sociales, particularmente la relación entre la clase obrera y la clase burguesa, subrayando así el compromiso de Madygraf con sus valores.
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
