@echo off
setlocal

echo [INFO] Activating .venv...
call .\.venv\Scripts\activate

echo [INFO] Installing packages from requirements.txt...
pip install -r requirements.txt

echo [INFO] Completed.
