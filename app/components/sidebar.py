"""
Componente de sidebar para Streamlit.
Muestra configuración y opciones del usuario.
"""

import streamlit as st
from typing import Dict, Optional


def render_sidebar() -> Dict:
    """
    Renderiza el sidebar con configuraciones.
    
    Returns:
        Dict con las configuraciones seleccionadas
    """
    import os
    
    with st.sidebar:
        st.title("⚙️ Configuración")
        
        # Verificar y configurar API keys
        st.subheader("🔑 API Keys")
        openai_key = os.getenv("OPENAI_API_KEY")
        google_key = os.getenv("GOOGLE_API_KEY")
        
        if not openai_key:
            openai_key_input = st.text_input(
                "OpenAI API Key (opcional):",
                type="password",
                help="Ingresa tu API key de OpenAI si deseas usar modelos OpenAI",
                key="openai_key_input"
            )
            if openai_key_input:
                os.environ["OPENAI_API_KEY"] = openai_key_input
                st.rerun()
        
        if not google_key:
            google_key_input = st.text_input(
                "Google API Key (opcional):",
                type="password",
                help="Ingresa tu API key de Google si deseas usar modelos Gemini",
                key="google_key_input"
            )
            if google_key_input:
                os.environ["GOOGLE_API_KEY"] = google_key_input
                st.rerun()
        
        if not openai_key and not google_key:
            st.warning("⚠️ Configura al menos una API key para usar la aplicación.")
        
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
        
        providers_available = LangChainAgent.get_available_providers()
        if not providers_available:
            st.error("❌ No hay proveedores disponibles. Instala las dependencias necesarias.")
            st.stop()
        
        # Filtrar proveedores que tienen API key configurada
        providers_with_key = []
        provider_names = {
            "openai": "OpenAI",
            "gemini": "Google Gemini"
        }
        
        if "openai" in providers_available and openai_key:
            providers_with_key.append("openai")
        if "gemini" in providers_available and google_key:
            providers_with_key.append("gemini")
        
        if not providers_with_key:
            st.warning("⚠️ Configura al menos una API key para usar la aplicación.")
            # Usar el primer proveedor disponible como fallback
            provider_real = providers_available[0] if providers_available else "openai"
            modelo = "gpt-4o-mini"  # Modelo por defecto
        else:
            # Mapeo de nombres amigables solo para proveedores disponibles
            provider_options = [provider_names.get(p, p) for p in providers_with_key]
            
            # Determinar el proveedor por defecto
            default_index = 0
            if "provider_previo" in st.session_state:
                if st.session_state.provider_previo in providers_with_key:
                    default_index = providers_with_key.index(st.session_state.provider_previo)
            
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
            modelo_keys = list(modelos_disponibles.keys())
            
            # Seleccionar modelo
            if modelo_keys:
                modelo_index = 0
                if "modelo_previo" in st.session_state and st.session_state.provider_previo == provider_real:
                    if st.session_state.modelo_previo in modelo_keys:
                        modelo_index = modelo_keys.index(st.session_state.modelo_previo)
                
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
        
        # Estadísticas
        st.subheader("📊 Estadísticas")
        if "estadisticas" in st.session_state:
            stats = st.session_state.estadisticas
            st.metric("Total", stats.get("total", 0))
            st.metric("Aprobados", stats.get("aprobados", 0))
            st.metric("Tasa de Aprobación", f"{stats.get('tasa_aprobacion', 0):.1f}%")
        
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

