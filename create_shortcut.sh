#!/usr/bin/env bash

# Exit on error
set -e

# Get absolute path to the application directory
APP_DIR="$(cd "$(dirname "$0")" && pwd)"

# Desktop entry content
read -r -d '' DESKTOP_ENTRY << EOM
[Desktop Entry]
Version=1.0
Type=Application
Name=WebUI
Comment=Launch WebUI Application
Exec=bash -c "cd '$APP_DIR' && ./run.sh"
Terminal=false
Categories=Development;
EOM

# Function to create desktop entry for Linux
create_linux_shortcut() {
    local desktop_file="$HOME/.local/share/applications/webui.desktop"
    echo "Creating Linux desktop entry..."
    mkdir -p "$(dirname "$desktop_file")"
    echo "$DESKTOP_ENTRY" > "$desktop_file"
    chmod +x "$desktop_file"
    echo "Desktop entry created at: $desktop_file"
    
    # Create symbolic link on Desktop (optional)
    local desktop_shortcut="$HOME/Desktop/WebUI.desktop"
    ln -sf "$desktop_file" "$desktop_shortcut"
    chmod +x "$desktop_shortcut"
    echo "Desktop shortcut created at: $desktop_shortcut"
}

# Function to create macOS shortcut
create_macos_shortcut() {
    local desktop_dir="$HOME/Desktop"
    local app_name="WebUI.command"
    local shortcut="$desktop_dir/$app_name"
    
    echo "Creating macOS shortcut..."
    echo '#!/usr/bin/env bash' > "$shortcut"
    echo "cd '$APP_DIR' && ./run.sh" >> "$shortcut"
    chmod +x "$shortcut"
    echo "Shortcut created at: $shortcut"
}

# Make run.sh executable
chmod +x "$APP_DIR/run.sh"

# Create appropriate shortcut based on OS
case "$(uname -s)" in
    Linux*)
        create_linux_shortcut
        ;;
    Darwin*)
        create_macos_shortcut
        ;;
    *)
        echo "Unsupported operating system"
        exit 1
        ;;
esac

echo "Done! You can now launch WebUI from your desktop."