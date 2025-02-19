import pywebview as webview
import os
import sys
import json
import subprocess
import atexit
import threading
import time
from pathlib import Path

class WebUIWrapper:
    def __init__(self):
        self.config_path = Path.home() / '.webui_config.json'
        self.load_config()
        self.server_process = None

    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'window_size': (1024, 768),
                'window_pos': None,
                'last_url': 'http://127.0.0.1:8080/'
            }

    def save_config(self):
        if hasattr(self, 'window') and self.window:
            self.config['window_size'] = self.window.width, self.window.height
            self.config['window_pos'] = self.window.x, self.window.y
        else:
            # Set default values if window is not initialized
            self.config['window_size'] = (1024, 768)
            self.config['window_pos'] = (0, 0)

        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)

    def start_server(self):
        # Start the open-webui server in a hidden window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        try:
            self.server_process = subprocess.Popen(
                ['open-webui', 'serve'],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # Wait for server to start
            time.sleep(2)
        except FileNotFoundError:
            print("Error: open-webui command not found. Please make sure it's installed and in your PATH.")
            sys.exit(1)

    def cleanup(self):
        self.save_config()
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()

    def on_closed(self):
        self.cleanup()

    def run(self):
        # Start the server before creating the window
        self.start_server()

        # Register cleanup on exit
        atexit.register(self.cleanup)

        # Create window with saved dimensions
        width, height = self.config['window_size']
        self.window = webview.create_window(
            'Web UI',
            self.config['last_url'],
            width=width,
            height=height
        )

        # Restore window position if saved
        if self.config['window_pos']:
            self.window.move(*self.config['window_pos'])

        # Set window events
        self.window.events.closed += self.on_closed

        webview.start()

if __name__ == '__main__':
    app = WebUIWrapper()
    app.run()
