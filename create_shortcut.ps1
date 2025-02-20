# Run this script to create a desktop shortcut for WebUI

$ErrorActionPreference = 'Stop'

# Get the current script directory
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Create WScript Shell Object
$WshShell = New-Object -ComObject WScript.Shell

# Get desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")

# Create shortcut
$shortcutPath = Join-Path $desktopPath "WebUI.lnk"
$shortcut = $WshShell.CreateShortcut($shortcutPath)

# Set shortcut properties
$shortcut.TargetPath = "cmd.exe"
$shortcut.Arguments = "/c `"`"$scriptPath\run.bat`"`""
$shortcut.WorkingDirectory = $scriptPath
$shortcut.Description = "Launch WebUI"

# You can set an icon if you have one
# $shortcut.IconLocation = "$scriptPath\icon.ico"

# Save the shortcut
$shortcut.Save()

Write-Host "Shortcut created on desktop: $shortcutPath"