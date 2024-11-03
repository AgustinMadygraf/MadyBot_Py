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
        """Loads the configuration from a file or environment variable."""
        pass

class JSONConfigStrategy(ConfigStrategy):
    """Loads configuration from a JSON file with UTF-8 encoding."""
    def __init__(self, config_path='src/logs/logging.json', env_key='LOG_CFG'):
        self.config_path = config_path
        self.env_key = env_key
    def load_config(self):
        """Loads configuration from a JSON file or environment variable with UTF-8."""
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
        # Configurar el handler de archivo con UTF-8
        local_logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler('sistema.log', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        local_logger.addHandler(file_handler)
        local_logger.addFilter(InfoErrorFilter())  # Aplica el filtro InfoErrorFilter
        return local_logger

# Configuración inicial
initial_config_strategy = JSONConfigStrategy()
logger_configurator = LoggerConfigurator(config_strategy=initial_config_strategy)
logger = logger_configurator.configure()
