@echo off
setlocal enabledelayedexpansion

:: バッチファイルの場所へカレントディレクトリを確実に移動
cd /d "%~dp0"

:: 1. ビルド前のクリーンアップ（build, dist フォルダとすべての .egg-info を再帰削除）
if exist build (
    rd /s /q build
)
if exist dist (
    rd /s /q dist
)
for /d /r %%i in (*.egg-info) do (
    if exist "%%i" (
        rd /s /q "%%i"
    )
)

:: 2. パッケージのビルド実行
echo Building package...
python -m build

if errorlevel 1 (
    echo [ERROR] Build failed.
    exit /b 1
)

:: 3. ビルド完了後のクリーンアップ（生成された一時ファイル・フォルダの削除）
echo Cleaning up temporary build files...
if exist build (
    rd /s /q build
)
for /d /r %%i in (*.egg-info) do (
    if exist "%%i" (
        rd /s /q "%%i"
    )
)

echo Build finished successfully.
