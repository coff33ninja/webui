import logging
import webview
from config import AppConfig

class UIManager:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.window = None

    def create_window(self) -> None:
        logging.info(f"Creating window with URL: {self.config.start_url}")
        self.window = webview.create_window(
            title=self.config.window_title,
            url=str(self.config.start_url),
            width=self.config.window_width,
            height=self.config.window_height
        )

    def run_window(self) -> None:
        if self.window is None:
            self.create_window()
        webview.start()