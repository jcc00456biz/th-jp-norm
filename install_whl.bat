@echo off
setlocal enabledelayedexpansion

REM distフォルダの存在確認
if not exist dist (
    echo [ERROR] dist folder does not exist. Please build the package first.
    exit /b 1
)

REM dist以下にある最も新しい.whlファイルのファイル名を取得する
for /f "delims=" %%i in ('dir /b /o:-d dist\*.whl 2^>nul') do (
    set "LATEST_WHL=%%i"
    goto :found
)

echo [ERROR] No wheel files found in dist folder.
exit /b 1

:found
echo Found latest wheel: %LATEST_WHL%
echo Installing...

python -m pip install "dist\%LATEST_WHL%"  --force-reinstall

echo Installation completed successfully.
