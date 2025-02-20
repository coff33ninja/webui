#!/usr/bin/env bash

# Exit on error
set -e

# Change to script directory
cd "$(dirname "$0")"

# Function to check Python version
check_python_version() {
    if ! command -v python3 >/dev/null 2>&1; then
        echo "Python 3 is not installed"
        echo "Please install Python 3.11 or newer from https://www.python.org/"
        exit 1
    fi

    # Check Python version
    if ! python3 -c "import sys; assert sys.version_info >= (3, 11), 'Python 3.11 or newer is required'" >/dev/null 2>&1; then
        echo "Python 3.11 or newer is required"
        echo "Current Python version:"
        python3 --version
        exit 1
    fi
}

# Function to create and activate virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        echo "Virtual environment not found! Creating one..."
        python3 -m venv venv || {
            echo "Failed to create virtual environment"
            exit 1
        }
        echo "Installing dependencies..."
        source venv/bin/activate || {
            echo "Failed to activate virtual environment"
            exit 1
        }
        pip install -r requirements.txt || {
            echo "Failed to install dependencies"
            exit 1
        }
    else
        echo "Virtual environment found. Activating..."
    fi

    # Activate virtual environment
    source venv/bin/activate || {
        echo "Failed to activate virtual environment"
        exit 1
    }
}

# Function to run the application
run_app() {
    echo "Starting WebUI..."
    python main.py
    exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "Application exited with error code $exit_code"
        exit $exit_code
    fi
}

# Main execution
echo "Checking Python installation..."
check_python_version

echo "Setting up virtual environment..."
setup_venv

echo "Running application..."
run_app