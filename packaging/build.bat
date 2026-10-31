@echo off
setlocal

cd /d "%~dp0\.."

if exist .venv\Scripts\pyinstaller.exe (
    call .venv\Scripts\activate.bat
)

echo === Generating application icon ===
python tools\make_icon.py || goto :error

echo === Building PixVault.exe with PyInstaller ===
python -m PyInstaller --clean --noconfirm PixVault.spec || goto :error

echo.
echo ================================================
echo Build complete:
echo   dist\PixVault.exe
echo ================================================
goto :eof

:error
echo.
echo Build failed.  See output above.
exit /b 1
