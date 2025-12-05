"""
Módulo para cargar variables de entorno de forma compatible con:
- Desarrollo local (.env)
- Streamlit Cloud (secrets)
- Otras plataformas (variables de entorno del sistema)
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Intentar importar streamlit (puede no estar disponible en todos los contextos)
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    st = None


def load_environment_variables():
    """
    Carga variables de entorno desde múltiples fuentes:
    1. Archivo .env (desarrollo local)
    2. Streamlit Secrets (Streamlit Cloud)
    3. Variables de entorno del sistema (producción)
    """
    # 1. Cargar desde .env (para desarrollo local)
    load_dotenv()
    
    # 2. Si estamos en Streamlit Cloud, cargar desde secrets
    if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
        try:
            # Streamlit Cloud almacena secrets en st.secrets
            # Puede ser un dict o un objeto con atributos
            secrets = st.secrets
            
            # Lista de todas las API keys que la app usa
            api_keys = [
                "OPENAI_API_KEY",
                "GOOGLE_API_KEY",
                "GEMINI_API_KEY",  # Alias alternativo
                "GROQ_API_KEY",
                "TOGETHER_API_KEY",
                "COHERE_API_KEY",
                "HUGGINGFACE_API_KEY",
                "APP_DEBUG",
                "MAX_REQUESTS_PER_MINUTE"
            ]
            
            # Cargar cada secret si existe
            for key in api_keys:
                try:
                    # Intentar acceder como dict
                    if isinstance(secrets, dict) and key in secrets:
                        os.environ[key] = str(secrets[key])
                    # Intentar acceder como atributo
                    elif hasattr(secrets, key):
                        os.environ[key] = str(getattr(secrets, key))
                except Exception:
                    # Si falla, continuar con la siguiente
                    pass
        except Exception:
            # Si hay error accediendo a secrets, continuar sin ellos
            pass


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Obtiene una variable de entorno, buscando en múltiples fuentes.
    
    Args:
        key: Nombre de la variable de entorno
        default: Valor por defecto si no se encuentra
        
    Returns:
        Valor de la variable de entorno o default
    """
    # Asegurar que las variables estén cargadas
    load_environment_variables()
    
    # Buscar en variables de entorno del sistema
    return os.getenv(key, default)


def is_streamlit_cloud() -> bool:
    """
    Detecta si la app está corriendo en Streamlit Cloud.
    
    Returns:
        True si está en Streamlit Cloud, False en caso contrario
    """
    if not STREAMLIT_AVAILABLE:
        return False
    
    try:
        # Streamlit Cloud tiene ciertas características que podemos detectar
        # Una forma es verificar si st.secrets está disponible y tiene contenido
        if hasattr(st, 'secrets'):
            # Intentar acceder a secrets para ver si está configurado
            try:
                _ = st.secrets
                return True
            except Exception:
                return False
    except Exception:
        pass
    
    return False


# Cargar variables automáticamente al importar el módulo
load_environment_variables()

