# Modernized WebUI Wrapper

This project is a modernized Python wrapper for Open WebUI. It uses async/await patterns, splits concerns among dedicated modules, and leverages Pydantic for configuration management.

## Project Structure

• config.py – Manages configuration using Pydantic  
• server_manager.py – Starts/stops the Open WebUI server asynchronously  
• ui_manager.py – Creates and runs the web UI window using pywebview  
• main.py – The entry point tying everything together  
• test/ – Contains unit tests

## Key Improvements

1. **Async/Await Pattern**
   - Server management uses asyncio for non-blocking operations
   - Proper process management with async subprocess
   - Async health checks for server readiness

2. **Modern Configuration**
   - Pydantic models for type-safe configuration
   - JSON-based persistent settings
   - Validation built into the config system

3. **Modular Architecture**
   - Separate modules for config, server, and UI management
   - Clear separation of concerns
   - Easy to test and maintain

4. **Improved Error Handling**
   - Structured logging
   - Proper cleanup on exit
   - Graceful server shutdown

## Setup

1. Create a Python 3.11 virtual environment:
   ```bash
   python3.11 -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

Start the application with:

```bash
python main.py
```

## Testing

Run the tests using pytest:

```bash
pytest
```

## License

MIT License