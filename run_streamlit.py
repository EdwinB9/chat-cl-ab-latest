"""
Script de entrada para ejecutar la aplicación Streamlit localmente.
Este script se asegura de que el path de Python esté configurado correctamente.

NOTA: Para Streamlit Cloud, usa streamlit_app.py como punto de entrada.
Este archivo es solo para ejecución local: python run_streamlit.py
"""

import sys
import os
from pathlib import Path

# Verificar si estamos en Streamlit Cloud
# Streamlit Cloud establece ciertas variables de entorno o está en /mount/src
is_streamlit_cloud = (
    os.getenv("STREAMLIT_SERVER_PORT") is not None or
    os.getenv("STREAMLIT_SERVER_ADDRESS") is not None or
    "/mount/src" in str(Path(__file__).absolute())
)

if is_streamlit_cloud:
    # Si estamos en Streamlit Cloud, redirigir a streamlit_app.py
    # para evitar conflictos de runtime
    try:
        # Intentar importar streamlit_app si existe
        import importlib.util
        streamlit_app_path = Path(__file__).parent / "streamlit_app.py"
        if streamlit_app_path.exists():
            spec = importlib.util.spec_from_file_location("streamlit_app", streamlit_app_path)
            streamlit_app = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(streamlit_app)
            sys.exit(0)
    except Exception:
        pass
    # Si no se puede importar, simplemente salir sin error
    sys.exit(0)

# Agregar el directorio raíz al path de Python
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Solo ejecutar streamlit si se llama directamente desde la línea de comandos
# y no estamos en un entorno de Streamlit Cloud
if __name__ == "__main__":
    import streamlit.web.cli as stcli
    
    # Ejecutar streamlit con el archivo main.py
    sys.argv = ["streamlit", "run", "app/main.py"]
    sys.exit(stcli.main())

