@echo off
echo ========================================
echo   Cyber IA Platform - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python n'est pas installe ou pas dans le PATH
    echo Telechargez Python depuis https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js n'est pas installe ou pas dans le PATH
    echo Telechargez Node.js depuis https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python detecte
echo [OK] Node.js detecte
echo.

REM Start Backend in new window
echo [1/2] Demarrage du Backend FastAPI...
start "Cyber IA - Backend" cmd /k "cd backend && (if not exist venv python -m venv venv) && venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend in new window
echo [2/2] Demarrage du Frontend Next.js...
start "Cyber IA - Frontend" cmd /k "cd frontend && (if not exist node_modules npm install) && npm run dev"

echo.
echo ========================================
echo   Les serveurs demarrent...
echo ========================================
echo.
echo Backend (API):       http://localhost:8000
echo Backend (Docs):      http://localhost:8000/api/docs
echo Frontend (App):      http://localhost:3000
echo.
echo Attendez quelques secondes que les serveurs soient prets.
echo.
echo Appuyez sur une touche pour ouvrir l'application...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo Application lancee !
echo Fermez cette fenetre pour continuer.
pause

