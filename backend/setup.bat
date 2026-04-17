@echo off
echo ========================================
echo    AI PPT Creator - Setup Script
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python first.
    pause
    exit /b
)

echo.
echo [2/4] Installing Flask and dependencies...
python -m pip install --upgrade pip
python -m pip install flask
python -m pip install flask-cors
python -m pip install python-pptx
python -m pip install requests
python -m pip install pillow

echo.
echo [3/4] Creating outputs folder...
if not exist "outputs" mkdir outputs

echo.
echo [4/4] Testing installation...
python -c "import flask; print('✓ Flask installed successfully!')"
python -c "import flask_cors; print('✓ Flask-CORS installed successfully!')"
python -c "import pptx; print('✓ python-pptx installed successfully!')"

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Run: python app.py
echo   2. Open browser to: http://localhost:5000
echo.
pause