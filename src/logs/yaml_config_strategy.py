"""
Path: src/logs/yaml_config_strategy.py
Module to load logging configuration from a YAML file.
"""
import os
import logging.config
import yaml

class YAMLConfigStrategy:
    """Loads logging configuration from a YAML file."""
    def __init__(self, config_path='src/logs/logging.yaml', env_key='LOG_CFG'):
        self.config_path = config_path
        self.env_key = env_key

    def load_config(self):
        """Carga la configuración de logging desde un archivo YAML especificado en env_key."""
        path = os.getenv(self.env_key, self.config_path)
        if os.path.exists(path):
            try:
                with open(path, 'rt', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error("Configuración YAML inválida: %s", e)
        else:
            logging.warning("Archivo de configuración no encontrado en la ruta: %s", path)
        # Retorna configuración por defecto
        return self.default_config()

    def default_config(self):
        """Proporciona una configuración de logging por defecto."""
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'WARNING',
                    'formatter': 'simpleFormatter',
                    'stream': 'ext://sys.stdout',
                },
            },
            'formatters': {
                'simpleFormatter': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                },
            },
            'root': {
                'level': 'WARNING',
                'handlers': ['console'],
            },
        }
