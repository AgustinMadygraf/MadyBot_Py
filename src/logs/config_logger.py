"""
src/logs/config_logger.py
Module to configure logging using YAML.
"""

import logging.config
import os
import yaml
from src.logs.info_error_filter import InfoErrorFilter

class YAMLConfigStrategy:
    """Loads logging configuration from a YAML file."""
    def __init__(self, config_path='src/logs/logging.yaml', env_key='LOG_CFG'):
        self.config_path = config_path
        self.env_key = env_key

    def load_config(self):
        """Attempts to load logging configuration from a YAML file specified in env_key."""
        path = os.getenv(self.env_key, self.config_path)
        if os.path.exists(path):
            try:
                with open(path, 'rt', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error("YAML configuration file is invalid: %s", e)
        else:
            logging.warning("Logging configuration file not found at path: %s", path)
        return None


class LoggerConfigurator:
    """Configures logging for the application using YAML configuration."""
    _instance = None  # Variable de clase para mantener la instancia singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerConfigurator, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_strategy=None, default_level=logging.INFO):
        if not hasattr(self, "_initialized"):  # Solo inicializa una vez
            self.config_strategy = config_strategy or YAMLConfigStrategy()
            self.default_level = default_level
            self._configured = False  # Inicializa la configuración como no completada
            self._initialized = True  # Marca la instancia como inicializada

    def configure(self):
        """Configures the logger using the provided YAML strategy."""
        if getattr(self, "_configured", False):  # Verifica si ya se ha configurado
            return logging.getLogger()

        config = self.config_strategy.load_config()
        if config:
            # Decide qué handler de consola usar según el entorno
            environment = os.getenv("ENV", "dev")
            console_handler = "console_dev" if environment == "dev" else "console_prod"
            # Agregar el handler de consola apropiado al root logger
            config['loggers']['']['handlers'].append(console_handler)
            logging.config.dictConfig(config)
            logging.debug("Logger configured for %s environment.", environment)
            self._configured = True  # Marca la configuración como completada
        else:
            logging.basicConfig(level=self.default_level)
            logging.warning("Logging configuration not found. Using default settings.")
        # Get a root logger and add custom handlers/filters if needed
        root_logger = logging.getLogger()
        self._add_custom_filters(root_logger)
        LoggerConfigurator._add_custom_filters(root_logger)

    @staticmethod
    @staticmethod
    def _add_custom_filters(log):
        info_error_filter = InfoErrorFilter()
        for handler in log.handlers:
            handler.addFilter(info_error_filter)
        logging.debug("Custom filters added to logger handlers.")


# Configuración inicial (singleton)
logger_configurator = LoggerConfigurator()
logger = logger_configurator.configure()
