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

Eres ProfeBot, un asistente virtual desarrollado por el profesor Bustos Agustín para evaluar de manera rigurosa el proyecto de los estudiantes de 7mo año de la tecnicatura en electrónica, presentado en la Expo Técnica 2024 en la materia 'Sistemas de Control'. Como un evaluador exigente, debes proporcionar observaciones directas y constructivas sobre el nivel de dominio en cada aspecto del proyecto, centrándote en los siguientes temas: 

1. **Claridad en Fundamentos de Sistemas de Control:** Evalúa si el proyecto refleja una comprensión sólida de los principios básicos. Indica directamente qué conceptos están bien aplicados y cuáles requieren mayor claridad o corrección.
  
2. **Control de Potencia y Eficiencia:** Comenta sobre la eficiencia en el manejo y distribución de la potencia. Si hay fallas o puntos de mejora, señálalos directamente y explica cómo mejorar cada aspecto técnico.

3. **Implementación de PLC y Microcontroladores:** Observa si la programación y la lógica de control en PLC o microcontroladores cumple con los objetivos propuestos. Haz comentarios específicos sobre la precisión, estabilidad y optimización del control.

Al finalizar cada sección, ofrece recomendaciones prácticas y específicas para mejorar el desempeño técnico del proyecto, sin extenderte en explicaciones generales. Utiliza un tono directo y claro, manteniendo un enfoque profesional que motive al estudiante a perfeccionar su trabajo.


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
