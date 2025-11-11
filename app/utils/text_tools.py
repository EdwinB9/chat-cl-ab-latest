"""
Utilidades para procesamiento de texto.
Incluye funciones para contar palabras, limpiar texto, etc.
"""

import re
from typing import List, Dict


def contar_palabras(texto: str) -> int:
    """
    Cuenta el número de palabras en un texto.
    
    Args:
        texto: Texto a analizar
    
    Returns:
        Número de palabras
    """
    if not texto:
        return 0
    palabras = texto.split()
    return len(palabras)


def contar_caracteres(texto: str) -> int:
    """
    Cuenta el número de caracteres en un texto.
    
    Args:
        texto: Texto a analizar
    
    Returns:
        Número de caracteres
    """
    return len(texto) if texto else 0


def limpiar_texto(texto: str) -> str:
    """
    Limpia un texto eliminando espacios extra y caracteres no deseados.
    
    Args:
        texto: Texto a limpiar
    
    Returns:
        Texto limpiado
    """
    if not texto:
        return ""
    
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    # Eliminar caracteres de control
    texto = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', texto)
    
    return texto


def extraer_oraciones(texto: str) -> List[str]:
    """
    Extrae oraciones de un texto.
    
    Args:
        texto: Texto a analizar
    
    Returns:
        Lista de oraciones
    """
    if not texto:
        return []
    
    # Dividir por signos de puntuación
    oraciones = re.split(r'[.!?]+', texto)
    # Limpiar y filtrar oraciones vacías
    oraciones = [limpiar_texto(o) for o in oraciones if limpiar_texto(o)]
    
    return oraciones


def analizar_texto(texto: str) -> Dict:
    """
    Analiza un texto y devuelve estadísticas.
    
    Args:
        texto: Texto a analizar
    
    Returns:
        Dict con estadísticas del texto
    """
    if not texto:
        return {
            "palabras": 0,
            "caracteres": 0,
            "oraciones": 0,
            "paragrafos": 0
        }
    
    palabras = contar_palabras(texto)
    caracteres = contar_caracteres(texto)
    oraciones = len(extraer_oraciones(texto))
    paragrafos = len([p for p in texto.split('\n\n') if p.strip()])
    
    return {
        "palabras": palabras,
        "caracteres": caracteres,
        "oraciones": oraciones,
        "paragrafos": paragrafos
    }


def truncar_texto(texto: str, max_palabras: int) -> str:
    """
    Trunca un texto a un número máximo de palabras.
    
    Args:
        texto: Texto a truncar
        max_palabras: Número máximo de palabras
    
    Returns:
        Texto truncado
    """
    if not texto:
        return ""
    
    palabras = texto.split()
    if len(palabras) <= max_palabras:
        return texto
    
    palabras_truncadas = palabras[:max_palabras]
    return " ".join(palabras_truncadas) + "..."


def formatear_texto(texto: str) -> str:
    """
    Formatea un texto para mejorar su presentación.
    
    Args:
        texto: Texto a formatear
    
    Returns:
        Texto formateado
    """
    if not texto:
        return ""
    
    texto = limpiar_texto(texto)
    # Asegurar que cada párrafo esté separado por doble salto de línea
    paragrafos = [p.strip() for p in texto.split('\n\n') if p.strip()]
    texto_formateado = '\n\n'.join(paragrafos)
    
    return texto_formateado

