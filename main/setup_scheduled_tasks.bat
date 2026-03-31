@echo off
REM Setup Windows Task Scheduler for AI Employee Watchers

echo Setting up AI Employee scheduled tasks...

REM Get the current directory
set "PROJECT_DIR=%~dp0"
set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

REM Set Python path (adjust if needed)
set "PYTHON_PATH=python"

REM ========================================
REM File System Watcher Task
REM ========================================
schtasks /create /tn "AI_Employee_FileWatcher" /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\watcher.py\"" /sc minute /mo 1 /f
if %errorlevel% equ 0 (
    echo [OK] File System Watcher scheduled (runs every minute)
) else (
    echo [ERROR] Failed to schedule File System Watcher
)

REM ========================================
REM Gmail Watcher Task
REM ========================================
schtasks /create /tn "AI_Employee_GmailWatcher" /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\gmail_watcher.py\"" /sc minute /mo 5 /f
if %errorlevel% equ 0 (
    echo [OK] Gmail Watcher scheduled (runs every 5 minutes)
) else (
    echo [ERROR] Failed to schedule Gmail Watcher
)

REM ========================================
REM LinkedIn Watcher Task
REM ========================================
schtasks /create /tn "AI_Employee_LinkedInWatcher" /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\linkedin_watcher.py\"" /sc minute /mo 10 /f
if %errorlevel% equ 0 (
    echo [OK] LinkedIn Watcher scheduled (runs every 10 minutes)
) else (
    echo [ERROR] Failed to schedule LinkedIn Watcher
)

REM ========================================
REM Process Tasks Task (twice daily)
REM ========================================
schtasks /create /tn "AI_Employee_ProcessTasks" /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\base_watcher.py\" process" /sc daily /st 09:00 /f
if %errorlevel% equ 0 (
    echo [OK] Process Tasks scheduled (runs daily at 9:00 AM)
) else (
    echo [ERROR] Failed to schedule Process Tasks
)

schtasks /create /tn "AI_Employee_ProcessTasks_PM" /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\base_watcher.py\" process" /sc daily /st 18:00 /f
if %errorlevel% equ 0 (
    echo [OK] Process Tasks PM scheduled (runs daily at 6:00 PM)
) else (
    echo [ERROR] Failed to schedule Process Tasks PM
)

REM ========================================
REM Email MCP Server (run on startup)
REM ========================================
schtasks /create /tn "AI_Employee_EmailServer" /tr "\"%PYTHON_PATH%\" \"%PROJECT_DIR%\email_mcp_server.py\"" /sc onlogon /f
if %errorlevel% equ 0 (
    echo [OK] Email MCP Server scheduled (runs on login)
) else (
    echo [ERROR] Failed to schedule Email MCP Server
)

echo.
echo ========================================
echo Task Scheduler Setup Complete!
echo ========================================
echo.
echo To view all tasks, run: schtasks /query /fo LIST
echo.
echo To delete tasks later, run: delete_scheduled_tasks.bat
echo.
pause
