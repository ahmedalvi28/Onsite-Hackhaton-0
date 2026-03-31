@echo off
REM LinkedIn Automation Scheduler Setup
REM This sets up a Windows Task Scheduler task to run LinkedIn automation
REM Automatically requests administrator privileges

:: Request admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :admin
) else (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:admin
echo ========================================
echo LinkedIn Automation Scheduler Setup
echo ========================================
echo.

echo ✓ Running as administrator

echo.
echo Creating scheduled task...
echo.

REM Get the full path to this script
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%linkedin_scheduler.py"
set "PYTHON_EXE=python"

REM Create task - runs daily at 12:10 AM
schtasks /create /tn "LinkedIn Daily Automation" /tr "\"%PYTHON_EXE%\" \"%PYTHON_SCRIPT%\" --once --task full" /sc daily /st 00:10 /ru "%USERNAME%" /rl highest

if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo SUCCESS! Task created
    echo ========================================
    echo.
    echo Task Name: LinkedIn Daily Automation
    echo Schedule: Daily at 9:00 AM
    echo.
    echo To manually run: python linkedin/linkedin_scheduler.py --once --task full
    echo To delete task: schtasks /delete /tn "LinkedIn Daily Automation" /f
    echo To view tasks: schtasks /query /tn "LinkedIn Daily Automation"
    echo.
) else (
    echo.
    echo ========================================
    echo FAILED to create task
    echo ========================================
    echo.
    echo You may need to run this as administrator.
    echo.
)

pause
