@echo off
setlocal
cd /d "%~dp0"

python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

python -m pip install pyinstaller
if errorlevel 1 exit /b 1

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist HandMouseControl.spec del /q HandMouseControl.spec

python -m PyInstaller --noconfirm --clean --onefile --windowed --icon=icon.ico --add-data "hand_landmarker.task;." --collect-all mediapipe --hidden-import=tkinter --hidden-import=tkinter.ttk --name HandMouseControl main.py
if errorlevel 1 exit /b 1

echo.
echo Built: dist\HandMouseControl.exe
endlocal
