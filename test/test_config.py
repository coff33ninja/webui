import json
import tempfile
from pathlib import Path
from config import AppConfig, load_config, save_config, CONFIG_PATH

def test_default_config() -> None:
    config = AppConfig()
    assert config.window_title == 'Web UI'
    assert config.window_width == 1024

def test_save_and_load_config(tmp_path: Path) -> None:
    # Create a temporary configuration file
    temp_config = tmp_path / "config.json"
    data = {
        "window_title": "Test UI",
        "window_width": 800,
        "window_height": 600,
        "start_url": "http://127.0.0.1:5000/"
    }
    temp_config.write_text(json.dumps(data))

    # Monkey-patch CONFIG_PATH for testing purposes
    original_config_path = CONFIG_PATH
    try:
        import config
        config.CONFIG_PATH = temp_config
        config_loaded = load_config()
        assert config_loaded.window_title == "Test UI"
        save_success = save_config(config_loaded)
        assert save_success
    finally:
        config.CONFIG_PATH = original_config_path