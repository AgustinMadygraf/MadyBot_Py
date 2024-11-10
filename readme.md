# MadyBotPy

**MadyBotPy** es una aplicación de servidor desarrollada con Flask para recibir y procesar datos JSON a través de endpoints RESTful.

## Estructura del Proyecto

```plaintext
MadyBotPy/
│
├── run.py                          # Archivo principal para iniciar la aplicación Flask
├── docs/
│   └── 00-Prompt-for-ProjectAnalysis.md
├── src/
│   ├── __init__.py
│   └── controllers/
│       ├── data_controller.py      # Controlador con endpoint para recibir datos
│       └── __pycache__/
└── __pycache__/
```

## Requisitos Previos

1. **Python 3.7 o superior**.
2. **Pip** para la gestión de paquetes de Python.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/MadyBotPy.git
   cd MadyBotPy
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para iniciar el servidor Flask, usa el siguiente comando:

```bash
python run.py
```

Esto ejecutará el servidor en `http://0.0.0.0:5000`.

## Endpoint
### `POST /receive-data`
Este endpoint permite enviar datos JSON al servidor para su procesamiento.

- **URL**: `/receive-data`
- **Método HTTP**: `POST`
- **Encabezados**: `Content-Type: application/json`
- **Cuerpo de la Solicitud**:
  ```json
  {
    "prompt_user": "Texto del mensaje",
    "user_data": {
      "id": "ID del usuario",
      "browserData": {
        "userAgent": "Agente de usuario del navegador",
        "screenResolution": "Resolución de pantalla",
        "language": "Idioma del navegador",
        "platform": "Plataforma del navegador"
      }
    },
    "stream": false
  }
  ```

#### Ejemplo de Solicitud
Puedes probar el endpoint con el siguiente comando:
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:5000/receive-data" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"prompt_user": "Hello, MadyBotPy!", "user_data": {"id": "12345", "browserData": {"userAgent": "Mozilla/5.0", "screenResolution": "1920x1080", "language": "es-ES", "platform": "Win32"}}, "stream": false}'
```

#### Ejemplo de Respuesta
Si el JSON se recibe y procesa correctamente, la respuesta será:
```json
{
  "response_MadyBot": "Texto de la respuesta generada"
}
```

#### Posibles Errores
- **400 Bad Request**: Datos inválidos en la solicitud.
  ```json
  {
    "response_MadyBot": "Datos inválidos en la solicitud."
  }
  ```
- **500 Internal Server Error**: Error desconocido en la generación de la respuesta.
  ```json
  {
    "response_MadyBot": "Error desconocido en la generación de la respuesta."
  }
  ```

## Recomendaciones para Extensiones Futuras

1. **Validación de Datos**: Agregar validación de campos `message` y `user_id`.
2. **Manejo de Errores**: Incluir respuestas de error en caso de datos faltantes o inválidos.
3. **Pruebas Unitarias**: Implementar pruebas unitarias y de integración para asegurar la funcionalidad del endpoint.

---

## Autor

**Tu Nombre** - [GitHub](https://github.com/tu_usuario)

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
