@echo off
title Hospital Stock - Iniciador Rapido
color 0B
echo ===================================================
echo             HOSPITAL STOCK - RUNNER
echo ===================================================
echo.

cd /d "%~dp0"

:: Verificar si el entorno virtual existe
if not exist .venv (
    echo [ERROR] No se encontro la carpeta de entorno virtual .venv en:
    echo         %CD%
    echo.
    echo Por favor asegurese de tener el entorno instalado.
    pause
    exit /b
)

echo [INFO] Detectado entorno virtual .venv.
echo [INFO] Iniciando el servidor de desarrollo de Django...
echo.

:: Iniciar el servidor en una ventana nueva y minimizada o separada
start "Servidor Hospital Stock" cmd /k "color 0E && title Servidor Django - Hospital Stock && echo Levantando Django... && .venv\Scripts\activate && python hospital_stock\manage.py runserver"

echo [INFO] Esperando a que el servidor web se inicialice...
timeout /t 3 /nobreak > nul

echo [INFO] Abriendo la aplicacion en su navegador predeterminado...
start http://127.0.0.1:8000/

echo.
echo ===================================================
echo [OK] Servidor en ejecucion.
echo [OK] Puede dejar esta ventana abierta o cerrarla.
echo ===================================================
timeout /t 5
