#!/bin/bash

echo "IMAGE JAIL BOOTH"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Change to the project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Run quick test
echo ""
echo "Running quick system test..."
python tests/quick_test.py

# Ask if user wants to continue
echo ""
read -p "Start The Slammer application? (Y/N): " choice
case "$choice" in 
    [yY]|[yY][eE][sS] )
        echo ""
        echo "Starting The Slammer..."
        python src/main.py
        ;;
    * )
        echo ""
        echo "To start manually, run: python src/main.py"
        ;;
esac
