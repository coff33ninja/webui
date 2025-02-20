# WebUI Wrapper

A user-friendly application wrapper for open-webui with persistent settings and native OS integration.

## 🚀 Quick Setup (For Everyone!)

### Windows Users
1. **Super Easy Start:**
   - Just double-click `run.bat`
   - That's it! The application will set everything up automatically

2. **Want a Desktop Shortcut?**
   - Right-click `create_shortcut.ps1`
   - Choose "Run with PowerShell"
   - You'll get a nice desktop icon to click next time!

### Mac Users
1. **Easy Start:**
   - Open the folder in Finder
   - Right-click `run.sh` and select "Open With" → "Terminal"
   - Click "Open" if you see a security warning
   - The app will start automatically!

2. **Desktop Shortcut:**
   - Open Terminal in the folder
   - Type: `chmod +x create_shortcut.sh && ./create_shortcut.sh`
   - You'll get a clickable icon on your desktop

### Linux Users
1. **Quick Start:**
   - Right-click in the folder and select "Open in Terminal"
   - Type: `chmod +x run.sh && ./run.sh`
   - The app will launch automatically

2. **Desktop Shortcut:**
   - In Terminal, type: `chmod +x create_shortcut.sh && ./create_shortcut.sh`
   - You'll get a desktop shortcut for easy access

## ⚙️ What's Happening Behind the Scenes?

When you start the app, it:
1. Checks if you have Python installed (and installs it if needed)
2. Sets up a virtual environment (like a clean room for the app)
3. Installs all required packages
4. Starts the WebUI server
5. Opens the application window

## 🔍 Features

- Easy one-click startup
- Remembers window size and position
- Automatic server management
- Works on Windows, Mac, and Linux
- Native OS integration
- Clear error messages if something goes wrong

## 📋 Requirements

- Python 3.11 or newer (will guide you to install if missing)
- Internet connection for first-time setup
- [Ollama](https://ollama.com/) installed and running

## 🛠️ For Developers

### Project Structure