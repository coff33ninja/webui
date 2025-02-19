# WebUI Wrapper

A Python-based browser wrapper for open-webui with persistent window settings.

## Features

- Persistent window size and position
- Automatically starts open-webui server in background
- Built with Python 3.11 and PyWebView

## Prerequisites

- Python 3.11
- [Ollama](https://ollama.com/) installed and running

## Setup

1. Create a Python 3.11 virtual environment:
   ```bash
   python3.11 -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Web UI

1. Start the web UI:
   ```bash
   python webui_wrapper.py
   ```

2. The web UI will open in a new window.

## Acknowledgements

- [Open WebUI](https://github.com/open-webui/open-webui) - The web UI framework
- [Ollama](https://ollama.com/) - The local LLM framework

## License

MIT License


python3.11 -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python webui_wrapper.py
