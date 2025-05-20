#!/bin/bash

# Define the virtual environment directory name
VENV_DIR=".venv"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please check your Python 3 installation."
        exit 1
    fi
else
    echo "Virtual environment $VENV_DIR already exists."
fi

# Activate the virtual environment
# For bash shell, the activate script is in $VENV_DIR/bin/activate
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "Activation script not found: $VENV_DIR/bin/activate"
    echo "Please ensure the virtual environment was created correctly."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    exit 1
fi

# Run the Python script
echo "Running the PDF parser script..."
cd api && python3 pdf_schedule_parser.py

# Deactivate the virtual environment (optional, as script ends)
# deactivate

echo "Script finished."
