@echo off
:: AI Skills Monitor Deployment Script for Windows
:: Run this file to upload code to GitHub

:: 自动切换到脚本所在目录（D盘）
cd /d "%~dp0"

echo ========================================
echo AI Skills Monitor Deployment Script
echo ========================================
echo.
echo Current directory: %cd%
echo.

:: Check git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Git not found
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git found

:: Check project files
if not exist "src\monitor.py" (
    echo ERROR: Please run this script in the ai-skills-monitor folder
    echo Current folder: %cd%
    pause
    exit /b 1
)

echo [OK] Project files found
echo.

:: Configure git
git config user.email "873974555@qq.com" 2>nul
git config user.name "AI Monitor" 2>nul

:: Initialize git if needed
if not exist ".git" (
    echo Initializing git repository...
    git init
)

:: Add remote
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/yangymy/ai-skills-monitor.git

:: Add files
echo Adding files...
git add .

:: Commit
echo Committing...
git commit -m "Initial commit" 2>nul
if %errorlevel% neq 0 (
    echo [OK] Nothing to commit or already committed
)

:: Push
echo.
echo Pushing to GitHub...
echo NOTE: If asked for password, use GitHub token
echo.
git push -u origin main 2>nul || git push -u origin master 2>nul

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Push failed
    echo Please check:
    echo 1. Are you logged into Git?
    echo 2. Is the repository created on GitHub?
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Code uploaded to GitHub
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. Open this link:
echo    https://github.com/yangymy/ai-skills-monitor/settings/secrets/actions
echo.
echo 2. Click "New repository secret" and add these 5 secrets:
echo.
echo    EMAIL_RECIPIENT = 873974555@qq.com
echo    SMTP_HOST = smtp.qq.com
echo    SMTP_PORT = 587
echo    SMTP_USER = 873974555@qq.com
echo    SMTP_PASSWORD = ncorpyflyeflbbic
echo.
echo 3. Then open:
echo    https://github.com/yangymy/ai-skills-monitor/actions
echo.
echo    Click "I understand..." to enable Actions
echo.
echo 4. Wait 2-3 minutes for the first report email
echo.

pause
