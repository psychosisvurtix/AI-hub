@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo Starting compilation...
echo.

python -m PyInstaller --name "AI Hub" --windowed --onefile --clean --exclude-module PyQt5 --exclude-module PyQt6 --exclude-module wx --exclude-module gtk --exclude-module gi --add-data "assets;assets" --hidden-import webview --collect-all webview main.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo Build completed!
    echo File: dist\AI Hub.exe
) else (
    echo Build failed!
)

echo.
pause
