"""
src/logs/config_logger.py
Module to configure logging using the Strategy Pattern.
"""

import logging.config
import os
import json
from abc import ABC, abstractmethod
import yaml
from src.logs.info_error_filter import InfoErrorFilter

class ConfigStrategy(ABC):
    """Abstract base class for configuration strategies."""
    @abstractmethod
    def load_config(self):
        """Loads the logging configuration from a specific source."""


class JSONConfigStrategy(ConfigStrategy):
    """Loads logging configuration from a JSON file."""
    def __init__(self, config_path='src/logs/logging.json', env_key='LOG_CFG'):
        self.config_path = config_path
        self.env_key = env_key

    def load_config(self):
        """Attempts to load logging configuration from a JSON file specified in env_key."""
        path = os.getenv(self.env_key, self.config_path)
        if os.path.exists(path):
            try:
                with open(path, 'rt', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logging.error("JSON configuration file is invalid: %s", e)
        else:
            logging.warning("Logging configuration file not found at path: %s", path)
        return None


class YAMLConfigStrategy(ConfigStrategy):
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
    """Configures logging for the application using a strategy pattern."""

    def __init__(self, config_strategy=None, default_level=logging.INFO):
        """
        Initializes the LoggerConfigurator with a configuration strategy.
        If no strategy is provided, it defaults to JSONConfigStrategy.
        """
        self.config_strategy = config_strategy or JSONConfigStrategy()
        self.default_level = default_level

    def configure(self):
        """Configures the logger using the provided strategy."""
        config = self.config_strategy.load_config()
        if config:
            logging.config.dictConfig(config)
            logging.debug("Logger configured using %s strategy.",
                          self.config_strategy.__class__.__name__)
        else:
            logging.basicConfig(level=self.default_level)
            logging.warning("Logging configuration not found. Using default settings.")

        # Get a root logger and add custom handlers/filters if needed
        root_logger = logging.getLogger()
        self._add_custom_filters(root_logger)
        return root_logger

    @staticmethod
    def _add_custom_filters(log):
        """Adds custom filters, such as InfoErrorFilter, to the logger."""
        info_error_filter = InfoErrorFilter()
        for handler in log.handlers:
            handler.addFilter(info_error_filter)
        logging.debug("Custom filters added to logger handlers.")

# Configuración inicial
initial_config_strategy = YAMLConfigStrategy()  # Cambiar aquí a YAMLConfigStrategy para probar YAML
logger_configurator = LoggerConfigurator(config_strategy=initial_config_strategy)
logger = logger_configurator.configure()
