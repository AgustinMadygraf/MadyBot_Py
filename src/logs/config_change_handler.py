"""
Path: src/logs/config_change_handle.py
Module to handle changes in logging configuration.
"""
import logging.config
from watchdog.events import FileSystemEventHandler


class ConfigChangeHandler(FileSystemEventHandler):
    """Handler to reload logging configuration when logging.yaml changes."""

    def __init__(self, configurator):
        self.configurator = configurator

    def on_modified(self, event):
        """Reloads logging configuration when logging.yaml is modified."""
        if event.src_path.endswith("logging.yaml"):
            logging.info("Detected change in logging.yaml, reloading configuration.")
            self.configurator.reload_config()
