import os
import sys
import json
import subprocess
import atexit
import time
import winshell
from pathlib import Path
from win32com.client import Dispatch
import logging
import webbrowser
import socket
import requests
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('webui_wrapper.log')
    ]
)

class WebUIWrapper:
    def __init__(self):
        self.config_path = Path.home() / '.webui_config.json'
        self.load_config()
        self.server_process = None
        self.cleaned_up = False
        logging.info("WebUIWrapper initialized")

    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logging.info("Config loaded successfully")
            except Exception as e:
                logging.error(f"Error loading config: {e}")
                self.config = {
                    'last_url': 'http://127.0.0.1:8080/'
                }
        else:
            logging.info("No config file found, using defaults")
            self.config = {
                'last_url': 'http://127.0.0.1:8080/'
            }

    def save_config(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f)
            logging.info("Config saved successfully")
        except Exception as e:
            logging.error(f"Error writing config to file: {e}")

    def wait_for_server(self, url, timeout=30):
        """Wait for server to be ready"""
        parsed_url = urlparse(url)
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    logging.info(f"Server is ready at {url}")
                    return True
            except requests.RequestException:
                time.sleep(1)
        logging.error(f"Server failed to start after {timeout} seconds")
        return False

    def start_server(self):
        # Start the open-webui server in a hidden window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        try:
            logging.info("Starting server...")
            self.server_process = subprocess.Popen(
                ['open-webui', 'serve'],
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            # Wait for server to be ready
            if not self.wait_for_server(self.config['last_url']):
                raise Exception("Server failed to start")

            logging.info("Server started successfully")

        except FileNotFoundError:
            logging.error("Error: open-webui command not found. Please ensure it is installed and available in your PATH.")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error starting server: {str(e)}")
            sys.exit(1)

    def cleanup(self):
        if self.cleaned_up:
            return
        self.cleaned_up = True
        logging.info("Starting cleanup...")

        # Save configuration first
        self.save_config()

        if self.server_process:
            try:
                logging.info("Terminating server process...")
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                logging.info("Server process terminated")
            except subprocess.TimeoutExpired:
                try:
                    logging.warning("Server process did not terminate, forcing kill...")
                    self.server_process.kill()
                    logging.info("Server process killed")
                except Exception:
                    logging.error("Failed to kill server process")
            except Exception as e:
                logging.error(f"Error during server cleanup: {str(e)}")

    def create_shortcut(self):
        """Create a desktop shortcut to run the web UI"""
        try:
            desktop = winshell.desktop()
            path = os.path.join(desktop, "WebUI Wrapper.lnk")
            target = str(Path(sys.executable).parent / "python.exe")
            w_dir = str(Path(__file__).parent)
            icon = str(Path(__file__).parent / "webui_wrapper.py")

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.Arguments = 'webui_wrapper.py'
            shortcut.WorkingDirectory = w_dir
            shortcut.IconLocation = icon
            shortcut.save()
            logging.info(f"Shortcut created successfully at: {path}")
            return True
        except Exception as e:
            logging.error(f"Failed to create shortcut: {str(e)}")
            return False

    def run(self):
        try:
            # Create desktop shortcut if it doesn't exist
            shortcut_path = os.path.join(winshell.desktop(), "WebUI Wrapper.lnk")
            if not os.path.exists(shortcut_path):
                self.create_shortcut()

            # Start the server before opening browser
            self.start_server()

            # Register cleanup on exit
            atexit.register(self.cleanup)

            # Open the default browser
            try:
                logging.info(f"Opening browser at {self.config['last_url']}")
                webbrowser.open(self.config['last_url'])

                # Keep the script running until Ctrl+C
                logging.info("Press Ctrl+C to exit")
                while True:
                    time.sleep(1)

                    # Check if server is still running
                    if self.server_process and self.server_process.poll() is not None:
                        logging.error("Server process has stopped unexpectedly")
                        break

            except KeyboardInterrupt:
                logging.info("Received keyboard interrupt, shutting down...")
            except Exception as e:
                logging.error(f"Error while running: {e}")
            finally:
                self.cleanup()

        except Exception as e:
            logging.error(f"Unexpected error in run(): {e}")
            self.cleanup()
            sys.exit(1)

if __name__ == '__main__':
    try:
        logging.info("Starting WebUI Wrapper application")
        app = WebUIWrapper()
        app.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
