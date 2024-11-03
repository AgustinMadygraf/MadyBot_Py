"""
src/logs/config_logger.py
Module to configure logging using YAML.
"""

import logging.config
import os
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.logs.info_error_filter import InfoErrorFilter

class YAMLConfigStrategy:
    """Loads logging configuration from a YAML file."""
    def __init__(self, config_path='src/logs/logging.yaml', env_key='LOG_CFG'):
        self.config_path = config_path
        self.env_key = env_key

    def load_config(self):
        """Loads logging configuration from a YAML file specified in env_key."""
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


class ConfigChangeHandler(FileSystemEventHandler):
    """Handler to reload logging configuration when logging.yaml changes."""

    def __init__(self, configurator):
        self.configurator = configurator

    def on_modified(self, event):
        """Reloads logging configuration when logging.yaml is modified."""
        if event.src_path.endswith("logging.yaml"):
            logging.info("Detected change in logging.yaml, reloading configuration.")
            self.configurator.reload_config()


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
