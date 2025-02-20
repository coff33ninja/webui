# WebUI Wrapper

A Python-based browser wrapper for open-webui with persistent window settings and native Windows integration.

## Features

- Persistent window size and position
- Automatically starts open-webui server in background
- Native Windows integration with batch script
- Asynchronous server management
- Type-safe configuration
- Comprehensive logging
- Built with Python 3.11 and PyWebView

## Prerequisites

- Python 3.11 or newer
- Windows OS (for native shortcut support)
- [Ollama](https://ollama.com/) installed and running

## Quick Start

1. **Direct Launch**
   Simply double-click `run.bat` to start the application. It will:
   - Create a virtual environment if needed
   - Install required dependencies
   - Launch the WebUI

2. **Desktop Shortcut (Optional)**
   To create a desktop shortcut:
   - Right-click `create_shortcut.ps1`
   - Select "Run with PowerShell"
   - A shortcut will be created on your desktop

## For Developers

### Project Structure