"""
Aplicación principal de Streamlit para el Chatbot Empresarial.
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from app.utils import LangChainAgent, IOManager, FeedbackManager, contar_palabras
from app.components import render_sidebar, render_result_display, render_file_uploader

# Cargar variables de entorno
load_dotenv()


# Configuración de la página
st.set_page_config(
    page_title="Chatbot Empresarial",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🧠 Chatbot Empresarial")
st.markdown("**Genera, corrige y resume textos empresariales con IA**")

# Inicializar session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "io_manager" not in st.session_state:
    st.session_state.io_manager = IOManager()
if "feedback_manager" not in st.session_state:
    st.session_state.feedback_manager = FeedbackManager(st.session_state.io_manager)
if "textos_referencia" not in st.session_state:
    st.session_state.textos_referencia = []
if "resultado_actual" not in st.session_state:
    st.session_state.resultado_actual = None
if "resultado_id" not in st.session_state:
    st.session_state.resultado_id = None

# Renderizar sidebar y obtener configuraciones
config = render_sidebar()

# Verificar que el proveedor seleccionado tenga API key configurada
provider = config.get("provider", "openai")
if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OpenAI API Key no está configurada. Por favor, configura tu API key de OpenAI en el sidebar.")
    st.stop()
elif provider == "gemini" and not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ Google API Key no está configurada. Por favor, configura tu API key de Google en el sidebar.")
    st.stop()

# Inicializar agente con configuraciones
try:
    # Verificar si necesitamos reinicializar el agente
    need_reinit = (
        st.session_state.agent is None or
        st.session_state.agent.provider != config.get("provider", "openai") or
        st.session_state.agent.model_name != config["modelo"] or
        st.session_state.agent.temperature != config["temperatura"]
    )
    
    if need_reinit:
        st.session_state.agent = LangChainAgent(
            provider=config.get("provider", "openai"),
            model_name=config["modelo"],
            temperature=config["temperatura"]
        )
except ValueError as e:
    st.error(f"❌ Error de configuración: {str(e)}")
    st.stop()
except ImportError as e:
    st.error(f"❌ Error de importación: {str(e)}")
    st.info("💡 Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    st.stop()
except Exception as e:
    st.error(f"❌ Error al inicializar el agente: {str(e)}")
    st.stop()

# Actualizar textos de referencia
textos_referencia_nuevos = render_file_uploader()
if textos_referencia_nuevos:
    st.session_state.textos_referencia = textos_referencia_nuevos
    st.session_state.agent.set_reference_texts(st.session_state.textos_referencia)

# También cargar textos aprobados
textos_aprobados = st.session_state.feedback_manager.obtener_textos_aprobados(limite=5)
if textos_aprobados:
    textos_combinados = list(set(st.session_state.textos_referencia + textos_aprobados))
    st.session_state.agent.set_reference_texts(textos_combinados)

# Actualizar estadísticas
estadisticas = st.session_state.feedback_manager.obtener_estadisticas()
st.session_state.estadisticas = estadisticas

# Contenido principal según la acción
st.divider()

accion = config["accion"]

if accion == "generar":
    st.subheader("✨ Generar Texto")
    
    tema = st.text_input(
        "Tema o prompt:",
        placeholder="Ej: Día del Operario de Limpieza",
        key="tema_generar"
    )
    
    instrucciones_adicionales = st.text_area(
        "Instrucciones adicionales (opcional):",
        placeholder="Ej: Incluir un tono más formal, mencionar los valores de la empresa...",
        key="instrucciones_generar"
    )
    
    if st.button("🚀 Generar Texto", type="primary", use_container_width=True):
        if not tema:
            st.error("❌ Por favor, ingresa un tema o prompt.")
        else:
            with st.spinner("⏳ Generando texto..."):
                resultado = st.session_state.agent.generar_texto(
                    tema=tema,
                    max_palabras=config["max_palabras"],
                    instrucciones_adicionales=instrucciones_adicionales
                )
                
                texto_generado = resultado["texto"]
                palabras = contar_palabras(texto_generado)
                
                # Guardar resultado
                resultado_id = st.session_state.io_manager.guardar_resultado(
                    accion="generar",
                    tema=tema,
                    resultado=texto_generado,
                    palabras=palabras,
                    modelo=f"{config.get('provider', 'openai')}/{config['modelo']}",
                    config={
                        "provider": config.get("provider", "openai"),
                        "temperature": config["temperatura"],
                        "max_palabras": config["max_palabras"]
                    }
                )
                
                st.session_state.resultado_actual = texto_generado
                st.session_state.resultado_id = resultado_id
                
                st.success("✅ Texto generado exitosamente!")
                
                # Mostrar información de tokens
                if resultado.get("tokens_usados"):
                    st.info(f"📊 Tokens usados: {resultado['tokens_usados']} | Costo: ${resultado.get('costo', 0):.4f}")

elif accion == "corregir":
    st.subheader("✏️ Corregir Texto")
    
    texto_original = st.text_area(
        "Texto a corregir:",
        height=200,
        placeholder="Pega aquí el texto que deseas corregir...",
        key="texto_corregir"
    )
    
    instrucciones_adicionales = st.text_area(
        "Instrucciones de corrección (opcional):",
        placeholder="Ej: Mejorar la fluidez, corregir errores ortográficos, hacer más formal...",
        key="instrucciones_corregir"
    )
    
    if st.button("🔧 Corregir Texto", type="primary", use_container_width=True):
        if not texto_original:
            st.error("❌ Por favor, ingresa un texto para corregir.")
        else:
            with st.spinner("⏳ Corrigiendo texto..."):
                resultado = st.session_state.agent.corregir_texto(
                    texto=texto_original,
                    instrucciones_adicionales=instrucciones_adicionales
                )
                
                texto_corregido = resultado["texto"]
                palabras = contar_palabras(texto_corregido)
                
                # Guardar resultado
                resultado_id = st.session_state.io_manager.guardar_resultado(
                    accion="corregir",
                    tema=texto_original[:100] + "..." if len(texto_original) > 100 else texto_original,
                    resultado=texto_corregido,
                    palabras=palabras,
                    modelo=f"{config.get('provider', 'openai')}/{config['modelo']}",
                    config={
                        "provider": config.get("provider", "openai"),
                        "temperature": config["temperatura"],
                        "instrucciones": instrucciones_adicionales
                    }
                )
                
                st.session_state.resultado_actual = texto_corregido
                st.session_state.resultado_id = resultado_id
                
                st.success("✅ Texto corregido exitosamente!")
                
                # Mostrar información de tokens
                if resultado.get("tokens_usados"):
                    st.info(f"📊 Tokens usados: {resultado['tokens_usados']} | Costo: ${resultado.get('costo', 0):.4f}")

elif accion == "resumir":
    st.subheader("🔍 Resumir Texto")
    
    texto_original = st.text_area(
        "Texto a resumir:",
        height=200,
        placeholder="Pega aquí el texto que deseas resumir...",
        key="texto_resumir"
    )
    
    instrucciones_adicionales = st.text_area(
        "Instrucciones de resumen (opcional):",
        placeholder="Ej: Enfocarse en los puntos principales, mantener el tono profesional...",
        key="instrucciones_resumir"
    )
    
    if st.button("📝 Resumir Texto", type="primary", use_container_width=True):
        if not texto_original:
            st.error("❌ Por favor, ingresa un texto para resumir.")
        else:
            with st.spinner("⏳ Resumiendo texto..."):
                resultado = st.session_state.agent.resumir_texto(
                    texto=texto_original,
                    max_palabras=config["max_palabras"],
                    instrucciones_adicionales=instrucciones_adicionales
                )
                
                texto_resumido = resultado["texto"]
                palabras = contar_palabras(texto_resumido)
                
                # Guardar resultado
                resultado_id = st.session_state.io_manager.guardar_resultado(
                    accion="resumir",
                    tema=texto_original[:100] + "..." if len(texto_original) > 100 else texto_original,
                    resultado=texto_resumido,
                    palabras=palabras,
                    modelo=f"{config.get('provider', 'openai')}/{config['modelo']}",
                    config={
                        "provider": config.get("provider", "openai"),
                        "temperature": config["temperatura"],
                        "max_palabras": config["max_palabras"],
                        "instrucciones": instrucciones_adicionales
                    }
                )
                
                st.session_state.resultado_actual = texto_resumido
                st.session_state.resultado_id = resultado_id
                
                st.success("✅ Texto resumido exitosamente!")
                
                # Mostrar información de tokens
                if resultado.get("tokens_usados"):
                    st.info(f"📊 Tokens usados: {resultado['tokens_usados']} | Costo: ${resultado.get('costo', 0):.4f}")

# Mostrar resultado si existe
if st.session_state.resultado_actual:
    st.divider()
    
    def manejar_feedback(resultado_id: str, aprobado: bool, comentario: str = ""):
        """Maneja el feedback del usuario."""
        st.session_state.feedback_manager.registrar_feedback(
            resultado_id=resultado_id,
            aprobado=aprobado,
            comentario=comentario
        )
        # Actualizar estadísticas
        estadisticas = st.session_state.feedback_manager.obtener_estadisticas()
        st.session_state.estadisticas = estadisticas
    
    render_result_display(
        resultado=st.session_state.resultado_actual,
        resultado_id=st.session_state.resultado_id,
        accion=accion,
        on_feedback=manejar_feedback
    )

# Sección de historial
st.divider()
st.subheader("📚 Historial del Mes")

if st.button("🔄 Actualizar Historial", use_container_width=True):
    st.rerun()

historial = st.session_state.io_manager.obtener_historial_mes()

if historial:
    # Mostrar últimos 5 resultados
    for registro in historial[-5:][::-1]:
        with st.expander(f"📄 {registro['accion'].capitalize()} - {registro['id']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Tema:** {registro['tema']}")
                st.write(f"**Palabras:** {registro['palabras']}")
                st.write(f"**Modelo:** {registro['modelo']}")
            with col2:
                feedback = registro.get("feedback", {})
                if feedback:
                    aprobado = feedback.get("aprobado", None)
                    if aprobado is True:
                        st.success("👍 Aprobado")
                    elif aprobado is False:
                        st.error("👎 Rechazado")
                    if feedback.get("comentario"):
                        st.write(f"**Comentario:** {feedback['comentario']}")
                else:
                    st.info("⏳ Sin feedback")
            
            st.text_area(
                "Resultado:",
                value=registro["resultado"],
                height=100,
                key=f"historial_{registro['id']}",
                disabled=True
            )
else:
    st.info("📭 No hay historial disponible para este mes.")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🧠 Chatbot Empresarial v1.0 | Powered by Streamlit + LangChain + OpenAI"
    "</div>",
    unsafe_allow_html=True
)

