@echo off
title Gymnatic Local Launcher
echo ========================================================
echo               Iniciando Gymnatic Localhost
echo ========================================================
echo.
echo 1. Iniciando servidor Backend (FastAPI) en http://localhost:8000...
start "Gymnatic Backend (FastAPI)" cmd /k "cd /d %~dp0backend && venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo 2. Iniciando servidor Frontend (Next.js) en http://localhost:3000...
start "Gymnatic Frontend (Next.js)" cmd /k "cd /d %~dp0frontend && npm run start"

echo.
echo ========================================================
echo Servidores iniciados con exito!
echo - Frontend: http://localhost:3000
echo - Backend API Docs: http://localhost:8000/docs
echo ========================================================
pause
