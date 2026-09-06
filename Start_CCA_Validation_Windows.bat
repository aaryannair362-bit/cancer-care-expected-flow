@echo off
cd /d "%~dp0"
echo CCA Cancer Care AI OS V12.2-PC4.0 - Clinician Validation
echo Open http://127.0.0.1:8765  ^|  Demo PIN: 2026
echo Validation feedback is saved until reset_demo.py is run.
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 server.py
) else (
  python server.py
)
pause
