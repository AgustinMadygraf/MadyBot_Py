
## **Evaluación y Optimización de Código Python según Principios SOLID con Pruebas Automatizadas**

Analiza el siguiente código Python y proporciona una evaluación detallada de cómo se podría mejorar para cumplir con los principios SOLID. 
Identifica los problemas específicos presentes en el código y sugiere posibles soluciones para cada uno de los cinco principios SOLID: 
- Principio de Responsabilidad Única (SRP)
- Principio Abierto/Cerrado (OCP)
- Principio de Sustitución de Liskov (LSP)
- Principio de Segregación de Interfaces (ISP)
- Principio de Inversión de Dependencias (DIP)

Después de proporcionar la evaluación y las posibles soluciones, selecciona una pequeña mejora específica y propónla para implementación. 
Espera mi confirmación antes de proceder.

Una vez confirmada la mejora, proporciona el código modificado necesario y crea o modifica el archivo de pruebas correspondiente usando `pytest`, con el nombre `tests/test_[nombre_del_archivo_creado_o_modificado].py`.

Aquí está el código a evaluar:

## Estructura de Carpetas y Archivos
```bash
MadyBotPy/
    readme.md                                     2.46kB - N/A
    run.py                                        0.88kB - 019 líneas de código
    docs/
        00-Prompt-for-ProjectAnalysis.md          30.64kB - N/A
    src/
        __init__.py                               0.00kB - N/A
        controllers/
            data_controller.py                    0.82kB - 019 líneas de código
            __pycache__/
        install/
            dependency_manager.py                 4.89kB - 107 líneas de código
            project_installer.py                  4.81kB - 110 líneas de código
            project_name_utils.py                 1.48kB - 037 líneas de código
            python_interpreter_utils.py           2.58kB - 060 líneas de código
            shortcut_creation_strategy.py         2.25kB - 048 líneas de código
            docs/
            __pycache__/
        logs/
            base_filter.py                        0.33kB - 009 líneas de código
            config_logger.py                      2.08kB - 048 líneas de código
            exclude_http_logs_filter.py           0.45kB - 010 líneas de código
            info_error_filter.py                  0.49kB - 012 líneas de código
            logging.json                          1.17kB - N/A
            __init__.py                           0.00kB - N/A
            docs/
            logs/
            __pycache__/
        model/
            db_setup.py                           2.10kB - 044 líneas de código
        models/
        __pycache__/
```


## Contenido de Archivos Seleccionados

### C:\AppServ\www\MadyBotPy\readme.md
```plaintext
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
    "message": "Texto del mensaje",
    "user_id": "ID del usuario"
  }
  ```

#### Ejemplo de Respuesta

Si el JSON se recibe correctamente, la respuesta será:
```json
{
  "status": "success",
  "message": "Data received successfully",
  "received_message": "Texto del mensaje",
  "user_id": "ID del usuario"
}
```

## Ejemplo de Solicitud con cURL

Puedes probar el endpoint usando cURL:

```bash
curl -X POST http://0.0.0.0:5000/receive-data \
-H "Content-Type: application/json" \
-d '{"message": "Hello, MadyBotPy!", "user_id": "12345"}'
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

```

### C:\AppServ\www\MadyBotPy\run.py
```plaintext
"""
Path: run.py
"""

import os
from flask import Flask
from src.controllers.data_controller import data_controller
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from src.model.db_setup import init_db  # Importar el nuevo módulo de inicialización de la base de datos
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger al inicio del script
logger = LoggerConfigurator().configure()
logger.debug("Logger configurado correctamente al inicio del servidor.")
# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Inicializar la base de datos y tablas
init_db()

# Registrar el blueprint del controlador
app.register_blueprint(data_controller)

if __name__ == '__main__':
    # Ejecuta el servidor Flask en el puerto 5000
    app.run(host='0.0.0.0', port=5000)

```

### C:\AppServ\www\MadyBotPy\src\controllers\data_controller.py
```plaintext
"""
Path: src/controllers/data_controller.py
"""

from flask import Blueprint, request, jsonify

# Crear un blueprint para el controlador
data_controller = Blueprint('data_controller', __name__)

@data_controller.route('/receive-data', methods=['POST'])
def receive_data():
    """Obtener los datos del cuerpo de la solicitud"""
    data = request.json
    message = data.get('message', 'No message provided')
    user_id = data.get('user_id', 'Unknown user')

    # Procesamiento (puedes agregar lógica aquí según tus necesidades)
    print(f"Received message: {message} from user ID: {user_id}")

    # Respuesta JSON
    response = {
        "status": "success",
        "message": "Data received successfully",
        "received_message": message,
        "user_id": user_id
    }
    return jsonify(response)

```

### C:\AppServ\www\MadyBotPy\src\install\dependency_manager.py
```plaintext
"""
src/install/dependency_manager.py
Este módulo proporciona clases para la gestión de dependencias, incluyendo la actualización de pip,
la instalación de dependencias y la verificación de dependencias faltantes.
"""

import subprocess
import sys
from abc import ABC, abstractmethod

class Updater(ABC):
    """
    Interfaz para actualizadores. Define el método `update` que debe ser implementado
    por las subclases.
    """
    @abstractmethod
    def update(self) -> None:
        """Actualiza alguna herramienta o dependencia."""
        print("Actualizando...")



class PipUpdater(Updater):
    """
    Clase responsable de actualizar pip a la última versión disponible.
    Implementa la interfaz `Updater`.
    """
    def update(self) -> None:
        """
        Actualiza pip utilizando el comando `pip install --upgrade pip`.
        """
        print("Actualizando pip...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            print("pip actualizado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"No se pudo actualizar pip. Error: {e}")


class DependencyInstaller(ABC):
    """
    Interfaz para la instalación de dependencias.
    Las clases que hereden de esta deberán implementar el método `install`.
    """
    @abstractmethod
    def install(self, dependency: str) -> bool:
        """Instala una dependencia."""
        print(f"Instalando {dependency}...")


class PipDependencyInstaller(DependencyInstaller):
    """
    Clase concreta que implementa la instalación de dependencias usando pip.
    Implementa la interfaz `DependencyInstaller`.
    """
    def install(self, dependency: str) -> bool:
        """
        Instala una dependencia usando pip.

        :param dependency: Nombre de la dependencia a instalar.
        :return: True si la instalación fue exitosa, False en caso contrario.
        """
        print(f"Instalando {dependency} usando pip...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
            print(f"{dependency} instalado correctamente.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"No se pudo instalar {dependency}. Error: {e}")
            return False


class DependencyInstallerManager:
    """
    Clase responsable de instalar las dependencias faltantes.
    Ahora depende de interfaces en lugar de clases concretas.
    """
    def __init__(self, installer: DependencyInstaller, updater: Updater, max_retries: int = 3):
        """
        Inicializa la clase DependencyInstallerManager con un instalador y un actualizador.

        :param installer: Instancia de una clase que implementa la interfaz DependencyInstaller.
        :param updater: Instancia de una clase que implementa la interfaz Updater.
        :param max_retries: Número máximo de intentos para instalar cada dependencia.
        """
        self.installer = installer
        self.updater = updater
        self.max_retries = max_retries

    def install_missing_dependencies(self, requirements_file: str = 'requirements.txt') -> None:
        """
        Instala las dependencias faltantes utilizando el instalador proporcionado.
        Si una instalación falla, se reintentará hasta max_retries veces.

        :param requirements_file: Ruta al archivo requirements.txt que contiene las dependencias.
        """
        failed_dependencies = []  # Lista para almacenar dependencias que no se pudieron instalar

        print(f"Leyendo dependencias desde {requirements_file}...")

        try:
            with open(requirements_file, 'r', encoding='utf-8') as file:
                dependencies = file.read().splitlines()
        except FileNotFoundError:
            print(f"El archivo {requirements_file} no fue encontrado.")
            return

        print(f"Las siguientes dependencias están faltantes: {', '.join(dependencies)}")
        print("Intentando instalar dependencias faltantes...")

        for dep in dependencies:
            success = False
            for attempt in range(self.max_retries):
                print(f"Intentando instalar {dep} (intento {attempt + 1}/{self.max_retries})...")
                if self.installer.install(dep):
                    success = True
                    break
                print(f"Reintentando instalación de {dep}...")

            if not success:
                print(f"Fallo la instalación de {dep} después de {self.max_retries} intentos.")
                failed_dependencies.append(dep)

        if failed_dependencies:
            print("Las siguientes dependencias no pudieron ser instaladas:")
            print(", ".join(failed_dependencies))
        else:
            print("Todas las dependencias fueron instaladas exitosamente.")

```

### C:\AppServ\www\MadyBotPy\src\install\project_installer.py
```plaintext
"""
src/install/project_installer.py
Este módulo proporciona utilidades para la instalación del proyecto.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import winshell
from src.install.project_name_utils import ProjectNameRetriever
from src.install.shortcut_creation_strategy import (
    ShortcutCreationStrategy, DefaultShortcutCreationStrategy
)
from src.logs.config_logger import logger

class BaseInstaller(ABC):
    """
    Clase base abstracta que define el comportamiento de un instalador de proyectos.
    """
    @abstractmethod
    def main(self):
        """Método principal que inicia el proceso de instalación del proyecto."""
        print("Iniciando instalador...")


class ProjectInstaller(BaseInstaller):
    """
    Clase principal encargada de la instalación del proyecto.
    Implementa la interfaz BaseInstaller.
    """
    def __init__(self):
        """
        Inicializa el instalador del proyecto.
        """
        self.logger = logger  # Utiliza el logger ya configurado
        self.logger.info("Logger configurado correctamente.")
        self.project_dir = Path(__file__).parent.parent.parent.resolve()
        self.name_proj = ProjectNameRetriever(self.project_dir).get_project_name()

    def main(self):
        """
        Método principal que inicia el proceso de instalación del proyecto.
        Implementa el método `main` de la clase base.
        """
        print("Iniciando instalador")
        print(f"Directorio del script: {self.project_dir}")
        print(f"Nombre del proyecto: {self.name_proj}")

        ruta_archivo_bat = self.project_dir / f"{self.name_proj}.bat"
        print(f"Ruta del archivo BAT: {ruta_archivo_bat}")
        if not ruta_archivo_bat.is_file():
            print(f"Creando archivo '{self.name_proj}.bat'")
            bat_creator = BatFileCreator(self.project_dir, self.name_proj, self.logger)
            bat_creator.crear_archivo_bat()

        shortcut_strategy = DefaultShortcutCreationStrategy()
        ShortcutManager(
            self.project_dir, self.name_proj, self.logger, shortcut_strategy
        ).create_shortcut(ruta_archivo_bat)


class ShortcutManager:
    """
    Clase responsable de gestionar la creación de accesos directos.
    """
    def __init__(self, project_dir, name_proj, log, strategy: ShortcutCreationStrategy):
        self.project_dir = project_dir
        self.name_proj = name_proj
        self.logger = log
        self.strategy = strategy

    def verificar_icono(self, ruta_icono):
        """
        Verifica si el archivo de ícono existe.

        :param ruta_icono: Ruta al archivo de ícono.
        :return: True si el archivo existe, False en caso contrario.
        """
        if not ruta_icono.is_file():
            self.logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
            return False
        return True

    def create_shortcut(self, ruta_archivo_bat):
        """
        Crea un acceso directo en el escritorio para el archivo BAT.

        :param ruta_archivo_bat: Ruta al archivo BAT.
        :return: True si el acceso directo se creó exitosamente, False en caso contrario.
        """
        escritorio = Path(winshell.desktop())
        ruta_acceso_directo = escritorio / f"{self.name_proj}.lnk"
        ruta_icono = self.project_dir / "static" / "favicon.ico"

        if not self.verificar_icono(ruta_icono):
            return False

        return self.strategy.create_shortcut(
            ruta_acceso_directo, ruta_archivo_bat, ruta_icono, self.logger
        )


class BatFileCreator:
    """
    Clase encargada de crear archivos BAT para la ejecución del proyecto.
    """
    def __init__(self, project_dir, name_proj, log):
        self.project_dir = project_dir
        self.name_proj = name_proj
        self.logger = log

    def crear_archivo_bat(self):
        """
        Crea un archivo BAT que ejecuta el proyecto utilizando pipenv.
        """
        _ruta_app_py = self.project_dir / 'run.py'
        _ruta_archivo_bat = self.project_dir / f"{self.name_proj}.bat"

        self.logger.debug(f"Ruta del archivo run.py: {_ruta_app_py}")
        self.logger.debug(f"Ruta del archivo BAT: {_ruta_archivo_bat}")

        if not _ruta_app_py.is_file():
            self.logger.error(f"El archivo run.py no existe en la ruta: {_ruta_app_py}")
            return

        try:
            with open(_ruta_archivo_bat, 'w', encoding='utf-8') as bat_file:
                bat_file.write("@echo off\n")
                bat_file.write(f"pipenv run python {_ruta_app_py}\n")
            self.logger.info(f"Archivo BAT creado exitosamente en: {_ruta_archivo_bat}")
        except FileNotFoundError as e:
            self.logger.error(f"Error al crear el archivo BAT: {e}", exc_info=True)

```

### C:\AppServ\www\MadyBotPy\src\install\project_name_utils.py
```plaintext
"""
src/install/project_name_utils.py
Este módulo proporciona la clase ProjectNameRetriever, 
que es responsable de obtener el nombre del proyecto
basado en el nombre del directorio principal.
"""

from pathlib import Path

class ProjectNameRetriever:
    """
    Clase responsable de obtener el nombre del proyecto basado en el nombre del directorio principal 
    o un archivo específico.
    """
    def __init__(self, project_dir: Path = None):
        """
        Inicializa la clase con la ruta del directorio del proyecto.
        
        :param project_dir: Ruta del directorio del proyecto.
        """
        self.project_dir = project_dir or Path.cwd()

    def get_project_name(self) -> str:
        """
        Recupera el nombre del proyecto basado en el nombre del directorio principal.

        :return: Nombre del proyecto.
        """
        try:
            project_name = self.project_dir.name
            return project_name
        except AttributeError as e:
            print(f"Error al obtener el nombre del proyecto: {e}")
            return "Unknown_Project"

    def get_project_name_from_file(self, file_name: str) -> str:
        """
        Recupera el nombre del proyecto desde un archivo específico.

        :param file_name: Nombre del archivo que contiene el nombre del proyecto.
        :return: Nombre del proyecto.
        """
        file_path = self.project_dir / file_name
        return file_path.read_text().strip()
    
```

### C:\AppServ\www\MadyBotPy\src\install\python_interpreter_utils.py
```plaintext
"""
src/install/python_interpreter_utils.py
Este módulo proporciona utilidades para la gestión de entornos 
Python y la verificación de la configuración de pipenv.
"""

import os
import glob
import sys
import subprocess

class PythonInterpreterUtils:
    """
    Clase que proporciona utilidades para la gestión de intérpretes de Python
    y la verificación de pipenv.
    """

    @staticmethod
    def is_pipenv_updated(python_executable: str) -> bool:
        """
        Verifica si pipenv está actualizado con Pipfile y Pipfile.lock.
        
        :param python_executable: Ruta del intérprete de Python a utilizar.
        :return: True si pipenv está actualizado, False en caso contrario.
        """
        print("Verificando si pipenv está actualizado...")
        try:
            result = subprocess.run(
                [python_executable, '-m', 'pipenv', 'sync', '--dry-run'],
                capture_output=True,
                text=True,
                check=True
            )
            if result.returncode == 0:
                print("pipenv está actualizado.")
                return True
            print("pipenv no está actualizado.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error al verificar pipenv. Error: {e}")
            return False

    @staticmethod
    def list_python_interpreters():
        """
        Lista los intérpretes de Python instalados en el sistema, eliminando duplicados.
        
        :return: Lista de rutas a los intérpretes de Python encontrados.
        """
        possible_locations = []
        if os.name == "nt":  # Windows
            possible_locations += glob.glob("C:\\Python*\\python.exe")
            possible_locations += glob.glob("C:\\Users\\*\\"
                                            "AppData\\Local\\Programs\\" 
                                            "Python\\Python*\\python.exe")
        else:  # Unix-based systems
            possible_locations += glob.glob("/usr/bin/python*")
            possible_locations += glob.glob("/usr/local/bin/python*")
            possible_locations += glob.glob("/opt/*/bin/python*")
        python_paths = set()  # Utilizamos un set para eliminar duplicados
        python_paths.add(os.path.normcase(os.path.normpath(sys.executable)))
        for path in possible_locations:
            normalized_path = os.path.normcase(os.path.normpath(path))
            if os.path.exists(normalized_path):
                python_paths.add(normalized_path)
        return sorted(python_paths)

```

### C:\AppServ\www\MadyBotPy\src\install\shortcut_creation_strategy.py
```plaintext
"""
src/install/shortcut_creation_strategy.py
Este módulo define las estrategias para la creación de accesos directos.
"""

from abc import ABC, abstractmethod
from win32com.client import Dispatch

class ShortcutCreationStrategy(ABC):
    """
    Clase abstracta que define la interfaz para la creación de accesos directos.
    """
    # pylint: disable=too-few-public-methods
    @abstractmethod
    def create_shortcut(self, ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger):
        """
        Método abstracto para crear un acceso directo.
        """


class DefaultShortcutCreationStrategy(ShortcutCreationStrategy):
    """
    Estrategia por defecto para la creación de accesos directos utilizando Windows Script Host.
    """
    # pylint: disable=too-few-public-methods
    def create_shortcut(self, ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger):
        """
        Crea un acceso directo en el escritorio apuntando al archivo BAT especificado.

        :param ruta_acceso_directo: Ruta donde se creará el acceso directo.
        :param ruta_archivo_bat: Ruta al archivo BAT que será el objetivo del acceso directo.
        :param ruta_icono: Ruta al archivo de icono que se usará para el acceso directo.
        :param logger: Logger para registrar el proceso.
        :return: True si la creación del acceso directo fue exitosa, False en caso de error.
        """
        try:
            shell = Dispatch('WScript.Shell')
            acceso_directo = shell.CreateShortCut(str(ruta_acceso_directo))
            acceso_directo.Targetpath = str(ruta_archivo_bat)
            acceso_directo.WorkingDirectory = str(ruta_archivo_bat.parent)
            acceso_directo.IconLocation = str(ruta_icono)
            acceso_directo.save()
            logger.debug(
                f"Acceso directo {'actualizado' if ruta_acceso_directo.exists() else 'creado'} "
                "exitosamente."
            )
            return True
        except OSError as error_os:
            logger.error(
                "No se pudo crear/actualizar el acceso directo debido a un error del sistema "
                "operativo: %s",
                error_os,
                exc_info=True
            )
            return False

```

### C:\AppServ\www\MadyBotPy\src\logs\base_filter.py
```plaintext
"""
src/logs/base_filter.py
Base filter module for shared filter functionality.
"""

import logging

class BaseLogFilter(logging.Filter):
    """Base class for log filters with shared functionality."""
    def filter(self, record: logging.LogRecord) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")

```

### C:\AppServ\www\MadyBotPy\src\logs\config_logger.py
```plaintext
"""
src/logs/config_logger.py
Logger configuration module.
"""

import logging.config
import os
import json
from abc import ABC, abstractmethod
from src.logs.info_error_filter import InfoErrorFilter

class ConfigStrategy(ABC):
    """Abstract base class for configuration strategies."""
    @abstractmethod
    def load_config(self):
        """Loads configuration from a specific source."""
        print("load_config method not implemented.")

class JSONConfigStrategy(ConfigStrategy):
    """Loads configuration from a JSON file."""
    def __init__(self, config_path='src/logs/logging.json', env_key='LOG_CFG'):
        self.config_path = config_path
        self.env_key = env_key

    def load_config(self):
        """Loads configuration from a JSON file or environment variable."""
        path = self.config_path
        value = os.getenv(self.env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt', encoding='utf-8') as f:
                return json.load(f)
        return None

class LoggerConfigurator:
    """Configures logging for the application using a strategy pattern."""
    def __init__(self, config_strategy=None, default_level=logging.INFO):
        self.config_strategy = config_strategy or JSONConfigStrategy()
        self.default_level = default_level

    def configure(self):
        """Configures the logger using the provided strategy."""
        config = self.config_strategy.load_config()
        if config:
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=self.default_level)
            logging.warning("Logging configuration file not found. Using default settings.")
        return logging.getLogger(__name__)

# Configuración inicial del logger para módulos individuales
initial_config_strategy = JSONConfigStrategy()
logger_configurator = LoggerConfigurator(config_strategy=initial_config_strategy)
logger = logger_configurator.configure()
logger.addFilter(InfoErrorFilter())  # Aplica el filtro InfoErrorFilter

```

### C:\AppServ\www\MadyBotPy\src\logs\exclude_http_logs_filter.py
```plaintext
"""
src/logs/ExcludeHTTPLogsFilter.py
Filter module for excluding specific HTTP logs.
"""

import logging

class ExcludeHTTPLogsFilter(logging.Filter):
    """Filters out HTTP GET and POST requests from logs."""
    # pylint: disable=too-few-public-methods
    def filter(self, record):
        """Exclude log records containing 'GET /' or 'POST /'."""
        return 'GET /' not in record.getMessage() and 'POST /' not in record.getMessage()

```

### C:\AppServ\www\MadyBotPy\src\logs\info_error_filter.py
```plaintext
"""
src/logs/info_error_filter.py
Filter module for allowing only INFO and ERROR logs.
"""

import logging

class InfoErrorFilter(logging.Filter):
    """Filters logs to allow only INFO and ERROR levels."""
    # pylint: disable=too-few-public-methods
    def __init__(self):
        super().__init__()

    def filter(self, record: logging.LogRecord) -> bool:
        """Allow log records with level INFO or ERROR."""
        return record.levelno in (logging.INFO, logging.ERROR)

```

### C:\AppServ\www\MadyBotPy\src\logs\logging.json
```json
{
    "version": 1,
    "disable_existing_loggers": false,
    "filters": {
        "exclude_http_logs": {
            "()": "src.logs.exclude_http_logs_filter.ExcludeHTTPLogsFilter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "filters": [
                "exclude_http_logs"
            ],
            "formatter": "simpleFormatter"
        },
        "ssl_file_handler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "src/logs/sistema.log",
            "formatter": "simpleFormatter"
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "ssl_file_handler"
            ]
        },
        "ssl": {
            "level": "DEBUG",
            "handlers": [
                "ssl_file_handler"
            ],
            "propagate": false
        }
    },
    "formatters": {
        "simpleFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        }
    }
}
```

### C:\AppServ\www\MadyBotPy\src\model\db_setup.py
```plaintext
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def init_db():
    """Inicializa la base de datos y las tablas necesarias si no existen."""
    try:
        # Conexión inicial sin especificar la base de datos para crearla si es necesario
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Verificar si la base de datos existe; si no, crearla
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
            print("Base de datos verificada/creada exitosamente.")
        
        # Conectar ahora especificando la base de datos para crear las tablas
        connection.database = os.getenv("DB_NAME")
        
        # Crear tabla usuarios si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                email VARCHAR(255),
                phone_number VARCHAR(20),
                first_connection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla mensajes si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
            )
        """)
        
        print("Tablas verificadas/creadas exitosamente.")

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

```
Fecha y hora:
02-11-2024 22:32:02

