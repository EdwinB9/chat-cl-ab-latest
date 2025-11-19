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


def generar_titulo_resumido(tema: str, max_caracteres: int = 50) -> str:
    """
    Genera un título resumido con palabras clave del tema.
    Si el tema es muy largo, extrae las palabras más importantes.
    
    Args:
        tema: Tema o texto original
        max_caracteres: Número máximo de caracteres para el título
    
    Returns:
        Título resumido con palabras clave
    """
    if not tema:
        return "Sin tema"
    
    # Limpiar el tema
    tema = limpiar_texto(tema)
    
    # Si el tema es corto, usarlo completo
    if len(tema) <= max_caracteres:
        return tema
    
    # Si es muy largo, extraer palabras clave
    palabras = tema.split()
    
    # Palabras comunes a ignorar (artículos, preposiciones, etc.)
    palabras_ignorar = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'de', 'del', 'a', 'al', 'en', 'por', 'para', 'con', 'sin',
        'sobre', 'bajo', 'entre', 'hasta', 'desde', 'durante',
        'y', 'o', 'pero', 'que', 'cual', 'cuales', 'cuando',
        'donde', 'como', 'porque', 'si', 'no', 'también', 'más'
    }
    
    # Extraer palabras importantes (sustantivos, verbos, adjetivos)
    palabras_importantes = []
    caracteres_usados = 0
    
    for palabra in palabras:
        palabra_lower = palabra.lower().strip('.,;:!?()[]{}"\'')
        
        # Si es una palabra común y ya tenemos palabras importantes, podemos omitirla
        if palabra_lower in palabras_ignorar and len(palabras_importantes) > 0:
            # Solo agregar si no excede el límite
            if caracteres_usados + len(palabra) + 1 <= max_caracteres - 3:  # -3 para "..."
                palabras_importantes.append(palabra)
                caracteres_usados += len(palabra) + 1  # +1 por el espacio
        else:
            # Palabra importante
            if caracteres_usados + len(palabra) + 1 <= max_caracteres - 3:
                palabras_importantes.append(palabra)
                caracteres_usados += len(palabra) + 1
            else:
                break
    
    # Si no se extrajeron palabras importantes, usar las primeras palabras
    if not palabras_importantes:
        palabras_importantes = []
        caracteres_usados = 0
        for palabra in palabras:
            if caracteres_usados + len(palabra) + 1 <= max_caracteres - 3:
                palabras_importantes.append(palabra)
                caracteres_usados += len(palabra) + 1
            else:
                break
    
    # Construir el título
    titulo = " ".join(palabras_importantes)
    
    # Si el título original era más largo, agregar "..."
    if len(tema) > len(titulo):
        titulo = titulo.rstrip() + "..."
    
    return titulo
