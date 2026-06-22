@echo off
echo Iniciando o Backend OBetãoChegou (API na porta 8000)...
cd /d C:\Users\carlo\Documents\codigo\obetaochegou-backend
call venv\Scripts\activate.bat
uvicorn app.main:app --reload
pause
