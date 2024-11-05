# MadyBotPy/Dockerfile
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la aplicación
COPY . .

# Instala pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Instala las dependencias usando Pipfile
RUN pipenv install --system --deploy

# Establece variables de entorno
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expone el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]