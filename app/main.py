"""
Aplicación principal de Streamlit para el Chatbot Empresarial.
"""

import streamlit as st
import os
import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List
# Agregar el directorio raíz del proyecto al path de Python
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Importar módulos principales PRIMERO (antes del logger para evitar importación circular)
try:
    from app.utils import LangChainAgent, IOManager, FeedbackManager, contar_palabras
except Exception as e:
    # Si falla la importación, mostrar error pero continuar
    print(f"❌ Error al importar utils: {e}")
    import traceback
    traceback.print_exc()
    raise

# Configurar logging DESPUÉS de importar los módulos principales
from app.utils.logger import logger

logger.info("=" * 80)
logger.info("Iniciando aplicación Chatbot CL-AB")
logger.info(f"Project root: {project_root}")
logger.info("=" * 80)
logger.info("✅ Módulos de utils importados correctamente")

try:
    from app.components import render_sidebar, render_result_display, render_file_uploader
    from app.components.help_modal import titulo_con_ayuda, AYUDA_GENERAR, AYUDA_CORREGIR, AYUDA_RESUMIR, AYUDA_HISTORIAL
    logger.info("✅ Módulos de components importados correctamente")
except Exception as e:
    logger.error(f"❌ Error al importar components: {e}", exc_info=True)
    raise

# Importar estilos ANTES de set_page_config
try:
    from app.components.styles import aplicar_estilos_globales, obtener_tema
    logger.info("✅ Estilos importados correctamente")
except Exception as e:
    logger.warning(f"⚠️ Error al importar estilos: {e}")

# Cargar variables de entorno (compatible con .env local y Streamlit Secrets)
from app.utils.env_loader import load_environment_variables
load_environment_variables()
logger.info("✅ Variables de entorno cargadas (desde .env o Streamlit Secrets)")

# Configuración de la página
try:
    st.set_page_config(
        page_title="Chatbot CL-AB",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    logger.info("✅ Configuración de página establecida")
except Exception as e:
    logger.error(f"❌ Error en set_page_config: {e}", exc_info=True)
    # Continuar aunque falle (puede que ya esté configurado)

# Aplicar estilos globales - se adaptarán automáticamente al tema del sistema
try:
    aplicar_estilos_globales()
    logger.info("✅ Estilos globales aplicados")
except Exception as e:
    logger.warning(f"⚠️ Error al aplicar estilos: {e}", exc_info=True)
    st.error(f"Error al aplicar estilos: {str(e)}")
    # Continuar sin estilos si hay un error

# Título principal con mejor diseño (adaptado automáticamente al tema del sistema)
st.markdown(
    """
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem; animation: fadeIn 0.3s ease-out;">
        <h1 id="main-title" style="font-size: 2.5rem; margin-bottom: 0.5rem;">
            🧠 Chatbot CL-AB
        </h1>
        <p id="main-subtitle" style="font-size: 1.1rem; margin: 0;">
            Genera, corrige y resume textos empresariales con IA
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Estilos CSS del título
st.markdown(
    """
    <style>
    #main-title {
        background: linear-gradient(135deg, #00acc1 0%, #00838f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: #00acc1;
    }
    
    #main-subtitle {
        color: #546e7a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar session state de manera eficiente (compatible con Streamlit 1.28+)
# Usar .get() con valores por defecto para mejor rendimiento
try:
    logger.info("Inicializando session_state...")
    st.session_state.setdefault("agent", None)
    logger.info("✅ agent inicializado en session_state")
    
    if "io_manager" not in st.session_state:
        st.session_state.io_manager = IOManager()
        logger.info("✅ io_manager inicializado")
    else:
        logger.info("✅ io_manager ya existe en session_state")
    
    if "feedback_manager" not in st.session_state:
        st.session_state.feedback_manager = FeedbackManager(st.session_state.io_manager)
        logger.info("✅ feedback_manager inicializado")
    else:
        logger.info("✅ feedback_manager ya existe en session_state")
    
    st.session_state.setdefault("textos_referencia", [])
    st.session_state.setdefault("resultado_actual", None)
    st.session_state.setdefault("resultado_id", None)
    logger.info("✅ Session state inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error al inicializar session_state: {e}", exc_info=True)
    st.exception(e)
    st.stop()
# El tema se detecta automáticamente del sistema mediante CSS
# No necesitamos almacenar el tema en session_state

# Renderizar sidebar y obtener configuraciones
try:
    logger.info("Renderizando sidebar...")
    config = render_sidebar()
    logger.info(f"✅ Sidebar renderizado. Config: {config}")
except Exception as e:
    logger.error(f"❌ Error al renderizar sidebar: {e}", exc_info=True)
    st.exception(e)
    st.error("❌ Error al cargar la configuración. Por favor, recarga la página.")
    st.stop()

# Verificar que el proveedor seleccionado tenga API key configurada
from app.utils.env_loader import get_env
provider = config.get("provider", "openai")
if provider == "openai" and not get_env("OPENAI_API_KEY"):
    st.error("❌ OpenAI API Key no está configurada. Por favor, configura tu API key de OpenAI en el sidebar.")
    st.stop()
elif provider == "gemini" and not get_env("GOOGLE_API_KEY"):
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

# Actualizar textos de referencia (incluye archivos guardados persistentes)
textos_referencia_nuevos = render_file_uploader()
if textos_referencia_nuevos:
    st.session_state.textos_referencia = textos_referencia_nuevos
    st.session_state.agent.set_reference_texts(st.session_state.textos_referencia)
elif "textos_referencia" not in st.session_state or not st.session_state.textos_referencia:
    # Si no hay textos nuevos pero tampoco hay en session_state, cargar los guardados
    textos_guardados = st.session_state.io_manager.cargar_archivos_referencia_guardados()
    if textos_guardados:
        st.session_state.textos_referencia = textos_guardados
        st.session_state.agent.set_reference_texts(textos_guardados)

# También cargar textos aprobados
textos_aprobados = st.session_state.feedback_manager.obtener_textos_aprobados(limite=5)
if textos_aprobados:
    textos_combinados = list(set(st.session_state.textos_referencia + textos_aprobados))
    st.session_state.agent.set_reference_texts(textos_combinados)

# Contenido principal según la acción
st.divider()

accion = config["accion"]

if accion == "generar":
    titulo_con_ayuda("✨ Generar Texto", AYUDA_GENERAR, "generar", nivel="subheader")
    
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
        logger.info("=" * 80)
        logger.info("BOTÓN PRESIONADO: Generar Texto")
        logger.info(f"Tema: {tema}")
        logger.info(f"Config: {config}")
        logger.info("=" * 80)
        
        try:
            if not tema:
                logger.warning("⚠️ Tema vacío")
                st.error("❌ Por favor, ingresa un tema o prompt.")
            else:
                logger.info("Iniciando generación de texto...")
                with st.spinner("⏳ Generando texto..."):
                    try:
                        resultado = st.session_state.agent.generar_texto(
                            tema=tema,
                            max_palabras=config["max_palabras"],
                            instrucciones_adicionales=instrucciones_adicionales
                        )
                        logger.info("✅ Texto generado exitosamente")
                        logger.info(f"Resultado keys: {resultado.keys() if isinstance(resultado, dict) else 'No es dict'}")
                    except Exception as e:
                        logger.error(f"❌ Error al generar texto: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al generar texto: {str(e)}")
                        raise
                    
                    try:
                        texto_generado = resultado.get("texto", "") if isinstance(resultado, dict) else str(resultado)
                        logger.info(f"Texto generado (primeros 100 chars): {texto_generado[:100]}")
                        
                        palabras = contar_palabras(texto_generado)
                        logger.info(f"Palabras contadas: {palabras}")
                        
                        # Guardar resultado
                        logger.info("Guardando resultado...")
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
                        logger.info(f"✅ Resultado guardado con ID: {resultado_id}")
                        
                        st.session_state.resultado_actual = texto_generado
                        st.session_state.resultado_id = resultado_id
                        logger.info("✅ Session state actualizado")
                        
                        st.success("✅ Texto generado exitosamente!")
                        
                        # Mostrar información de tokens
                        if resultado.get("tokens_usados"):
                            st.info(f"📊 Tokens usados: {resultado['tokens_usados']} | Costo: ${resultado.get('costo', 0):.4f}")
                        logger.info("✅ Proceso de generación completado")
                    except Exception as e:
                        logger.error(f"❌ Error al procesar resultado: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al procesar el resultado: {str(e)}")
        except Exception as e:
            logger.error(f"❌ ERROR CRÍTICO en botón Generar: {e}", exc_info=True)
            st.exception(e)
            st.error("❌ Ocurrió un error inesperado. Por favor, revisa los logs.")

elif accion == "corregir":
    titulo_con_ayuda("✏️ Corregir Texto", AYUDA_CORREGIR, "corregir", nivel="subheader")
    
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
        logger.info("=" * 80)
        logger.info("BOTÓN PRESIONADO: Corregir Texto")
        logger.info(f"Texto original (primeros 100 chars): {texto_original[:100] if texto_original else 'None'}")
        logger.info("=" * 80)
        
        try:
            if not texto_original:
                logger.warning("⚠️ Texto original vacío")
                st.error("❌ Por favor, ingresa un texto para corregir.")
            else:
                logger.info("Iniciando corrección de texto...")
                with st.spinner("⏳ Corrigiendo texto..."):
                    try:
                        resultado = st.session_state.agent.corregir_texto(
                            texto=texto_original,
                            instrucciones_adicionales=instrucciones_adicionales
                        )
                        logger.info("✅ Texto corregido exitosamente")
                    except Exception as e:
                        logger.error(f"❌ Error al corregir texto: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al corregir texto: {str(e)}")
                        raise
                    
                    try:
                        texto_corregido = resultado.get("texto", "") if isinstance(resultado, dict) else str(resultado)
                        logger.info(f"Texto corregido (primeros 100 chars): {texto_corregido[:100]}")
                        
                        palabras = contar_palabras(texto_corregido)
                        logger.info(f"Palabras contadas: {palabras}")
                        
                        # Guardar resultado
                        logger.info("Guardando resultado...")
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
                        logger.info(f"✅ Resultado guardado con ID: {resultado_id}")
                        
                        st.session_state.resultado_actual = texto_corregido
                        st.session_state.resultado_id = resultado_id
                        logger.info("✅ Session state actualizado")
                        
                        st.success("✅ Texto corregido exitosamente!")
                        
                        # Mostrar información de tokens
                        if resultado.get("tokens_usados"):
                            st.info(f"📊 Tokens usados: {resultado['tokens_usados']} | Costo: ${resultado.get('costo', 0):.4f}")
                        logger.info("✅ Proceso de corrección completado")
                    except Exception as e:
                        logger.error(f"❌ Error al procesar resultado: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al procesar el resultado: {str(e)}")
        except Exception as e:
            logger.error(f"❌ ERROR CRÍTICO en botón Corregir: {e}", exc_info=True)
            st.exception(e)
            st.error("❌ Ocurrió un error inesperado. Por favor, revisa los logs.")

elif accion == "resumir":
    titulo_con_ayuda("🔍 Resumir Texto", AYUDA_RESUMIR, "resumir", nivel="subheader")
    
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
        logger.info("=" * 80)
        logger.info("BOTÓN PRESIONADO: Resumir Texto")
        logger.info(f"Texto original (primeros 100 chars): {texto_original[:100] if texto_original else 'None'}")
        logger.info("=" * 80)
        
        try:
            if not texto_original:
                logger.warning("⚠️ Texto original vacío")
                st.error("❌ Por favor, ingresa un texto para resumir.")
            else:
                logger.info("Iniciando resumen de texto...")
                with st.spinner("⏳ Resumiendo texto..."):
                    try:
                        resultado = st.session_state.agent.resumir_texto(
                            texto=texto_original,
                            max_palabras=config["max_palabras"],
                            instrucciones_adicionales=instrucciones_adicionales
                        )
                        logger.info("✅ Texto resumido exitosamente")
                    except Exception as e:
                        logger.error(f"❌ Error al resumir texto: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al resumir texto: {str(e)}")
                        raise
                    
                    try:
                        texto_resumido = resultado.get("texto", "") if isinstance(resultado, dict) else str(resultado)
                        logger.info(f"Texto resumido (primeros 100 chars): {texto_resumido[:100]}")
                        
                        palabras = contar_palabras(texto_resumido)
                        logger.info(f"Palabras contadas: {palabras}")
                        
                        # Guardar resultado
                        logger.info("Guardando resultado...")
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
                        logger.info(f"✅ Resultado guardado con ID: {resultado_id}")
                        
                        st.session_state.resultado_actual = texto_resumido
                        st.session_state.resultado_id = resultado_id
                        logger.info("✅ Session state actualizado")
                        
                        st.success("✅ Texto resumido exitosamente!")
                        
                        # Mostrar información de tokens
                        if resultado.get("tokens_usados"):
                            st.info(f"📊 Tokens usados: {resultado['tokens_usados']} | Costo: ${resultado.get('costo', 0):.4f}")
                        logger.info("✅ Proceso de resumen completado")
                    except Exception as e:
                        logger.error(f"❌ Error al procesar resultado: {e}", exc_info=True)
                        st.exception(e)
                        st.error(f"❌ Error al procesar el resultado: {str(e)}")
        except Exception as e:
            logger.error(f"❌ ERROR CRÍTICO en botón Resumir: {e}", exc_info=True)
            st.exception(e)
            st.error("❌ Ocurrió un error inesperado. Por favor, revisa los logs.")

# Mostrar resultado si existe
if st.session_state.resultado_actual:
    st.divider()
    
    def manejar_feedback(resultado_id: str, aprobado: bool, comentario: str = ""):
        """Maneja el feedback del usuario."""
        logger.info("=" * 80)
        logger.info(f"MANEJAR FEEDBACK: resultado_id={resultado_id}, aprobado={aprobado}")
        logger.info(f"Comentario: {comentario[:100] if comentario else 'None'}")
        logger.info("=" * 80)
        
        try:
            # Verificar que el resultado existe antes de procesar
            logger.info(f"Buscando resultado con ID: {resultado_id}")
            resultado_existente = st.session_state.io_manager.obtener_resultado_por_id(resultado_id)
            if not resultado_existente:
                logger.warning(f"⚠️ No se encontró resultado con ID: {resultado_id}")
                st.error(f"❌ No se encontró el resultado con ID: {resultado_id}")
                return
            
            logger.info(f"✅ Resultado encontrado, registrando feedback...")
            # Registrar el feedback
            st.session_state.feedback_manager.registrar_feedback(
                resultado_id=resultado_id,
                aprobado=aprobado,
                comentario=comentario
            )
            logger.info(f"✅ Feedback registrado exitosamente para {resultado_id}")
            
            # No limpiar el resultado cuando se rechaza, 
            # para que el usuario pueda ver el estado de rechazado
        except Exception as e:
            logger.error(f"❌ ERROR CRÍTICO al registrar feedback: {e}", exc_info=True)
            st.exception(e)
            st.error(f"❌ Error al registrar feedback: {str(e)}")
    
    render_result_display(
        resultado=st.session_state.resultado_actual,
        resultado_id=st.session_state.resultado_id,
        accion=accion,
        on_feedback=manejar_feedback
    )

# Sección de historial
st.divider()
titulo_con_ayuda("📚 Historial del Mes", AYUDA_HISTORIAL, "historial", nivel="subheader")

# Botón para actualizar
if st.button("🔄 Actualizar Historial", use_container_width=True):
    logger.info("BOTÓN PRESIONADO: Actualizar Historial")
    try:
        st.rerun()
    except Exception as e:
        logger.error(f"❌ Error en st.rerun() después de Actualizar Historial: {e}", exc_info=True)
        st.exception(e)

# Obtener historial completo
historial_completo = st.session_state.io_manager.obtener_historial_completo()
aprobados = historial_completo.get("aprobados", [])
rechazados = historial_completo.get("rechazados", [])
todos = historial_completo.get("todos", aprobados + rechazados)  # Incluye todos: aprobados + rechazados + sin feedback

# Pestañas para filtrar
tab1, tab2, tab3 = st.tabs(["📋 Todos", "✅ Aprobados", "❌ Rechazados"])

def mostrar_registro(registro: Dict, es_rechazado: bool = False, tab_prefix: str = ""):
    """Función auxiliar para mostrar un registro del historial."""
    resultado_id = registro.get("id", "")
    accion = registro.get("accion", "generar")
    tema = registro.get("tema", "")
    
    # Generar título resumido del tema
    from app.utils.text_tools import generar_titulo_resumido
    titulo_resumido = generar_titulo_resumido(tema, max_caracteres=50)
    
    # Determinar el icono según el estado
    if es_rechazado:
        icono = "❌"
        estado_color = "red"
    else:
        feedback = registro.get("feedback", {})
        if feedback.get("aprobado") is True:
            icono = "✅"
            estado_color = "green"
        else:
            icono = "⏳"
            estado_color = "gray"
    
    # Crear claves únicas usando el prefijo de la pestaña
    eliminar_key = f"eliminar_{tab_prefix}_{resultado_id}"
    textarea_key = f"historial_{tab_prefix}_{resultado_id}"
    
    # Formatear el título del expander: Acción - Título Resumido - ID
    titulo_expander = f"{icono} {accion.capitalize()} - {titulo_resumido} - {resultado_id}"
    
    with st.expander(titulo_expander, expanded=False):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(
                """
                <div class="info-container" style="animation: fadeIn 0.3s ease-out;">
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <p style="margin: 0.25rem 0;"><strong>Tema:</strong> {registro['tema']}</p>
                <p style="margin: 0.25rem 0;"><strong>Palabras:</strong> {registro['palabras']}</p>
                <p style="margin: 0.25rem 0;"><strong>Modelo:</strong> {registro['modelo']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
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
        
        with col3:
            # Botones de descarga
            resultado_texto = registro.get("resultado", "")
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                st.download_button(
                    "📄 TXT",
                    data=resultado_texto,
                    file_name=f"resultado_{resultado_id}.txt",
                    mime="text/plain",
                    key=f"descargar_txt_{tab_prefix}_{resultado_id}",
                    use_container_width=True
                )
            
            with col_download2:
                import json
                resultado_json = json.dumps(registro, ensure_ascii=False, indent=2)
                st.download_button(
                    "📦 JSON",
                    data=resultado_json,
                    file_name=f"resultado_{resultado_id}.json",
                    mime="application/json",
                    key=f"descargar_json_{tab_prefix}_{resultado_id}",
                    use_container_width=True
                )
        
        with col4:
            # Botón de eliminación
            if st.button("🗑️ Eliminar", key=eliminar_key, use_container_width=True, type="secondary"):
                logger.info(f"BOTÓN PRESIONADO: Eliminar resultado {resultado_id}")
                try:
                    if st.session_state.io_manager.eliminar_resultado(resultado_id):
                        logger.info(f"✅ Resultado {resultado_id} eliminado exitosamente")
                        st.success("✅ Resultado eliminado")
                        try:
                            st.rerun()
                        except Exception as e:
                            logger.error(f"❌ Error en st.rerun() después de eliminar: {e}", exc_info=True)
                            st.exception(e)
                    else:
                        logger.warning(f"⚠️ No se pudo eliminar resultado {resultado_id}")
                        st.error("❌ Error al eliminar")
                except Exception as e:
                    logger.error(f"❌ Error al eliminar resultado {resultado_id}: {e}", exc_info=True)
                    st.exception(e)
                    st.error(f"❌ Error al eliminar: {str(e)}")
        
        # Contenedor para el resultado con mejor diseño (adaptado automáticamente al tema del sistema)
        st.markdown(
            """
            <div class="historial-container" style="animation: fadeIn 0.3s ease-out;">
            """,
            unsafe_allow_html=True
        )
        # Mostrar resultado siempre en markdown renderizado
        st.markdown(registro["resultado"])

# Función helper para paginación
def paginar_resultados(resultados: List[Dict], items_por_pagina: int = 10, key_prefix: str = "pagina"):
    """
    Maneja la paginación de resultados.
    
    Args:
        resultados: Lista de resultados a paginar
        items_por_pagina: Número de items por página
        key_prefix: Prefijo único para las keys de session_state
    
    Returns:
        Tupla (página_actual, resultados_paginados, total_paginas, total_resultados)
    """
    total_resultados = len(resultados)
    total_paginas = max(1, (total_resultados + items_por_pagina - 1) // items_por_pagina)
    
    # Inicializar página actual en session_state (optimizado para Streamlit 1.28+)
    pagina_key = f"{key_prefix}_actual"
    pagina_actual = st.session_state.get(pagina_key, 1)
    
    # Asegurar que la página esté en rango válido
    if pagina_actual < 1:
        pagina_actual = 1
    elif pagina_actual > total_paginas:
        pagina_actual = total_paginas
    
    # Calcular índices para la página actual
    inicio = (pagina_actual - 1) * items_por_pagina
    fin = inicio + items_por_pagina
    resultados_paginados = resultados[inicio:fin]
    
    return pagina_actual, resultados_paginados, total_paginas, total_resultados

def render_paginacion_mejorada(pagina_actual: int, total_paginas: int, total_resultados: int, 
                                key_prefix: str, items_por_pagina: int = 10):
    """
    Renderiza controles de paginación simples y sutiles.
    
    Args:
        pagina_actual: Página actual
        total_paginas: Total de páginas
        total_resultados: Total de resultados
        key_prefix: Prefijo para las keys únicas
        items_por_pagina: Items por página
    """
    if total_paginas <= 1:
        # Si solo hay una página, solo mostrar el contador
        st.caption(f"📊 {total_resultados} resultado{'s' if total_resultados != 1 else ''}")
        return
    
    # Calcular rango de resultados mostrados
    inicio = (pagina_actual - 1) * items_por_pagina + 1
    fin = min(pagina_actual * items_por_pagina, total_resultados)
    
    # Información sutil
    st.caption(f"📊 Mostrando {inicio}-{fin} de {total_resultados} (Página {pagina_actual}/{total_paginas})")
    
    # Controles de navegación simples - SIEMPRE máximo 5 números de página visibles
    max_pages_visible = 5
    
    # Calcular qué páginas mostrar (SIEMPRE máximo 5, sin importar cuántas páginas haya)
    if total_paginas <= max_pages_visible:
        # Si hay 5 o menos páginas, mostrar todas
        page_numbers = list(range(1, total_paginas + 1))
    else:
        # Si hay más de 5 páginas, mostrar máximo 5 números relevantes
        if pagina_actual <= 3:
            # Cerca del inicio (páginas 1-3): mostrar 1, 2, 3, 4, 5
            page_numbers = list(range(1, max_pages_visible + 1))
        elif pagina_actual >= total_paginas - 2:
            # Cerca del final: mostrar últimas 5 páginas
            page_numbers = list(range(total_paginas - max_pages_visible + 1, total_paginas + 1))
        else:
            # En el medio: mostrar 2 antes, actual, 2 después (siempre 5 números)
            page_numbers = list(range(pagina_actual - 2, pagina_actual + 3))
    
    # Asegurar que nunca se muestren más de 5 números
    assert len(page_numbers) <= max_pages_visible, f"Error: se están mostrando más de {max_pages_visible} páginas"
    
    # Calcular cuántas columnas necesitamos
    # Siempre: [Anterior] [Primera(opcional)] [5 números máx] [Última(opcional)] [Siguiente]
    num_cols_extra = 0
    if total_paginas > max_pages_visible:
        # Mostrar botones primera/última solo si hay más de 5 páginas
        if pagina_actual > 3:
            num_cols_extra += 1  # Botón primera
        if pagina_actual < total_paginas - 2:
            num_cols_extra += 1  # Botón última
    
    total_cols = 2 + len(page_numbers) + num_cols_extra  # Anterior + números + última(opcional) + Siguiente
    
    # Controles de navegación en una sola fila
    cols = st.columns([1] * total_cols)
    
    idx = 0
    
    # Botón Anterior
    with cols[idx]:
        if st.button("◀️", key=f"{key_prefix}_prev", disabled=(pagina_actual <= 1),
                    help="Página anterior", use_container_width=True):
            logger.info(f"BOTÓN PAGINACIÓN: Anterior (de {pagina_actual} a {max(1, pagina_actual - 1)})")
            try:
                st.session_state[f"{key_prefix}_actual"] = max(1, pagina_actual - 1)
                st.rerun()
            except Exception as e:
                logger.error(f"❌ Error en st.rerun() después de página anterior: {e}", exc_info=True)
                st.exception(e)
    idx += 1
    
    # Botón Primera página (solo si hay más de 5 páginas y no estamos en las primeras)
    if total_paginas > max_pages_visible and pagina_actual > 3:
        with cols[idx]:
            if st.button("⏮️", key=f"{key_prefix}_first", help="Primera página", use_container_width=True):
                logger.info(f"BOTÓN PAGINACIÓN: Primera página (de {pagina_actual} a 1)")
                try:
                    st.session_state[f"{key_prefix}_actual"] = 1
                    st.rerun()
                except Exception as e:
                    logger.error(f"❌ Error en st.rerun() después de primera página: {e}", exc_info=True)
                    st.exception(e)
        idx += 1
    
    # Números de página (SIEMPRE máximo 5)
    for page_num in page_numbers:
        with cols[idx]:
            if page_num == pagina_actual:
                # Página actual - sutil pero destacada
                st.markdown(
                    f"""
                    <div style="
                        background: rgba(0, 172, 193, 0.15);
                        color: #00acc1;
                        padding: 0.4rem;
                        border-radius: 0.4rem;
                        text-align: center;
                        font-weight: 600;
                        border: 1px solid rgba(0, 172, 193, 0.3);
                    ">
                        {page_num}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Otras páginas - botones simples
                if st.button(str(page_num), key=f"{key_prefix}_page_{page_num}", 
                           use_container_width=True, help=f"Página {page_num}"):
                    logger.info(f"BOTÓN PAGINACIÓN: Página {page_num} (de {pagina_actual} a {page_num})")
                    try:
                        st.session_state[f"{key_prefix}_actual"] = int(page_num)
                        st.rerun()
                    except Exception as e:
                        logger.error(f"❌ Error en st.rerun() después de página {page_num}: {e}", exc_info=True)
                        st.exception(e)
        idx += 1
    
    # Botón Última página (solo si hay más de 5 páginas y no estamos en las últimas)
    if total_paginas > max_pages_visible and pagina_actual < total_paginas - 2:
        with cols[idx]:
            if st.button("⏭️", key=f"{key_prefix}_last", help="Última página", use_container_width=True):
                logger.info(f"BOTÓN PAGINACIÓN: Última página (de {pagina_actual} a {total_paginas})")
                try:
                    st.session_state[f"{key_prefix}_actual"] = total_paginas
                    st.rerun()
                except Exception as e:
                    logger.error(f"❌ Error en st.rerun() después de última página: {e}", exc_info=True)
                    st.exception(e)
        idx += 1
    
    # Botón Siguiente
    with cols[idx]:
        if st.button("▶️", key=f"{key_prefix}_next", disabled=(pagina_actual >= total_paginas),
                    help="Página siguiente", use_container_width=True):
            logger.info(f"BOTÓN PAGINACIÓN: Siguiente (de {pagina_actual} a {min(total_paginas, pagina_actual + 1)})")
            try:
                st.session_state[f"{key_prefix}_actual"] = min(total_paginas, pagina_actual + 1)
                st.rerun()
            except Exception as e:
                logger.error(f"❌ Error en st.rerun() después de página siguiente: {e}", exc_info=True)
                st.exception(e)

# Pestaña: Todos
with tab1:
    if todos:
        # Ordenar por ID (fecha) descendente
        todos_ordenados = sorted(todos, key=lambda x: x.get("id", ""), reverse=True)
        
        # Paginación
        pagina_actual, todos_paginados, total_paginas, total = paginar_resultados(
            todos_ordenados, items_por_pagina=10, key_prefix="todos_pagina"
        )
        
        # Mostrar controles de paginación mejorados
        render_paginacion_mejorada(pagina_actual, total_paginas, total, "todos_pagina", items_por_pagina=10)
        
        # Mostrar resultados de la página actual
        for registro in todos_paginados:
            # Determinar si es rechazado
            es_rechazado = registro.get("feedback", {}).get("aprobado") is False
            mostrar_registro(registro, es_rechazado, tab_prefix="todos")
    else:
        st.info("📭 No hay historial disponible para este mes.")

# Pestaña: Aprobados
with tab2:
    if aprobados:
        aprobados_ordenados = sorted(aprobados, key=lambda x: x.get("id", ""), reverse=True)
        
        # Paginación
        pagina_actual, aprobados_paginados, total_paginas, total = paginar_resultados(
            aprobados_ordenados, items_por_pagina=10, key_prefix="aprobados_pagina"
        )
        
        # Mostrar controles de paginación mejorados
        render_paginacion_mejorada(pagina_actual, total_paginas, total, "aprobados_pagina", items_por_pagina=10)
        
        # Mostrar resultados de la página actual
        for registro in aprobados_paginados:
            mostrar_registro(registro, es_rechazado=False, tab_prefix="aprobados")
    else:
        st.info("📭 No hay resultados aprobados para este mes.")

# Pestaña: Rechazados
with tab3:
    if rechazados:
        rechazados_ordenados = sorted(rechazados, key=lambda x: x.get("id", ""), reverse=True)
        
        # Paginación
        pagina_actual, rechazados_paginados, total_paginas, total = paginar_resultados(
            rechazados_ordenados, items_por_pagina=10, key_prefix="rechazados_pagina"
        )
        
        # Mostrar controles de paginación mejorados
        render_paginacion_mejorada(pagina_actual, total_paginas, total, "rechazados_pagina", items_por_pagina=10)
        
        # Mostrar resultados de la página actual
        for registro in rechazados_paginados:
            mostrar_registro(registro, es_rechazado=True, tab_prefix="rechazados")
    else:
        st.info("📭 No hay resultados rechazados para este mes.")

# Footer (adaptado automáticamente al tema del sistema)
st.divider()
st.markdown(
    """
    <div class="footer-text">
        🧠 Chatbot CL-AB v1.0 | Powered by Streamlit + LangChain + OpenAI
    </div>
    """,
    unsafe_allow_html=True
)

