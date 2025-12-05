"""Utilidades para la aplicación."""

from app.utils.langchain_agent import LangChainAgent
from app.utils.io_manager import IOManager
from app.utils.feedback_manager import FeedbackManager

# Importación robusta de empresa_config para evitar errores en Streamlit Cloud
try:
    from app.utils.empresa_config import EmpresaConfig, get_empresa_config
except (ImportError, KeyError, ModuleNotFoundError):
    # Si falla la importación, crear clases stub
    class EmpresaConfig:
        """Clase stub cuando empresa_config no está disponible."""
        def get_contexto_completo(self):
            return ""
    
    def get_empresa_config(config_path=None):
        """Función stub cuando empresa_config no está disponible."""
        return EmpresaConfig()

from app.utils.text_tools import (
    contar_palabras,
    contar_caracteres,
    limpiar_texto,
    analizar_texto,
    formatear_texto,
    generar_titulo_resumido
)

__all__ = [
    "LangChainAgent",
    "IOManager",
    "FeedbackManager",
    "EmpresaConfig",
    "get_empresa_config",
    "contar_palabras",
    "contar_caracteres",
    "limpiar_texto",
    "analizar_texto",
    "formatear_texto",
    "generar_titulo_resumido"
]

