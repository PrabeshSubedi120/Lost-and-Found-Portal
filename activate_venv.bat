@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated!
echo.
echo To run Django:
echo   python manage.py runserver
echo.
echo To deactivate:
echo   deactivate
echo.
cmd /k
