
import os
import sys
import json
import atexit
import winshell
import subprocess
import time
import socket
from pathlib import Path
from win32com.client import Dispatch
import logging
import webview

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
        self.window = None
        self.cleaned_up = False
        logging.info("WebUIWrapper initialized")

    def load_config(self):
        # Default configuration
        self.config = {
            'window_title': 'Web UI',
            'window_width': 1024,
            'window_height': 768,
            'start_url': 'http://127.0.0.1:8080/'
        }

        # Try to load from config file if it exists
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    file_config = json.load(f)
                    # Merge file config with defaults
                    self.config.update(file_config)
                logging.info("Config loaded successfully")
            except Exception as e:
                logging.error(f"Error loading config: {e}. Using default configuration")
        else:
            logging.info("No config file found, using default configuration")


    def save_config(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f)
            logging.info("Config saved successfully")
        except Exception as e:
            logging.error(f"Error writing config to file: {e}")

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

    def cleanup(self):
        if self.cleaned_up:
            return
        self.cleaned_up = True
        logging.info("Starting cleanup...")
        self.save_config()
        logging.info("Cleanup completed")

    def start_server(self, method='direct'):
        """Start the Open WebUI server using specified method

        Args:
            method (str): Startup method to use. Options are:
                - 'direct': Direct subprocess execution (default)
                - 'piped': Subprocess with piped output
                - 'threaded': Background thread execution
        """
        try:
            # Activate virtual environment if present
            venv_path = os.path.join(os.path.dirname(__file__), 'venv')
            python_exec = sys.executable

            if os.path.exists(venv_path):
                python_exec = os.path.join(venv_path, 'Scripts', 'python.exe')
                if not os.path.exists(python_exec):
                    raise Exception(f"Virtual environment Python executable not found at: {python_exec}")

            if method == 'direct':
                # Method 1: Direct execution
                self.server_process = subprocess.Popen(
                    ['open-webui', 'serve'],
                    cwd=os.path.dirname(__file__),
                    env=os.environ.copy()
                )
                logging.info("Started Open WebUI server using direct method")

            elif method == 'piped':
                # Method 2: Piped output
                self.server_process = subprocess.Popen(
                    ['open-webui', 'serve'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.path.dirname(__file__),
                    env=os.environ.copy()
                )
                # Log server output in separate threads
                def log_stream(stream, prefix):
                    for line in stream:
                        logging.info(f"[Server] {prefix}: {line.strip()}")

                import threading
                threading.Thread(target=log_stream, args=(self.server_process.stdout, "stdout"), daemon=True).start()
                threading.Thread(target=log_stream, args=(self.server_process.stderr, "stderr"), daemon=True).start()
                logging.info("Started Open WebUI server using piped method")

            elif method == 'threaded':
                # Method 3: Background thread
                def run_server():
                    subprocess.run(
                        ['open-webui', 'serve'],
                        cwd=os.path.dirname(__file__),
                        env=os.environ.copy()
                    )

                import threading
                self.server_thread = threading.Thread(target=run_server, daemon=True)
                self.server_thread.start()
                logging.info("Started Open WebUI server using threaded method")

            else:
                raise ValueError(f"Invalid server startup method: {method}")

            # Wait for server to be ready
            time.sleep(5)  # Initial wait
            max_attempts = 12
            for attempt in range(max_attempts):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex(('127.0.0.1', 8080))
                    sock.close()
                    if result == 0:
                        logging.info("Server is ready and accepting connections")
                        return True
                except Exception as e:
                    logging.warning(f"Server check failed (attempt {attempt + 1}/{max_attempts}): {e}")
                time.sleep(5)

            logging.error("Server failed to start within the expected time")
            return False

        except Exception as e:
            logging.error(f"Failed to start Open WebUI server: {e}")
            return False

    def stop_server(self):
        """Stop the Open WebUI server"""
        if hasattr(self, 'server_process') and self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                logging.info("Stopped Open WebUI server")
            except Exception as e:
                logging.error(f"Error stopping server: {e}")

    def run(self):
        try:
            # Create desktop shortcut if it doesn't exist
            shortcut_path = os.path.join(winshell.desktop(), "WebUI Wrapper.lnk")
            if not os.path.exists(shortcut_path):
                self.create_shortcut()

            # Start Open WebUI server with different methods
            methods = ['direct', 'piped', 'threaded']
            for method in methods:
                logging.info(f"Attempting to start server using method: {method}")
                if self.start_server(method=method):
                    break
                if method == methods[-1]:
                    raise Exception("Failed to start Open WebUI server after trying all methods")
                logging.warning(f"Server startup failed with method {method}, trying next method...")
                time.sleep(10)

            # Register cleanup on exit
            atexit.register(self.cleanup)
            atexit.register(self.stop_server)

            # Wait for server to be ready and verify it's running
            time.sleep(60)  # Increased wait time for server initialization
            try:
                # Verify server is running by checking if port is open
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', 8080))
                if result != 0:
                    raise Exception("Server failed to start on port 8080")
                sock.close()
                logging.info("Server is running and ready")

                # Create and start the window
                # Ensure start_url is valid
                if not self.config.get('start_url'):
                    self.config['start_url'] = 'http://127.0.0.1:8080/'
                    logging.warning("start_url was missing, using default")

                logging.info(f"Creating window with URL: {self.config['start_url']}")
                self.window = webview.create_window(
                    self.config.get('window_title', 'Web UI'),
                    self.config['start_url'],
                    width=self.config.get('window_width', 1024),
                    height=self.config.get('window_height', 768)
                )

                webview.start()
                logging.info("Window closed")

            except Exception as e:
                logging.error(f"Error while running window: {e}")
            finally:
                self.cleanup()
                self.stop_server()

        except Exception as e:
            logging.error(f"Unexpected error in run(): {e}")
            self.cleanup()
            self.stop_server()
            sys.exit(1)

if __name__ == '__main__':
    try:
        logging.info("Starting WebUI Wrapper application")
        app = WebUIWrapper()
        app.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
