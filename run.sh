#!/bin/bash

# Quick start script for ModelYourData
# Run this after setup.sh

echo "Starting ModelYourData development server..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Start Django development server
python manage.py runserver

echo ""
echo "Server stopped."
