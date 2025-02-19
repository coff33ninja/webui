import webview
import os
import sys
import json
import subprocess
import atexit
import time
import winshell
from pathlib import Path
from win32com.client import Dispatch

class WebUIWrapper:
    def __init__(self):
        self.config_path = Path.home() / '.webui_config.json'
        self.load_config()
        self.server_process = None
        self.cleaned_up = False  # prevent duplicate cleanup

    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                # Make sure window_size and window_pos are tuples (JSON saves them as lists)
                self.config['window_size'] = tuple(self.config.get('window_size', (1024, 768)))
                if self.config.get('window_pos'):
                    self.config['window_pos'] = tuple(self.config['window_pos'])
            except Exception as e:
                print(f"Error loading config, using defaults: {e}")
                self.config = {
                    'window_size': (1024, 768),
                    'window_pos': (0, 0),
                    'last_url': 'http://127.0.0.1:8080/'
                }
        else:
            self.config = {
                'window_size': (1024, 768),
                'window_pos': None,
                'last_url': 'http://127.0.0.1:8080/'
            }

    def save_config(self):
        try:
            if hasattr(self, 'window') and self.window:
                # Wrap in try/except incase attributes are not available
                try:
                    width = self.window.width
                    height = self.window.height
                    self.config['window_size'] = (width, height)
                except Exception as e:
                    self.config['window_size'] = (1024, 768)
                    print(f"Warning: Could not retrieve window size: {e}")
                try:
                    # Some backends might not support window.x and window.y
                    x = getattr(self.window, 'x', 0)
                    y = getattr(self.window, 'y', 0)
                    self.config['window_pos'] = (x, y)
                except Exception as e:
                    self.config['window_pos'] = (0, 0)
                    print(f"Warning: Could not retrieve window position: {e}")
            else:
                self.config['window_size'] = (1024, 768)
                self.config['window_pos'] = (0, 0)
        except Exception as e:
            # Fallback to default values if any error occurs
            print(f"Error saving config: {e}")
            self.config['window_size'] = (1024, 768)
            self.config['window_pos'] = (0, 0)

        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Error writing config to file: {e}")

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
            # Wait for server to start (could be replaced with a more robust check)
            time.sleep(2)
            
            # Verify the process is running
            if self.server_process.poll() is not None:
                raise Exception("Server process failed to start")
                
        except FileNotFoundError:
            print("Error: open-webui command not found. Please ensure it is installed and available in your PATH.")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error starting server: {str(e)}")
            sys.exit(1)

    def cleanup(self):
        if self.cleaned_up:
            return
        self.cleaned_up = True
        # Save configuration first
        self.save_config()

        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    self.server_process.kill()
                except Exception:
                    pass
            except Exception as e:
                print(f"Error during server cleanup: {str(e)}")

    def on_closed(self):
        self.cleanup()

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
            print(f"Shortcut created successfully at: {path}")
            return True
        except Exception as e:
            print(f"Failed to create shortcut: {str(e)}")
            return False

    def run(self):
        # Create desktop shortcut if it doesn't exist
        shortcut_path = os.path.join(winshell.desktop(), "WebUI Wrapper.lnk")
        if not os.path.exists(shortcut_path):
            self.create_shortcut()

        # Start the server before creating the window
        self.start_server()

        # Register cleanup on exit (this helps if the user kills the app unexpectedly)
        atexit.register(self.cleanup)

        # Create window with saved dimensions
        try:
            width, height = self.config.get('window_size', (1024, 768))
            self.window = webview.create_window(
                'Web UI',
                self.config.get('last_url', 'http://127.0.0.1:8080/'),
                width=width,
                height=height
            )
        except Exception as e:
            print(f"Error creating webview window: {e}")
            self.cleanup()
            sys.exit(1)

        # Restore window position if saved and if supported
        if self.config.get('window_pos') and hasattr(self.window, 'move'):
            try:
                self.window.move(*self.config['window_pos'])
            except Exception as e:
                print(f"Warning: Unable to restore window position: {e}")

        # Attach event handler to ensure cleanup on window close
        try:
            self.window.events.closed += self.on_closed
        except Exception as e:
            print(f"Error setting close event: {e}")

        # Start the UI inside a try/except to catch any unexpected errors that might cause a crash
        try:
            webview.start()
        except Exception as e:
            print(f"Error encountered during UI execution: {e}")
            self.cleanup()
            sys.exit(1)

if __name__ == '__main__':
    app = WebUIWrapper()
    app.run()