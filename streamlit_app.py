"""
Punto de entrada principal para Streamlit Cloud.
Este archivo debe estar en la raíz del proyecto para que Streamlit Cloud lo reconozca.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path de Python
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importar y ejecutar la aplicación principal
from app.main import *



