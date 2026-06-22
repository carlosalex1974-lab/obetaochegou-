@echo off
title Servidor Backend - OBetaoChegou
cd /d C:\Users\carlo\Documents\codigo\obetaochegou-backend
echo Iniciando a API...
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
pause
