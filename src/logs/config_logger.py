"""
src/logs/config_logger.py
This module configures the logging for the application using a YAML configuration file with dynamic reloading.
"""

import logging.config
import os
from watchdog.observers import Observer
from src.logs.info_error_filter import InfoErrorFilter
from src.logs.yaml_config_strategy import YAMLConfigStrategy
from src.logs.config_change_handler import ConfigChangeHandler

class LoggerConfigurator:
    """Configures logging for the application using YAML configuration with dynamic reloading."""
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerConfigurator, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_strategy=None, default_level=logging.INFO):
        if not hasattr(self, "_initialized"):
            self.config_strategy = config_strategy or YAMLConfigStrategy()
            self.default_level = default_level
            self._configured = False
            self._initialized = True  # Singleton initialization flag

    def configure(self):
        """Initial configuration of the logger."""
        if self._configured:
            return logging.getLogger()

        self.reload_config()  # Initial configuration
        self._configured = True
        self.start_watchdog()

    def reload_config(self):
        """Reloads logging configuration from YAML file."""
        config = self.config_strategy.load_config()
        if config:
            environment = os.getenv("ENV", "dev")
            console_handler = "console_dev" if environment == "dev" else "console_prod"
            config['loggers']['']['handlers'].append(console_handler)
            logging.config.dictConfig(config)
            logging.debug("Logger reconfigured for %s environment.", environment)
        else:
            logging.basicConfig(level=self.default_level)
            logging.warning("Logging configuration not found. Using default settings.")
        root_logger = logging.getLogger()
        self._add_custom_filters(root_logger)

    def start_watchdog(self):
        """Starts a watchdog observer to monitor changes in the logging config file."""
        observer = Observer()
        event_handler = ConfigChangeHandler(self)
        observer.schedule(event_handler, path=os.path.dirname(
            self.config_strategy.config_path), recursive=False)
        observer.start()
        logging.info("Started watchdog for dynamic logging configuration reloading.")

    @staticmethod
    def _add_custom_filters(log):
        info_error_filter = InfoErrorFilter()
        for handler in log.handlers:
            handler.addFilter(info_error_filter)
        logging.debug("Custom filters added to logger handlers.")

# Configuración inicial
logger_configurator = LoggerConfigurator()
logger = logger_configurator.configure()
