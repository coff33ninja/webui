import asyncio
import logging
import atexit
import sys
import os
from pathlib import Path
from config import load_config, save_config, AppConfig
from server_manager import ServerManager
from ui_manager import UIManager

# Set up logging to both file and console
log_file: Path = Path(os.path.expanduser('~')) / '.webui' / 'webui.log'
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def cleanup_server(server_manager: ServerManager) -> None:
    try:
        if server_manager.process:
            asyncio.run(server_manager.stop_server())
    except (ProcessLookupError, AttributeError):
        logging.info("Server process already terminated")

async def main() -> None:
    try:
        # Log startup information
        logging.info("Starting WebUI")
        logging.info(f"Python version: {sys.version}")
        logging.info(f"Working directory: {os.getcwd()}")

        # Load configuration using pydantic
        config: AppConfig = load_config()
        logging.info(f"Configuration loaded: {config.to_json()}")

        # Initialize server manager
        server_manager: ServerManager = ServerManager()

        # Check if server is already running
        if await server_manager.check_port():
            logging.info("Server is already running on port 8080")
        else:
            # Attempt to start server if not running
            server_started: bool = False
            for method in ['direct', 'piped']:
                logging.info(f"Attempting to start server using method: {method}")
                if await server_manager.start_server(method=method):
                    server_started = True
                    break
                else:
                    logging.warning(f"Server startup failed using method: {method}")

            if not server_started:
                logging.error("All server startup methods failed. Exiting.")
                sys.exit(1)

        atexit.register(lambda: save_config(config))
        atexit.register(lambda: cleanup_server(server_manager))

        # Start the UI window with server manager
        ui: UIManager = UIManager(config, server_manager)
        ui.run_window()

        # After window closes, stop the server if running
        if await server_manager.check_port():
            await server_manager.stop_server()

    except Exception:
        logging.exception("Fatal error occurred")
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application terminated by user")
    except Exception:
        logging.exception("Fatal error in main")
        sys.exit(1)
