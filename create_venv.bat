@echo off
setlocal

echo [INFO] Creating .venv if not exists...
if not exist .venv (
    python -m venv .venv
)

echo [INFO] Activating .venv...
call .\.venv\Scripts\activate

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo [INFO] Completed.
