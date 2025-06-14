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
            'reloadPage': self.reload_page,
            'getServerStatus': self.get_server_status,
            'shutdownApp': self.shutdown_app  # New method for graceful shutdown
        }
        self._server_running = False
        if self.server_manager:
            self.server_manager.set_connection_callback(self._on_server_status_change)

    async def _on_server_status_change(self, is_up: bool):
        if is_up and not self._server_running:
            self._server_running = True
            if self.window:
                self.window.evaluate_js('window.location.reload()')
        elif not is_up:
            self._server_running = False

    def get_server_status(self) -> bool:
        return self._server_running

    def create_window(self) -> None:
        # Convert HttpUrl to string for webview
        start_url = str(self.config.start_url)
        logging.info(f"Creating window with URL: {start_url}")
        self.window = webview.create_window(
            title=self.config.window_title,
            url=start_url,
            width=self.config.window_width,
            height=self.config.window_height,
            js_api=self._js_api,
            resizable=True,
            easy_drag=False
        )
        # Start port monitoring
        if self.server_manager:
            self.server_manager.start_monitoring()

    async def start_server(self) -> bool:
        if self.server_manager:
            return await self.server_manager.start_server()
        return False

    async def stop_server(self) -> bool:
        if self.server_manager:
            await self.server_manager.stop_server()
            return True
        return False

    def reload_page(self) -> None:
        if self.window:
            self.window.evaluate_js('window.location.reload()')

    def shutdown_app(self) -> None:
        """Gracefully shutdown the app: stop server and close window."""
        if self.server_manager:
            # Stop the server synchronously (fire and forget)
            import asyncio
            asyncio.create_task(self.server_manager.stop_server())
        if self.window:
            self.window.destroy()

    def run_window(self) -> None:
        if self.window is None:
            self.create_window()
        webview.start()
