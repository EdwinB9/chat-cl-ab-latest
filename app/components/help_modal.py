"""
Componente para mostrar modales de ayuda contextual.
"""

import streamlit as st
from typing import Optional
import markdown


def mostrar_ayuda_modal(titulo: str, contenido: str, key: str):
    """
    Muestra un modal de ayuda usando st.dialog (Streamlit 1.29+).
    Si no está disponible, usa un expander como fallback.
    
    Args:
        titulo: Título del modal
        contenido: Contenido HTML/markdown del modal
        key: Clave única para el modal
    """
    # Intentar usar st.dialog si está disponible
    try:
        if hasattr(st, 'dialog'):
            if st.button("❓", key=f"help_btn_{key}", help=f"Ayuda: {titulo}"):
                st.session_state[f"show_help_{key}"] = True
            
            if st.session_state.get(f"show_help_{key}", False):
                with st.dialog(titulo):
                    st.markdown(contenido)
                    if st.button("Cerrar", key=f"close_{key}"):
                        st.session_state[f"show_help_{key}"] = False
                        st.rerun()
        else:
            # Fallback: usar expander
            with st.expander(f"❓ Ayuda: {titulo}", expanded=False):
                st.markdown(contenido)
    except:
        # Fallback: usar expander
        with st.expander(f"❓ Ayuda: {titulo}", expanded=False):
            st.markdown(contenido)


def titulo_con_ayuda(titulo_texto: str, contenido_ayuda: str, key: str, nivel: str = "subheader"):
    """
    Renderiza un título con un botón de ayuda discreto al lado.
    
    Args:
        titulo_texto: Texto del título
        contenido_ayuda: Contenido de ayuda a mostrar
        key: Clave única
        nivel: Nivel del título ("title", "header", "subheader")
    """
    help_key = f"show_help_{key}"
    
    # Inicializar estado (optimizado para Streamlit 1.28+)
    st.session_state.setdefault(help_key, False)
    
    # Para títulos grandes, usar título normal con botón que muestra ayuda destacada
    if nivel == "title":
        # Renderizar título normalmente
        st.title(titulo_texto)
        
        # Botón de ayuda simple
        col_btn1, col_btn2 = st.columns([1, 10])
        with col_btn1:
            if st.button("ℹ️", key=f"help_btn_{key}", help=f"Ayuda sobre {titulo_texto}", type="secondary", use_container_width=True):
                st.session_state[help_key] = not st.session_state[help_key]
                st.rerun()
        
        # Mostrar ayuda destacada si está activada
        if st.session_state.get(help_key, False):
            # Usar contenedor destacado con estilo personalizado (modo claro)
            bg_ayuda = "rgba(0, 172, 193, 0.15)"
            bg_ayuda_end = "rgba(0, 172, 193, 0.05)"
            border_ayuda = "#00acc1"
            texto_ayuda = "#1a237e"
            shadow_ayuda = "0 2px 8px rgba(0, 0, 0, 0.1)"
            
            # Convertir markdown a HTML e incluirlo directamente en el contenedor
            contenido_html = markdown.markdown(contenido_ayuda, extensions=['nl2br', 'fenced_code'])
            
            st.markdown(
                f"""
                <div class="help-container" style="
                    background: linear-gradient(135deg, {bg_ayuda} 0%, {bg_ayuda_end} 100%);
                    border-left: 4px solid {border_ayuda};
                    border-radius: 0.5rem;
                    padding: 1.25rem;
                    margin: 0.75rem 0;
                    box-shadow: {shadow_ayuda};
                    overflow: visible;
                    color: {texto_ayuda};
                ">
                    <h3 style="margin-top: 0; margin-bottom: 1rem; color: {border_ayuda}; display: flex; align-items: center; gap: 0.5rem;">
                        <span>ℹ️</span>
                        <span>Ayuda: {titulo_texto}</span>
                    </h3>
                    <div class="help-content-wrapper" style="color: {texto_ayuda}; line-height: 1.6;">
                        {contenido_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Botón para cerrar (clave única para título)
            if st.button("✅ Cerrar ayuda", key=f"close_title_{key}", use_container_width=True, type="primary"):
                st.session_state[help_key] = False
                st.rerun()
    else:
        # Para subheaders y headers, usar columnas estándar
        col_titulo, col_ayuda = st.columns([20, 1], gap="small")
        
        with col_titulo:
            if nivel == "header":
                st.header(titulo_texto)
            else:  # subheader por defecto
                st.subheader(titulo_texto)
        
        with col_ayuda:
            if st.button("ℹ️", key=f"help_btn_{key}", help="Ayuda", type="secondary", use_container_width=True):
                st.session_state[help_key] = not st.session_state[help_key]
                st.rerun()
        
        # Mostrar ayuda solo si está activada (para subheaders/headers)
        if st.session_state.get(help_key, False):
            # Contenedor de ayuda con estilos (modo claro)
            bg_ayuda = "rgba(0, 172, 193, 0.08)"
            border_ayuda = "#00acc1"
            texto_ayuda = "#1a237e"
            
            # Convertir markdown a HTML e incluirlo directamente en el contenedor
            contenido_html = markdown.markdown(contenido_ayuda, extensions=['nl2br', 'fenced_code'])
            
            st.markdown(
                f"""
                <div class="help-container" style="background: {bg_ayuda}; 
                            border-left: 4px solid {border_ayuda}; 
                            border-radius: 0.5rem; 
                            padding: 1rem; 
                            margin: 0.75rem 0;
                            overflow: visible;
                            word-wrap: break-word;
                            overflow-wrap: break-word;
                            color: {texto_ayuda};">
                    <div class="help-content-wrapper" style="color: {texto_ayuda}; line-height: 1.6;">
                        {contenido_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("Cerrar", key=f"close_sub_{key}", use_container_width=True):
                st.session_state[help_key] = False
                st.rerun()


def boton_ayuda(titulo: str, contenido: str, key: str, posicion: str = "icon"):
    """
    Función legacy - ahora usa titulo_con_ayuda internamente.
    Mantenida para compatibilidad pero se recomienda usar titulo_con_ayuda directamente.
    """
    # Para compatibilidad, simplemente mostrar el botón después del título
    help_key = f"show_help_{key}"
    
    # Inicializar estado (optimizado para Streamlit 1.28+)
    st.session_state.setdefault(help_key, False)
    
    if posicion == "icon":
        # Botón pequeño inline
        col1, col2 = st.columns([20, 1])
        with col2:
            if st.button("ℹ️", key=f"help_btn_{key}", help=titulo, type="secondary", use_container_width=True):
                st.session_state[help_key] = not st.session_state[help_key]
                st.rerun()
        
        if st.session_state.get(help_key, False):
            with st.expander(f"ℹ️ Ayuda: {titulo}", expanded=True):
                st.markdown(contenido)
                if st.button("Cerrar", key=f"close_{key}", use_container_width=True):
                    st.session_state[help_key] = False
                    st.rerun()
    else:
        if st.button(f"ℹ️ {titulo}", key=f"help_btn_{key}"):
            st.session_state[help_key] = not st.session_state[help_key]
            st.rerun()
        
        if st.session_state.get(help_key, False):
            with st.expander(f"ℹ️ Ayuda: {titulo}", expanded=True):
                st.markdown(contenido)
                if st.button("Cerrar", key=f"close_{key}", use_container_width=True):
                    st.session_state[help_key] = False
                    st.rerun()


# Contenidos de ayuda predefinidos
AYUDA_ARCHIVOS_REFERENCIA = """
**¿Qué son los archivos de referencia?**

Los archivos de referencia son textos que ayudan a la IA a entender el estilo y tono que deseas en tus generaciones.

**Formato TXT:**
- El sistema leerá todo el contenido del archivo como un único texto de referencia
- Puedes incluir múltiples párrafos, listas o cualquier formato de texto plano
- Ideal para textos largos o documentos completos

**Formato JSON:**
- El sistema buscará campos comunes como: `texto`, `content`, `body`, `mensaje`, `descripcion`
- Si no encuentra estos campos, usará todo el contenido JSON como texto
- Útil para estructurar información de manera organizada

**Consejos:**
- Sube textos que representen el estilo que quieres lograr
- Los textos aprobados también se usan como referencia automáticamente
- Puedes tener múltiples archivos activos simultáneamente
"""

AYUDA_GENERAR = """
**¿Cómo generar textos?**

1. **Tema o prompt:** Describe brevemente qué quieres generar
   - Ejemplo: "Día del Operario de Limpieza"
   - Sé específico para mejores resultados

2. **Instrucciones adicionales (opcional):** Agrega detalles sobre:
   - Tono deseado (formal, informal, amigable)
   - Elementos a incluir (valores de la empresa, fechas, etc.)
   - Estilo de escritura

3. **Configuración:**
   - **Temperatura:** Controla la creatividad (0.0 = más consistente, 1.0 = más creativo)
   - **Palabras máximas:** Límite de palabras para el texto generado

**Consejos:**
- Usa archivos de referencia para mejorar el estilo
- Aproba o rechaza resultados para entrenar el sistema
- Los textos aprobados se usan como referencia futura
"""

AYUDA_CORREGIR = """
**¿Cómo corregir textos?**

1. **Texto a corregir:** Pega el texto que deseas mejorar
   - Puede ser cualquier texto que necesites corregir
   - El sistema mejorará ortografía, gramática y fluidez

2. **Instrucciones de corrección (opcional):** Especifica qué mejorar:
   - "Mejorar la fluidez"
   - "Corregir errores ortográficos"
   - "Hacer más formal/informal"
   - "Mejorar la estructura"

**El sistema puede:**
- Corregir errores ortográficos y gramaticales
- Mejorar la fluidez y coherencia
- Ajustar el tono según tus instrucciones
- Mantener el significado original

**Consejos:**
- Sé específico en las instrucciones para mejores resultados
- Revisa siempre el resultado antes de aprobarlo
"""

AYUDA_RESUMIR = """
**¿Cómo resumir textos?**

1. **Texto a resumir:** Pega el texto que deseas resumir
   - Puede ser cualquier texto largo que necesites condensar
   - El sistema mantendrá los puntos principales

2. **Instrucciones de resumen (opcional):** Especifica el enfoque:
   - "Enfocarse en los puntos principales"
   - "Mantener el tono profesional"
   - "Incluir fechas y datos importantes"
   - "Resumir en formato de lista"

**El sistema puede:**
- Reducir el texto manteniendo información clave
- Conservar el tono y estilo original
- Adaptarse a la longitud máxima especificada
- Priorizar información según tus instrucciones

**Consejos:**
- Ajusta "Palabras máximas" según tus necesidades
- Usa instrucciones específicas para mejores resultados
"""

AYUDA_FEEDBACK = """
**¿Qué es el feedback?**

El feedback ayuda a mejorar las futuras generaciones del sistema.

**👍 Me gusta (Aprobar):**
- Marca el resultado como aprobado
- Se guarda en el historial de aprobados
- Se usa como referencia para futuras generaciones
- Mejora el estilo y calidad de los textos generados

**👎 No me gusta (Rechazar):**
- Marca el resultado como rechazado
- Se mueve al historial de rechazados
- Puedes agregar un comentario explicando por qué
- El sistema aprenderá de tus preferencias

**Comentarios:**
- Agrega comentarios para explicar tu feedback
- Útiles para entender qué mejorar
- Se guardan junto con el feedback

**Consejos:**
- Aproba textos que representen el estilo deseado
- Rechaza textos que no cumplan tus expectativas
- Los comentarios ayudan a entender tus preferencias
"""

AYUDA_CONFIGURACION = """
**Configuración del sistema**

**🔑 API Keys:**
Las API keys se configuran en el archivo `.env` en la raíz del proyecto. La aplicación solo muestra los proveedores que tengan una API key válida configurada.

**Proveedores disponibles:**

🟢 **Google Gemini (Gratuito - Recomendado)**
- Obtén tu API key: https://makersuite.google.com/app/apikey
- Modelo: `gemini-flash-latest`

🟢 **Groq (Gratuito - Muy Rápido)**
- Obtén tu API key: https://console.groq.com
- Varios modelos Llama y Mistral disponibles

🟢 **Together AI (Gratuito - Modelos Open Source)**
- Obtén tu API key: https://api.together.xyz
- Modelos Llama, Mistral, etc.

🟢 **Hugging Face (Gratuito)**
- Obtén tu token: https://huggingface.co/settings/tokens
- Amplia variedad de modelos

🟢 **Cohere (Gratuito para Desarrollo)**
- Obtén tu API key: https://dashboard.cohere.ai
- Modelo disponible: `command-nightly` únicamente

🔵 **OpenAI (Requiere Pago)**
- Obtén tu API key: https://platform.openai.com/api-keys
- Modelos: GPT-4o, GPT-4o-mini, GPT-3.5-turbo

**⚠️ Importante:**
- Las API keys deben configurarse en el archivo `.env`
- No compartas tus API keys públicamente
- Puedes usar solo las API keys que necesites (mínimo una)

**🤖 Proveedor de IA:**
- Selecciona entre los proveedores disponibles (solo se muestran si tienen API key configurada)
- Cada proveedor tiene diferentes modelos disponibles
- Elige según tus necesidades y presupuesto

**Modelo:**
- Diferentes modelos tienen diferentes capacidades y costos
- Modelos más potentes = mejor calidad pero mayor costo (en proveedores de pago)
- Los proveedores gratuitos tienen límites de uso

**Temperatura (Creatividad):**
- **0.0 - 0.3:** Muy consistente, predecible
- **0.4 - 0.7:** Balance entre consistencia y creatividad (recomendado)
- **0.8 - 1.0:** Muy creativo, menos predecible

**📏 Palabras máximas:**
- Límite de palabras para textos generados o resumidos
- Ajusta según tus necesidades
- Valores más altos = textos más largos pero mayor costo (en proveedores de pago)

**💡 Cómo configurar API Keys:**
1. Copia el archivo `example.env` a `.env` en la raíz del proyecto
2. Edita el archivo `.env` y agrega tus API keys
3. Reinicia la aplicación para que detecte las nuevas API keys
4. Los proveedores con API key válida aparecerán automáticamente en el selector
"""

AYUDA_HISTORIAL = """
**Historial del Mes**

El historial guarda todos los resultados generados durante el mes actual.

**Pestañas:**
- **📋 Todos:** Muestra todos los resultados (aprobados y rechazados)
- **✅ Aprobados:** Solo resultados marcados como "Me gusta"
- **❌ Rechazados:** Solo resultados marcados como "No me gusta"

**Funcionalidades:**
- **🗑️ Eliminar:** Elimina un resultado del historial
- **📄 Descargar TXT:** Descarga el texto del resultado
- **📦 Descargar JSON:** Descarga el resultado completo con metadatos

**Información mostrada:**
- Tema o prompt usado
- Número de palabras
- Modelo utilizado
- Estado de feedback (aprobado/rechazado)
- Comentarios asociados
- Fecha y hora de creación

**Consejos:**
- El historial se organiza por mes
- Los textos aprobados se usan como referencia automáticamente
- Puedes descargar resultados para uso externo
"""

