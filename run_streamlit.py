"""
Script de entrada para ejecutar la aplicación Streamlit.
Este script se asegura de que el path de Python esté configurado correctamente.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importar y ejecutar la aplicación
import streamlit.web.cli as stcli

if __name__ == "__main__":
    # Ejecutar streamlit con el archivo main.py
    sys.argv = ["streamlit", "run", "app/main.py"]
    sys.exit(stcli.main())




