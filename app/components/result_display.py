"""
Componente para mostrar resultados y gestionar feedback.
"""

import streamlit as st
from typing import Dict, Optional, Callable


def render_result_display(
    resultado: str,
    resultado_id: Optional[str] = None,
    accion: str = "generar",
    on_feedback: Optional[Callable] = None
):
    """
    Renderiza el resultado y permite dar feedback.
    
    Args:
        resultado: Texto resultante
        resultado_id: ID del resultado (opcional)
        accion: Acción realizada
        on_feedback: Callback para manejar feedback
    """
    if not resultado:
        return
    
    st.subheader(f"📝 Resultado ({accion.capitalize()})")
    
    # Mostrar resultado en un área de texto editable
    texto_editado = st.text_area(
        "Texto generado:",
        value=resultado,
        height=300,
        key=f"resultado_{resultado_id}" if resultado_id else "resultado"
    )
    
    # Estadísticas del texto
    from app.utils.text_tools import analizar_texto
    stats = analizar_texto(texto_editado)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Palabras", stats["palabras"])
    with col2:
        st.metric("Caracteres", stats["caracteres"])
    with col3:
        st.metric("Oraciones", stats["oraciones"])
    with col4:
        st.metric("Párrafos", stats["paragrafos"])
    
    st.divider()
    
    # Opciones de feedback
    if resultado_id and on_feedback:
        st.subheader("💬 Feedback")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👍 Me gusta", use_container_width=True, type="primary"):
                comentario = st.session_state.get(f"comentario_{resultado_id}", "")
                on_feedback(resultado_id, aprobado=True, comentario=comentario)
                st.success("¡Feedback registrado! ✅")
                st.rerun()
        
        with col2:
            if st.button("👎 No me gusta", use_container_width=True):
                comentario = st.session_state.get(f"comentario_{resultado_id}", "")
                on_feedback(resultado_id, aprobado=False, comentario=comentario)
                st.info("Resultado movido a rechazados.")
                st.rerun()
        
        # Comentario opcional
        comentario = st.text_area(
            "Comentario (opcional):",
            key=f"comentario_{resultado_id}",
            placeholder="Escribe tu comentario sobre el resultado..."
        )
    
    # Botones de descarga
    st.divider()
    st.subheader("💾 Descargar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Descargar como TXT",
            data=texto_editado,
            file_name=f"resultado_{accion}_{resultado_id or 'nuevo'}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        import json
        data_json = json.dumps({
            "accion": accion,
            "resultado": texto_editado,
            "estadisticas": stats
        }, ensure_ascii=False, indent=2)
        st.download_button(
            label="📦 Descargar como JSON",
            data=data_json,
            file_name=f"resultado_{accion}_{resultado_id or 'nuevo'}.json",
            mime="application/json",
            use_container_width=True
        )

