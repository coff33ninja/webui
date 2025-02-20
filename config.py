from pathlib import Path
import json
import logging
from typing import Dict, Any
from pydantic import BaseModel, HttpUrl, model_validator

CONFIG_PATH = Path.home() / '.webui_config.json'

class AppConfig(BaseModel):
    window_title: str = 'Web UI'
    window_width: int = 1024
    window_height: int = 768
    start_url: HttpUrl = 'http://127.0.0.1:8080/'

    def to_json(self) -> str:
        """Convert config to JSON string with indentation"""
        # Convert the model to a dict and handle HttpUrl
        data = self.model_dump()
        # Convert HttpUrl to string for JSON serialization
        data['start_url'] = str(data['start_url'])
        return json.dumps(data, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'AppConfig':
        """Create config from JSON string"""
        data = json.loads(json_str)
        # The HttpUrl validation will happen automatically when creating the model
        return cls(**data)

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Override model_dump to handle HttpUrl"""
        data = super().model_dump(**kwargs)
        data['start_url'] = str(data['start_url'])
        return data

def load_config() -> AppConfig:
    """Load configuration from file or return defaults"""
    if CONFIG_PATH.exists():
        try:
            config_json = CONFIG_PATH.read_text()
            config = AppConfig.from_json(config_json)
            logging.info("Configuration loaded successfully")
            return config
        except Exception as e:
            logging.error(f"Error loading configuration: {e}. Using default configuration")
    logging.info("No configuration file was found; using defaults")
    return AppConfig()

def save_config(config: AppConfig) -> bool:
    """Save configuration to file"""
    try:
        CONFIG_PATH.write_text(config.to_json())
        logging.info("Configuration saved successfully")
        return True
    except Exception as e:
        logging.error(f"Error saving configuration: {e}")
        return False