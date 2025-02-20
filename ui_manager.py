import logging
import webview
from typing import Optional
from config import AppConfig
from server_manager import ServerManager

class UIManager:
    def __init__(self, config: AppConfig, server_manager: Optional[ServerManager] = None) -> None:
        self.config = config
        self.window = None
        self.server_manager = server_manager
        self._js_api = {
            'startServer': self.start_server,
            'stopServer': self.stop_server,
            'reloadPage': self.reload_page
        }

    def create_window(self) -> None:
        # Convert HttpUrl to string for webview
        start_url = str(self.config.start_url)
        logging.info(f"Creating window with URL: {start_url}")

        # Create window with native controls
        self.window = webview.create_window(
            title=self.config.window_title,
            url=start_url,
            width=self.config.window_width,
            height=self.config.window_height,
            js_api=self._js_api,
            resizable=True,
            easy_drag=False
        )

        # Add native controls
        self.window.events.loaded += self._add_native_controls

    def _add_native_controls(self) -> None:
        """Add native control buttons to the window"""
        # Create a toolbar
        toolbar = webview.create_toolbar(self.window)

        # Add Start Server button
        toolbar.add_button(
            "Start Server",
            lambda: asyncio.run(self.start_server()),
            tooltip="Start the backend server"
        )

        # Add Stop Server button
        toolbar.add_button(
            "Stop Server",
            lambda: asyncio.run(self.stop_server()),
            tooltip="Stop the backend server",
            enabled=False
        )

        # Add Reload button
        toolbar.add_button(
            "Reload",
            lambda: self.window.evaluate_js('window.location.reload()'),
            tooltip="Reload current page"
        )

        # Add toolbar to window
        self.window.add_toolbar(toolbar)

    async def start_server(self) -> bool:
        if self.server_manager:
            return await self.server_manager.start_server()
        return False

    async def stop_server(self) -> bool:
        if self.server_manager:
            return await self.server_manager.stop_server()
        return False

    def reload_page(self) -> None:
        if self.window:
            self.window.evaluate_js('window.location.reload()')

    def run_window(self) -> None:
        if self.window is None:
            self.create_window()
        webview.start()
