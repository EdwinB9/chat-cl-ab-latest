#!/bin/bash

echo "Iniciando Chatbot Empresarial..."
echo

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
streamlit run app/main.py

