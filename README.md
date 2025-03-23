# WebUI Wrapper

A user-friendly application wrapper for Open-WebUI with persistent settings and native OS integration.

## 🚀 Quick Setup (For Everyone!)

### Windows Users
1. **Super Easy Start:**
   - Double-click `run.bat`
   - The application will set everything up automatically

2. **Want a Desktop Shortcut?**
   - Right-click `create_shortcut.ps1`
   - Choose "Run with PowerShell"
   - A desktop icon will be created for easy access

### Mac Users
1. **Easy Start:**
   - Open the folder in Finder
   - Right-click `run.sh` and select "Open With" → "Terminal"
   - Click "Open" if you see a security warning
   - The app will start automatically

2. **Desktop Shortcut:**
   - Open Terminal in the folder
   - Run: `chmod +x create_shortcut.sh && ./create_shortcut.sh`
   - A clickable desktop icon will be created

### Linux Users
1. **Quick Start:**
   - Right-click in the folder and select "Open in Terminal"
   - Run: `chmod +x run.sh && ./run.sh`
   - The app will launch automatically

2. **Desktop Shortcut:**
   - Open Terminal and run: `chmod +x create_shortcut.sh && ./create_shortcut.sh`
   - A desktop shortcut will be created

## ⚙️ What's Happening Behind the Scenes?

When you start the app, it:
1. Checks if Python is installed (installs it if needed)
2. Sets up a virtual environment (isolated workspace for dependencies)
3. Installs all required packages
4. Starts the WebUI server
5. Opens the application window

## 🔍 Features

- One-click startup
- Remembers window size and position
- Automatic server management
- Cross-platform support (Windows, Mac, Linux)
- Native OS integration
- Clear error messages for troubleshooting

## 📋 Requirements

- [Internet connection for first-time setup](https://www.speedtest.net/)
- [Git](https://git-scm.com/) (for cloning the repository)
- [Python 3.11](https://www.python.org/downloads/release/python-3119/) prefered (installer will guide you if missing)
- [Ollama](https://ollama.com/) installed and running

## Upgrading Open-Webui
   ```bash
pip install --upgrade open-webui
   ```
   
## 🛠️ For Developers

### Project Structure
```
webui/
├── main.py              # Main application code
├── config.py            # Settings management
├── server_manager.py    # Server control
├── ui_manager.py        # Window management
├── run.bat              # Windows launcher
├── run.sh               # Mac/Linux launcher
├── create_shortcut.ps1  # Windows shortcut creator
├── create_shortcut.sh   # Mac/Linux shortcut creator
├── requirements.txt     # Python dependencies
└── test/                # Unit tests
```

### Key Components

1. **Native Integration:**
   - Windows: Batch and PowerShell scripts
   - Mac/Linux: Bash scripts with OS detection
   - Automatic desktop integration

2. **Modern Features:**
   - Async server management
   - Type-safe configuration
   - Comprehensive logging
   - Error recovery

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/coff33ninja/webui
   cd webui
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the environment and install dependencies:
   ```bash
   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate

   pip install -r requirements.txt
   ```
4. Run tests:
   ```bash
   pytest
   ```

## 📝 Logs
- **Windows:** `%USERPROFILE%\.webui\webui.log`
- **Mac/Linux:** `~/.webui/webui.log`

## 🤔 Common Questions

**Q: The app won't start, what should I do?**
A: Ensure Python is installed. The launcher will guide you if it's missing.

**Q: Where are my settings saved?**
A: In your home directory under `.webui_config.json`

**Q: How do I update the app?**
A: Pull the latest version and restart the app – it will update automatically.

## 🆘 Need Help?
- Check the log file for detailed errors
- Ensure Ollama is running
- Try running the launcher script again
- Open an issue if you need further assistance

## Resource Optimization Philosophy

One of the primary motivations behind this wrapper is to maximize the computational resources available on your machine. Traditional browser-based interfaces, while familiar, tend to consume a significant amount of RAM and CPU power—resources that could otherwise be dedicated to running AI models or processing data. This wrapper is designed to offload as much of that overhead as possible by minimizing the reliance on a full browser window. Instead, it leverages native OS integration and lightweight scripting to launch and manage the interface in a more resource-friendly manner. In essence, your system allocates more power to the core functions of Open WebUI—without modifying any of its core functionality—delivering a smoother and more efficient user experience.

## Remote Access and Flexibility

For users who prefer to use a browser or need remote access, Open WebUI remains fully accessible. By default, it binds to 0.0.0.0:8080, so you can connect using your computer name, domain name, or IP address. This ensures that whether you’re accessing the interface locally or remotely, you can enjoy the benefits of the original Open WebUI without compromise.

## Continuous Improvement Note

I’m always tinkering—constantly adding features and refining the wrapper based on every little idea that comes to mind. As I study and experiment along the way, you might occasionally notice duplicate fixes or iterative updates. Rest assured, this process is all about learning and enhancing the user experience without changing the core functionality of Open WebUI. Your patience and feedback are greatly appreciated as the wrapper evolves!

## 📜 License

MIT License
