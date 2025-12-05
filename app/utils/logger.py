"""
Módulo de logging para la aplicación.
Proporciona logging detallado que se puede ver en la consola de Streamlit Cloud.
"""

import logging
import sys
from pathlib import Path

# Configurar el logger
def setup_logger(name: str = "chatbot_clab", level: int = logging.INFO) -> logging.Logger:
    """
    Configura y retorna un logger para la aplicación.
    
    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Handler para consola (se ve en Streamlit Cloud)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formato detallado
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger()

