#!/bin/bash

echo "Running configuration tool..."

poetry run python Tools/main.py Excel Output

echo:
echo "Configuration tool running ends."
echo:

read -p "Press any key to continue..."