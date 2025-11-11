"""
Componente para subir archivos de referencia.
"""

import streamlit as st
from typing import List, Optional


def render_file_uploader() -> List[str]:
    """
    Renderiza el componente para subir archivos de referencia.
    
    Returns:
        Lista de textos extraídos de los archivos
    """
    st.subheader("📎 Archivos de Referencia")
    st.info(
        "💡 Sube archivos .txt o .json con textos de referencia "
        "para mejorar el estilo de las generaciones."
    )
    
    archivos_subidos = st.file_uploader(
        "Selecciona archivos de referencia:",
        type=["txt", "json"],
        accept_multiple_files=True,
        key="archivos_referencia"
    )
    
    textos_referencia = []
    
    if archivos_subidos:
        for archivo in archivos_subidos:
            try:
                contenido = archivo.read().decode('utf-8')
                
                # Determinar tipo de archivo
                tipo = archivo.name.split('.')[-1].lower()
                
                # Cargar textos
                from app.utils.io_manager import IOManager
                io_manager = IOManager()
                textos = io_manager.cargar_archivo_referencia(contenido, tipo)
                textos_referencia.extend(textos)
                
                st.success(f"✅ {archivo.name}: {len(textos)} texto(s) cargado(s)")
            except Exception as e:
                st.error(f"❌ Error al cargar {archivo.name}: {str(e)}")
    
    if textos_referencia:
        st.info(f"📚 {len(textos_referencia)} texto(s) de referencia cargado(s)")
    
    return textos_referencia

