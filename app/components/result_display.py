"""
Componente para mostrar resultados y gestionar feedback.
"""

import streamlit as st
from typing import Dict, Optional, Callable
from app.utils.logger import logger
from app.components.help_modal import titulo_con_ayuda, AYUDA_FEEDBACK


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
    
    # Colores Casa Limpia (modo claro)
    color_titulo = "#1a237e"  # Azul oscuro profundo Casa Limpia
    bg_gradiente = "rgba(0, 172, 193, 0.1)"  # Turquesa Casa Limpia
    bg_gradiente_end = "rgba(0, 172, 193, 0.05)"
    border_color = "#00acc1"  # Turquesa principal
    
    # Título del resultado con mejor diseño (adaptado al tema Casa Limpia)
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, {bg_gradiente} 0%, {bg_gradiente_end} 100%); 
                    border-left: 4px solid {border_color}; 
                    border-radius: 0.5rem; 
                    padding: 1rem 1.5rem; 
                    margin-bottom: 1.5rem;
                    animation: fadeIn 0.3s ease-out;">
            <h2 style="margin: 0; color: {color_titulo}; font-size: 1.5rem;">
                📝 Resultado ({accion.capitalize()})
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Contenedor para el resultado con mejor diseño (modo claro)
    bg_card = "#ffffff"
    border_card = "#b0bec5"
    shadow_card = "0 4px 6px -1px rgba(0, 172, 193, 0.15)"
    
    # Convertir el resultado a HTML si es necesario y envolverlo en el contenedor
    import markdown as md
    resultado_html = md.markdown(resultado, extensions=['nl2br', 'fenced_code'])
    
    st.markdown(
        f"""
        <div style="background: {bg_card}; 
                    border: 1px solid {border_card}; 
                    border-radius: 0.75rem; 
                    padding: 1.5rem; 
                    box-shadow: {shadow_card};
                    margin-bottom: 1.5rem;
                    animation: fadeIn 0.4s ease-out;">
            {resultado_html}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Usar el resultado original para estadísticas y descargas
    texto_editado = resultado
    
    # Estadísticas del texto con mejor diseño
    from app.utils.text_tools import analizar_texto
    stats = analizar_texto(texto_editado)
    
    # Colores Casa Limpia para estadísticas (modo claro)
    bg_stats = "rgba(0, 172, 193, 0.05)"  # Turquesa Casa Limpia
    bg_stats_end = "rgba(0, 172, 193, 0.02)"
    
    # Aplicar estilos directamente a las métricas usando CSS con selector específico
    stats_container_key = f"stats_container_{resultado_id or 'default'}"
    
    # Primero crear las métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📝 Palabras", stats["palabras"])
    with col2:
        st.metric("🔤 Caracteres", stats["caracteres"])
    with col3:
        st.metric("📄 Oraciones", stats["oraciones"])
    with col4:
        st.metric("📑 Párrafos", stats["paragrafos"])
    
    # Aplicar estilos después usando CSS que selecciona el contenedor padre de las métricas
    st.markdown(
        f"""
        <style>
        [data-testid="stMetric"]:first-of-type {{
            margin-top: 0;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Opciones de feedback
    if resultado_id and on_feedback:
        titulo_con_ayuda("💬 Feedback", AYUDA_FEEDBACK, "feedback", nivel="subheader")
        
        # Verificar si el usuario quiere cambiar el feedback
        cambiar_feedback_key = f"cambiar_feedback_{resultado_id}"
        quiere_cambiar = st.session_state.get(cambiar_feedback_key, False)
        
        # Verificar si ya existe feedback (siempre obtenerlo para pre-llenar comentario si es necesario)
        feedback_existente = None
        if resultado_id:
            # Intentar obtener feedback desde io_manager
            try:
                from app.utils.io_manager import IOManager
                io_manager = IOManager()
                feedback_existente = io_manager.obtener_feedback_resultado(resultado_id)
            except:
                pass
        
        # Si ya hay feedback Y no se quiere cambiar, mostrarlo
        if feedback_existente and not quiere_cambiar:
            aprobado = feedback_existente.get("aprobado", None)
            comentario_existente = feedback_existente.get("comentario", "")
            
            if aprobado is True:
                st.success("✅ **Aprobado** - Este resultado ha sido marcado como aprobado.")
            elif aprobado is False:
                st.error("❌ **Rechazado** - Este resultado ha sido movido a rechazados.")
            
            if comentario_existente:
                st.info(f"💬 **Comentario:** {comentario_existente}")
            
            # Permitir cambiar el feedback
            if st.button("🔄 Cambiar Feedback", use_container_width=True, key=f"btn_cambiar_{resultado_id}"):
                logger.info(f"BOTÓN RESULT_DISPLAY: Cambiar Feedback para {resultado_id}")
                try:
                    # Activar el flag para cambiar feedback
                    st.session_state[cambiar_feedback_key] = True
                    st.rerun()
                except Exception as e:
                    logger.error(f"❌ Error en st.rerun() después de cambiar feedback: {e}", exc_info=True)
                    st.exception(e)
        else:
            # No hay feedback o se quiere cambiar, mostrar opciones para dar feedback
            # Si se está cambiando, mostrar mensaje
            if quiere_cambiar and feedback_existente:
                st.info("🔄 Modificando feedback...")
                if st.button("❌ Cancelar", use_container_width=True, key=f"cancelar_{resultado_id}"):
                    logger.info(f"BOTÓN RESULT_DISPLAY: Cancelar cambio de feedback para {resultado_id}")
                    try:
                        st.session_state[cambiar_feedback_key] = False
                        st.rerun()
                    except Exception as e:
                        logger.error(f"❌ Error en st.rerun() después de cancelar: {e}", exc_info=True)
                        st.exception(e)
            
            col1, col2 = st.columns(2)
            
            # Comentario opcional (mostrarlo antes de los botones)
            # Si hay feedback existente, pre-llenar el comentario
            comentario_default = ""
            if feedback_existente and quiere_cambiar:
                comentario_default = feedback_existente.get("comentario", "")
            
            comentario = st.text_area(
                "Comentario (opcional):",
                value=comentario_default,
                key=f"comentario_{resultado_id}",
                placeholder="Escribe tu comentario sobre el resultado...",
                help="Puedes agregar un comentario antes de dar tu feedback"
            )
            
            with col1:
                if st.button("👍 Me gusta", use_container_width=True, type="primary", key=f"me_gusta_{resultado_id}"):
                    logger.info(f"BOTÓN RESULT_DISPLAY: Me gusta para {resultado_id}")
                    try:
                        # Guardar en session_state para evitar pérdida de estado
                        st.session_state[f"feedback_guardado_{resultado_id}"] = {
                            "aprobado": True,
                            "comentario": comentario
                        }
                        logger.info(f"✅ Feedback guardado en session_state para {resultado_id}")
                        on_feedback(resultado_id, aprobado=True, comentario=comentario)
                        logger.info(f"✅ Callback on_feedback ejecutado para {resultado_id}")
                        # Limpiar el flag de cambiar feedback
                        if cambiar_feedback_key in st.session_state:
                            del st.session_state[cambiar_feedback_key]
                        st.success("¡Feedback registrado! ✅")
                        # Usar st.rerun() pero el estado ya está guardado
                        st.rerun()
                    except Exception as e:
                        logger.error(f"❌ ERROR CRÍTICO en botón Me gusta: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al registrar feedback: {str(e)}")
            
            with col2:
                if st.button("👎 No me gusta", use_container_width=True, key=f"no_me_gusta_{resultado_id}"):
                    logger.info(f"BOTÓN RESULT_DISPLAY: No me gusta para {resultado_id}")
                    try:
                        # Guardar en session_state para evitar pérdida de estado
                        st.session_state[f"feedback_guardado_{resultado_id}"] = {
                            "aprobado": False,
                            "comentario": comentario
                        }
                        logger.info(f"✅ Feedback guardado en session_state para {resultado_id}")
                        on_feedback(resultado_id, aprobado=False, comentario=comentario)
                        logger.info(f"✅ Callback on_feedback ejecutado para {resultado_id}")
                        # Limpiar el flag de cambiar feedback
                        if cambiar_feedback_key in st.session_state:
                            del st.session_state[cambiar_feedback_key]
                        st.info("Resultado movido a rechazados. Puedes verlo en el historial.")
                        # No limpiar el resultado inmediatamente, dejar que se muestre el estado
                        st.rerun()
                    except Exception as e:
                        logger.error(f"❌ ERROR CRÍTICO en botón No me gusta: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al registrar feedback: {str(e)}")
    
    # Botones de descarga (el subheader se adapta automáticamente al tema vía CSS)
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

