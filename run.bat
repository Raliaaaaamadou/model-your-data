@echo off
REM Quick start script for ModelYourData
REM Run this after setup.bat

echo Starting ModelYourData development server...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Start Django development server
python manage.py runserver

echo.
echo Server stopped.
pause
