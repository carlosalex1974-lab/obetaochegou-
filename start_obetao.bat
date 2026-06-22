@echo off
echo Iniciando o Backend (API na porta 8000)...
start cmd /k "cd /d C:\Users\carlo\Documents\codigo\obetaochegou-backend && venv\Scripts\python.exe -m uvicorn app.main:app --reload"

echo Iniciando o Frontend (Servidor Web na porta 5500)...
start cmd /k "cd /d C:\Users\carlo\Documents\codigo\obetaochegou-frontend && ..\obetaochegou-backend\venv\Scripts\python.exe server.py"

echo Servidores iniciados em novas janelas!
