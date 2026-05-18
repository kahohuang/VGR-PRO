@echo off
set PYTHON_EXE=C:\Users\Latop\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
"%PYTHON_EXE%" "%~dp0vgr_ai_assistant.py" analyze --output-dir "%~dp0outputs"
start "" "%~dp0outputs\vgr_dashboard.html"
pause
