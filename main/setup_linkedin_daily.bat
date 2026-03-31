@echo off
REM Setup LinkedIn Daily Auto-Posting Task

echo Setting up LinkedIn Daily Auto-Posting...

REM Get the current directory
set "PROJECT_DIR=%~dp0"
set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

REM Set Python path
set "PYTHON_PATH=python"

REM ========================================
REM LinkedIn Daily Auto-Post Task
REM ========================================
echo.
echo Creating LinkedIn Daily Auto-Post task...
echo Will post automatically at 9:00 AM daily
echo.

schtasks /create /tn "AI_Employee_LinkedInDailyPost" ^
    /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\linkedin_auto_daily.py\"" ^
    /sc daily /st 09:00 ^
    /f

if %errorlevel% equ 0 (
    echo [OK] LinkedIn Daily Auto-Post scheduled (runs daily at 9:00 AM)
) else (
    echo [ERROR] Failed to schedule LinkedIn Daily Auto-Post
)

echo.
echo ========================================
echo To test the daily poster now:
echo   python linkedin_auto_daily.py
echo.
echo To view scheduled tasks:
echo   schtasks /query /fo LIST /v1 /fi "TaskName eq 'AI_Employee_LinkedInDailyPost'"
echo.
echo To delete later:
echo   schtasks /delete /tn "AI_Employee_LinkedInDailyPost"
echo ========================================
echo.
pause
