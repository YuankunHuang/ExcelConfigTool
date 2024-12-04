#!/bin/bash
echo "Initializing environment, creating virtual environment and installing dependencies..."
poetry install --no-root
echo "Environment setup is completed!"
read -p "Press any key to continue..."