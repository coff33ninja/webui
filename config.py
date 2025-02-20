from pathlib import Path
import json
import logging
from pydantic import BaseModel, HttpUrl

CONFIG_PATH = Path.home() / '.webui_config.json'

class AppConfig(BaseModel):
    window_title: str = 'Web UI'
    window_width: int = 1024
    window_height: int = 768
    start_url: HttpUrl = 'http://127.0.0.1:8080/'

def load_config() -> AppConfig:
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text())
            config = AppConfig(**data)
            logging.info("Configuration loaded successfully")
            return config
        except Exception as e:
            logging.error(f"Error loading configuration: {e}. Using default configuration")
    logging.info("No configuration file was found; using defaults")
    return AppConfig()

def save_config(config: AppConfig) -> bool:
    try:
        CONFIG_PATH.write_text(config.json(indent=2))
        logging.info("Configuration saved successfully")
        return True
    except Exception as e:
        logging.error(f"Error saving configuration: {e}")
        return False