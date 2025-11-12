#!/bin/bash

echo "Iniciando Chatbot Empresarial..."
echo

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Verificar si existe el entorno virtual
if [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
else
    echo "No se encontró el entorno virtual. Creando uno nuevo..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

echo
echo "Ejecutando aplicación..."
echo "Nota: Asegúrate de estar en el directorio raíz del proyecto"
streamlit run app/main.py

