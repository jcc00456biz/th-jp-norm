echo off
python -m pip freeze --exclude-editable > requirements-lock.txt
if errorlevel 1 (
    echo [ERROR] Failed to create requirements-lock.txt.
    exit /b 1
)
echo [INFO] Environment snapshot written to requirements-lock.txt.
