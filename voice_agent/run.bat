@echo off
echo Check for dependencies...
pip install -r requirements.txt
echo.
echo Starting Jarvis UI...
python gui.py
pause
