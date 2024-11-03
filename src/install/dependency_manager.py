"""
src/install/dependency_manager.py
Este módulo proporciona clases para la gestión de dependencias, incluyendo la actualización de pip,
la instalación de dependencias y la verificación de dependencias faltantes.
"""

import subprocess
import sys
from abc import ABC, abstractmethod
import logging
import traceback

# Configurar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('dependency_manager.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

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
    """ Clase que gestiona la instalación de dependencias. """
    def __init__(self, installer, pip_updater, max_retries=3):
        self.installer = installer
        self.pip_updater = pip_updater
        self.max_retries = max_retries

    def install_missing_dependencies(self, requirements_file):
        """ Instala las dependencias faltantes desde un archivo requirements. """
        for attempt in range(self.max_retries):
            try:
                self.installer.install(requirements_file)
                logger.info("Dependencies installed successfully from %s", requirements_file)
                break
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                logger.error("Attempt %d failed: %s", attempt + 1, str(e))
                logger.debug(traceback.format_exc())
                if attempt == self.max_retries - 1:
                    logger.critical("Failed to install dependencies after %d attempts",
                                    self.max_retries)
                    raise RuntimeError("Failed to install dependencies") from e
