"""
Componente de sidebar para Streamlit.
Muestra configuración y opciones del usuario.
"""

import streamlit as st
import os
from typing import Dict, Optional
from app.components.help_modal import titulo_con_ayuda, AYUDA_CONFIGURACION
from app.utils.logger import logger
from app.utils.env_loader import load_environment_variables, get_env

# Cargar variables de entorno al importar el módulo (compatible con .env y Streamlit Secrets)
load_environment_variables()


def render_sidebar() -> Dict:
    """
    Renderiza el sidebar con configuraciones.
    
    Returns:
        Dict con las configuraciones seleccionadas
    """
    
    # Colores Casa Limpia para sidebar (modo claro)
    color_titulo = "#1a237e"  # Azul oscuro profundo Casa Limpia
    bg_gradiente = "rgba(0, 172, 193, 0.1)"  # Turquesa Casa Limpia
    bg_gradiente_end = "rgba(0, 172, 193, 0.05)"
    border_color = "#00acc1"  # Turquesa principal
    
    with st.sidebar:
        # Título mejorado del sidebar (adaptado al tema Casa Limpia)
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, {bg_gradiente} 0%, {bg_gradiente_end} 100%); 
                        border-left: 4px solid {border_color}; 
                        border-radius: 0.5rem; 
                        padding: 1rem; 
                        margin-bottom: 1.5rem;
                        animation: fadeIn 0.3s ease-out;">
                <h1 style="margin: 0; color: {color_titulo}; font-size: 1.75rem;">
                    ⚙️ Configuración
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Botón de ayuda visible justo después del título
        if st.button("❓ Ayuda de Configuración", key="help_config_btn", use_container_width=True, type="secondary"):
            logger.info("BOTÓN SIDEBAR: Ayuda de Configuración")
            try:
                st.session_state.show_config_help = not st.session_state.get("show_config_help", False)
                st.rerun()
            except Exception as e:
                logger.error(f"❌ Error en st.rerun() después de ayuda config: {e}", exc_info=True)
                st.exception(e)
        
        # Mostrar ayuda si está activada
        if st.session_state.get("show_config_help", False):
            st.markdown("---")
            st.markdown("### ℹ️ Ayuda de Configuración")
            from app.components.help_modal import AYUDA_CONFIGURACION
            st.markdown(AYUDA_CONFIGURACION)
            if st.button("✅ Cerrar ayuda", key="close_config_help", use_container_width=True, type="primary"):
                logger.info("BOTÓN SIDEBAR: Cerrar ayuda")
                try:
                    st.session_state.show_config_help = False
                    st.rerun()
                except Exception as e:
                    logger.error(f"❌ Error en st.rerun() después de cerrar ayuda: {e}", exc_info=True)
                    st.exception(e)
            st.markdown("---")
        
        # Verificar API keys desde variables de entorno (compatible con .env y Streamlit Secrets)
        load_environment_variables()
        
        openai_key = get_env("OPENAI_API_KEY", "")
        google_key = get_env("GOOGLE_API_KEY", "") or get_env("GEMINI_API_KEY", "")
        groq_key = get_env("GROQ_API_KEY", "")
        together_key = get_env("TOGETHER_API_KEY", "")
        cohere_key = get_env("COHERE_API_KEY", "")
        huggingface_key = get_env("HUGGINGFACE_API_KEY", "")
        
        # Mostrar estado de configuración (solo informativo, sin opción de editar)
        keys_configuradas = []
        if openai_key:
            keys_configuradas.append("🤖 OpenAI")
        if google_key:
            keys_configuradas.append("🔷 Google Gemini")
        if groq_key:
            keys_configuradas.append("⚡ Groq")
        if together_key:
            keys_configuradas.append("🤝 Together AI")
        if cohere_key:
            keys_configuradas.append("💬 Cohere")
        if huggingface_key:
            keys_configuradas.append("🤗 Hugging Face")
        
        if keys_configuradas:
            st.info(f"✅ **Proveedores configurados:** {', '.join(keys_configuradas)}")
        else:
            st.warning(
                "⚠️ **Atención:** Configura al menos una API key en variables de entorno. "
                "Crea un archivo `.env` con OPENAI_API_KEY o GOOGLE_API_KEY."
            )
        
        st.divider()
        
        # Selección de acción
        st.subheader("📋 Acción")
        accion = st.selectbox(
            "Selecciona la acción a realizar:",
            ["Generar", "Corregir", "Resumir"],
            key="accion"
        )
        
        st.divider()
        
        # Configuración de proveedor y modelo
        st.subheader("🤖 Proveedor de IA")
        
        # Importar para obtener proveedores disponibles
        from app.utils.langchain_agent import LangChainAgent
        
        # Obtener proveedores disponibles (el método ya verifica Groq dinámicamente)
        providers_available = LangChainAgent.get_available_providers()
        if not providers_available:
            st.error("❌ No hay proveedores disponibles. Instala las dependencias necesarias.")
            st.stop()
        
        # Filtrar proveedores que tienen API key configurada
        providers_with_key = []
        provider_names = {
            "openai": "OpenAI",
            "gemini": "Google Gemini",
            "groq": "Groq",
            "together": "Together AI",
            "cohere": "Cohere",
            "huggingface": "Hugging Face"
        }
        
        if "openai" in providers_available and openai_key:
            providers_with_key.append("openai")
        if "gemini" in providers_available and google_key:
            providers_with_key.append("gemini")
        
        # Verificar proveedores adicionales dinámicamente
        def check_provider_package(package_name, class_name=None):
            """Verifica si un paquete de proveedor está disponible."""
            try:
                __import__(package_name)
                return True
            except ImportError:
                if class_name:
                    try:
                        from langchain_community import chat_models
                        if hasattr(chat_models, class_name):
                            return True
                    except (ImportError, AttributeError):
                        pass
                return False
        
        # Verificar y agregar proveedores adicionales
        additional_providers = [
            ("groq", "langchain_groq", "ChatGroq", groq_key),
            ("together", "langchain_together", "ChatTogether", together_key),
            ("cohere", "langchain_cohere", "ChatCohere", cohere_key),
            ("huggingface", "langchain_huggingface", "ChatHuggingFace", huggingface_key)
        ]
        
        for provider_id, package_name, class_name, api_key in additional_providers:
            if api_key and check_provider_package(package_name, class_name):
                if provider_id not in providers_with_key:
                    providers_with_key.append(provider_id)
                if provider_id not in providers_available:
                    providers_available.append(provider_id)
        
        
        if not providers_with_key:
            st.warning("⚠️ Configura al menos una API key para usar la aplicación.")
            # Usar el primer proveedor disponible como fallback
            provider_real = providers_available[0] if providers_available else "openai"
            modelo = "gpt-4o-mini"  # Modelo por defecto
        else:
            # Mapeo de nombres amigables solo para proveedores disponibles
            provider_options = [provider_names.get(p, p) for p in providers_with_key]
            
            # Determinar el proveedor por defecto (optimizado para Streamlit 1.28+)
            default_index = 0
            provider_previo = st.session_state.get("provider_previo")
            if provider_previo and provider_previo in providers_with_key:
                default_index = providers_with_key.index(provider_previo)
            
            provider_selected = st.selectbox(
                "Selecciona el proveedor:",
                provider_options,
                index=default_index,
                key="provider_select"
            )
            
            # Obtener el proveedor real del nombre seleccionado
            provider_real = None
            for p, name in provider_names.items():
                if name == provider_selected:
                    provider_real = p
                    break
            
            if provider_real is None:
                provider_real = providers_with_key[0]
            
            # Obtener modelos disponibles para el proveedor seleccionado
            modelos_disponibles = LangChainAgent.get_available_models(provider_real)
            
            # Para Gemini, solo mostrar modelos GRATUITOS
            if provider_real == "gemini":
                # Obtener solo modelos gratuitos disponibles dinámicamente
                available_gemini_models = LangChainAgent.list_available_gemini_models()
                if available_gemini_models:
                    # Crear un diccionario con los modelos gratuitos disponibles
                    modelos_dinamicos = {model: model for model in available_gemini_models}
                    # Combinar con los modelos predefinidos (todos gratuitos), dando prioridad a los dinámicos
                    modelos_disponibles = {**modelos_dinamicos, **modelos_disponibles}
                # Asegurar que solo mostramos modelos gratuitos (filtrar cualquier modelo no gratuito)
                modelos_gratuitos = LangChainAgent.get_available_models("gemini")
                # Filtrar para mantener solo los que están en la lista de gratuitos
                modelos_disponibles = {k: v for k, v in modelos_disponibles.items() if k in modelos_gratuitos}
            
            modelo_keys = list(modelos_disponibles.keys())
            
            # Seleccionar modelo (optimizado para Streamlit 1.28+)
            if modelo_keys:
                modelo_index = 0
                modelo_previo = st.session_state.get("modelo_previo")
                provider_previo_check = st.session_state.get("provider_previo")
                if modelo_previo and provider_previo_check == provider_real and modelo_previo in modelo_keys:
                    modelo_index = modelo_keys.index(modelo_previo)
                
                modelo = st.selectbox(
                    f"Modelo {provider_names.get(provider_real, provider_real)}:",
                    modelo_keys,
                    index=modelo_index,
                    key="modelo"
                )
            else:
                modelo = "gpt-4o-mini"  # Fallback
                st.warning(f"No hay modelos disponibles para {provider_selected}")
        
        # Guardar selección anterior
        st.session_state.provider_previo = provider_real
        st.session_state.modelo_previo = modelo
        
        # Configuración de temperatura
        temperatura = st.slider(
            "Temperatura (creatividad):",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Valores más bajos = más consistente, valores más altos = más creativo",
            key="temperatura"
        )
        
        st.divider()
        
        # Configuración de longitud
        st.subheader("📏 Longitud")
        max_palabras = st.number_input(
            "Palabras máximas:",
            min_value=50,
            max_value=2000,
            value=200,
            step=50,
            key="max_palabras"
        )
        
        st.divider()
        
        # Información
        st.subheader("ℹ️ Información")
        st.info(
            "💡 **Tip**: Los textos aprobados se usan como referencia "
            "para mejorar el estilo de futuras generaciones."
        )
    
    return {
        "accion": accion.lower(),
        "provider": provider_real,
        "modelo": modelo,
        "temperatura": temperatura,
        "max_palabras": max_palabras
    }

