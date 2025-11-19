"""
Componente de sidebar para Streamlit.
Muestra configuración y opciones del usuario.
"""

import streamlit as st
from typing import Dict, Optional
from app.components.help_modal import titulo_con_ayuda, AYUDA_CONFIGURACION


def render_sidebar() -> Dict:
    """
    Renderiza el sidebar con configuraciones.
    
    Returns:
        Dict con las configuraciones seleccionadas
    """
    import os
    
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
            st.session_state.show_config_help = not st.session_state.get("show_config_help", False)
            st.rerun()
        
        # Mostrar ayuda si está activada
        if st.session_state.get("show_config_help", False):
            st.markdown("---")
            st.markdown("### ℹ️ Ayuda de Configuración")
            from app.components.help_modal import AYUDA_CONFIGURACION
            st.markdown(AYUDA_CONFIGURACION)
            if st.button("✅ Cerrar ayuda", key="close_config_help", use_container_width=True, type="primary"):
                st.session_state.show_config_help = False
                st.rerun()
            st.markdown("---")
        
        # Verificar y configurar API keys
        st.subheader("🔑 API Keys")
        
        # Función helper para manejar API keys de forma consistente
        def gestionar_api_key(
            key_name: str,
            env_var: str,
            display_name: str,
            help_text: str,
            icon: str = "🔑",
            min_length: int = 10
        ) -> str:
            """
            Gestiona una API key: inicializa, sincroniza y muestra UI.
            
            Args:
                key_name: Nombre de la key en session_state (ej: "openai_api_key")
                env_var: Nombre de la variable de entorno (ej: "OPENAI_API_KEY")
                display_name: Nombre a mostrar en la UI
                help_text: Texto de ayuda
                icon: Icono a mostrar
                min_length: Longitud mínima esperada para validación
            
            Returns:
                La API key actual (puede estar vacía)
            """
            # Inicializar session_state si no existe
            if key_name not in st.session_state:
                st.session_state[key_name] = os.getenv(env_var, "")
            
            # Sincronizar session_state con os.environ
            if st.session_state[key_name] and not os.getenv(env_var):
                os.environ[env_var] = st.session_state[key_name]
            
            # Obtener la key actual
            current_key = st.session_state[key_name] or os.getenv(env_var, "")
            
            # Mostrar UI según si hay key configurada
            if not current_key:
                # Input para ingresar nueva key
                key_input = st.text_input(
                    f"{icon} {display_name}:",
                    type="password",
                    help=help_text,
                    key=f"{key_name}_input",
                    placeholder="sk-... o AIza...",
                    label_visibility="visible"
                )
                if key_input and key_input.strip():
                    cleaned_key = key_input.strip()
                    # Validación básica de formato
                    if len(cleaned_key) < min_length:
                        st.error(f"⚠️ La API key parece ser muy corta (mínimo {min_length} caracteres). Verifica que sea correcta.")
                    elif cleaned_key.startswith("sk-") or cleaned_key.startswith("AIza") or len(cleaned_key) >= min_length:
                        st.session_state[key_name] = cleaned_key
                        os.environ[env_var] = cleaned_key
                        st.success(f"✅ {display_name} guardada correctamente")
                        st.rerun()
                    else:
                        st.warning("⚠️ El formato de la API key no parece correcto. Verifica que sea válida.")
            else:
                # Mostrar key configurada con opción de cambiar
                col_key, col_btn = st.columns([4, 1])
                with col_key:
                    # Mostrar últimos 4 caracteres para verificación
                    masked_key = f"{'•' * max(8, len(current_key) - 4)}{current_key[-4:]}" if len(current_key) > 4 else "•" * len(current_key)
                    st.text_input(
                        f"{icon} {display_name}:",
                        value=masked_key,
                        type="password",
                        disabled=True,
                        key=f"{key_name}_display",
                        help=f"API key configurada (últimos 4 caracteres: {current_key[-4:]})"
                    )
                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True)  # Alinear verticalmente
                    if st.button(
                        "🔄",
                        key=f"change_{key_name}",
                        help="Cambiar API Key",
                        use_container_width=True
                    ):
                        st.session_state[key_name] = ""
                        os.environ.pop(env_var, None)
                        st.info("🔄 API Key eliminada. Ingresa una nueva.")
                        st.rerun()
            
            return current_key
        
        # Gestionar ambas API keys
        openai_key = gestionar_api_key(
            key_name="openai_api_key",
            env_var="OPENAI_API_KEY",
            display_name="OpenAI API Key",
            help_text="Ingresa tu API key de OpenAI. Obtén una en: https://platform.openai.com/api-keys",
            icon="🤖",
            min_length=20
        )
        
        st.markdown("<br>", unsafe_allow_html=True)  # Espaciado
        
        google_key = gestionar_api_key(
            key_name="google_api_key",
            env_var="GOOGLE_API_KEY",
            display_name="Google API Key",
            help_text="Ingresa tu API key de Google Gemini. Obtén una en: https://makersuite.google.com/app/apikey",
            icon="🔷",
            min_length=20
        )
        
        # Estado de configuración mejorado
        st.markdown("<br>", unsafe_allow_html=True)
        keys_configuradas = []
        if openai_key:
            keys_configuradas.append("🤖 OpenAI")
        if google_key:
            keys_configuradas.append("🔷 Google Gemini")
        
        if keys_configuradas:
            st.success(f"✅ **Proveedores configurados:** {', '.join(keys_configuradas)}")
        else:
            st.warning(
                "⚠️ **Atención:** Configura al menos una API key para usar la aplicación. "
                "Puedes usar solo OpenAI, solo Google Gemini, o ambos."
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

