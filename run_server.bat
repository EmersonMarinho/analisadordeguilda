@echo off
cd /d %~dp0

:: Ativa o ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

:: Define variáveis de ambiente
set FLASK_APP=app.py
set FLASK_ENV=production
set FLASK_DEBUG=0

:: Inicia o servidor
python -m flask run --host=0.0.0.0 --port=5000 