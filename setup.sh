#!/bin/bash

# ModelYourData - Quick Setup Script

echo "========================================="
echo "  ModelYourData - Setup Script"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p media/uploads
mkdir -p staticfiles

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start server: python manage.py runserver"
echo "  3. Open browser: http://127.0.0.1:8000/"
echo ""
echo "Optional: Create superuser for admin access"
echo "  python manage.py createsuperuser"
echo ""
