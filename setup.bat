@echo off
REM ModelYourData - Quick Setup Script for Windows

echo =========================================
echo   ModelYourData - Setup Script
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist media\uploads mkdir media\uploads
if not exist staticfiles mkdir staticfiles

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Start server: python manage.py runserver
echo   3. Open browser: http://127.0.0.1:8000/
echo.
echo Optional: Create superuser for admin access
echo   python manage.py createsuperuser
echo.
pause
