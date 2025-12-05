@echo off
echo Iniciando Chatbot Empresarial...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar si existe el entorno virtual
if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo No se encontro el entorno virtual. Creando uno nuevo...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Ejecutando aplicacion...
echo Nota: Asegurate de estar en el directorio raiz del proyecto
streamlit run app/main.py

pause

