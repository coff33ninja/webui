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
log_file = Path(os.path.expanduser('~')) / '.webui' / 'webui.log'
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

async def main() -> None:
    try:
        # Log startup information
        logging.info("Starting WebUI")
        logging.info(f"Python version: {sys.version}")
        logging.info(f"Working directory: {os.getcwd()}")
        
        # Load configuration using pydantic
        config: AppConfig = load_config()
        logging.info(f"Configuration loaded: {config.to_json()}")

        # Initialize and start the server manager
        server_manager = ServerManager()
        server_started = False
        
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

        # Register cleanup functions
        atexit.register(lambda: save_config(config))
        atexit.register(lambda: asyncio.run(server_manager.stop_server()))

        # Start the UI window (blocking call)
        ui = UIManager(config)
        ui.run_window()

        # After window closes, stop the server
        await server_manager.stop_server()
        
    except Exception as e:
        logging.exception("Fatal error occurred")
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application terminated by user")
    except Exception as e:
        logging.exception("Fatal error in main")
        sys.exit(1)