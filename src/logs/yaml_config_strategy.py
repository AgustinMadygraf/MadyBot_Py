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
