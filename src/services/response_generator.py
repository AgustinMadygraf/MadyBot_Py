"""
Path: src/services/response_generator.py
Este módulo contiene una clase que genera respuestas utilizando un modelo de lenguaje generativo.
"""

import os
import google.generativeai as genai

class ResponseGenerator:
    "ResponseGenerator is a class that generates responses using the Gemini AI model."
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
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
            system_instruction="""Eres un asistente virtual de Madygraf Bajo Gestión Obrera,
            tu propósito es brindar asistencia técnica y capacitaciones para implementar 
            ERP Tryton.""",)

    def generate_response(self, message_input):
        "Genera una respuesta en base al mensaje de entrada."
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(message_input)
        return response.text
