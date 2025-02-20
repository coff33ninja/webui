import asyncio
import logging
import atexit
import sys
from config import load_config, save_config, AppConfig
from server_manager import ServerManager
from ui_manager import UIManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main() -> None:
    # Load configuration using pydantic
    config: AppConfig = load_config()

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

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)