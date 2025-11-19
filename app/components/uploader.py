"""
Componente para subir archivos de referencia.
"""

import streamlit as st
import json
import html
import uuid
from typing import List, Optional
from app.components.help_modal import titulo_con_ayuda, AYUDA_ARCHIVOS_REFERENCIA


def render_file_uploader() -> List[str]:
    """
    Renderiza el componente para subir archivos de referencia.
    Guarda los archivos de forma persistente y muestra los archivos guardados.
    
    Returns:
        Lista de textos extraídos de los archivos (nuevos + guardados)
    """
    # Título con ayuda discreta al lado
    titulo_con_ayuda("📎 Archivos de Referencia", AYUDA_ARCHIVOS_REFERENCIA, "archivos_referencia", nivel="subheader")
    
    st.caption(
        "💡 Sube archivos .txt o .json con textos de referencia. Los archivos se guardan automáticamente."
    )
    
    # Los estilos del file uploader están definidos globalmente en styles.py
    # No necesitamos estilos adicionales aquí
    
    # Mostrar ejemplos de formato
    with st.expander("📋 Ver ejemplos de formato", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📄 Formato TXT:**")
            ejemplo_txt = """Este es un ejemplo de texto de referencia en formato TXT.
Puedes incluir cualquier texto que quieras usar como referencia para mejorar el estilo de las generaciones.

El sistema leerá todo el contenido del archivo como un único texto de referencia.
Puedes incluir múltiples párrafos, listas, o cualquier formato de texto plano."""
            
            st.code(ejemplo_txt, language="text")
            st.download_button(
                "📥 Descargar ejemplo TXT",
                data=ejemplo_txt,
                file_name="ejemplo_referencia.txt",
                mime="text/plain",
                key="descargar_ejemplo_txt",
                use_container_width=True
            )
        
        with col2:
            st.write("**📦 Formato JSON:**")
            ejemplo_json_dict = {
                "texto": "Este es un ejemplo de texto de referencia en formato JSON.",
                "descripcion": "El sistema buscará campos comunes como 'texto', 'content', 'body', 'mensaje' o 'descripcion'.",
                "content": "Si no encuentra estos campos, usará todo el contenido JSON como texto de referencia.",
                "notas": "Puedes estructurar el JSON como prefieras, pero asegúrate de incluir campos de texto legibles."
            }
            ejemplo_json = json.dumps(ejemplo_json_dict, ensure_ascii=False, indent=4)
            
            # Crear un contenedor con ID único para aplicar estilos específicos
            container_id = f"json-container-{uuid.uuid4().hex[:8]}"
            
            # Estilos específicos para este contenedor JSON
            st.markdown(f"""
            <style>
            #{container_id} {{
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
                overflow-x: auto !important;
                overflow-y: visible !important;
            }}
            
            #{container_id} div[data-testid="stCodeBlock"] {{
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
                overflow-x: auto !important;
                margin: 0 !important;
            }}
            
            #{container_id} div[data-testid="stCodeBlock"] pre {{
                white-space: pre !important;
                word-wrap: normal !important;
                overflow-wrap: normal !important;
                word-break: normal !important;
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
                overflow-x: auto !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            
            #{container_id} div[data-testid="stCodeBlock"] code {{
                white-space: pre !important;
                word-wrap: normal !important;
                overflow-wrap: normal !important;
                word-break: normal !important;
                display: block !important;
                width: 100% !important;
            }}
            </style>
            <div id="{container_id}">
            """, unsafe_allow_html=True)
            
            # Usar st.code() con el JSON completo
            st.code(ejemplo_json, language="json")
            
            # Cerrar el contenedor
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                "📥 Descargar ejemplo JSON",
                data=ejemplo_json,
                file_name="ejemplo_referencia.json",
                mime="application/json",
                key="descargar_ejemplo_json",
                use_container_width=True
            )
        
        st.caption("💡 **Tip:** Los archivos .txt se leen completos. Los .json se procesan buscando campos de texto comunes.")
    
    from app.utils.io_manager import IOManager
    io_manager = IOManager()
    
    # Inicializar session_state para archivos a eliminar
    if "archivos_a_eliminar" not in st.session_state:
        st.session_state.archivos_a_eliminar = []
    
    # Procesar eliminaciones pendientes
    if st.session_state.archivos_a_eliminar:
        archivos_eliminados = []
        archivos_error = []
        
        for archivo_a_eliminar in st.session_state.archivos_a_eliminar:
            try:
                from pathlib import Path
                archivo_path = Path(archivo_a_eliminar['ruta'])
                if archivo_path.exists() and archivo_path.is_file():
                    archivo_path.unlink()
                    archivos_eliminados.append(archivo_a_eliminar['nombre'])
                else:
                    archivos_error.append(f"{archivo_a_eliminar['nombre']} (no encontrado)")
            except Exception as e:
                archivos_error.append(f"{archivo_a_eliminar.get('nombre', 'archivo')} ({str(e)})")
        
        # Mostrar mensajes de resultado
        if archivos_eliminados:
            st.success(f"✅ Archivo(s) eliminado(s): {', '.join(archivos_eliminados)}")
        if archivos_error:
            st.error(f"❌ Error al eliminar: {', '.join(archivos_error)}")
        
        # Limpiar la lista de archivos a eliminar y recargar
        st.session_state.archivos_a_eliminar = []
        st.rerun()
    
    # Obtener lista de archivos ya guardados para evitar duplicados
    archivos_guardados_lista = io_manager.listar_archivos_referencia()
    nombres_guardados = {archivo['nombre'] for archivo in archivos_guardados_lista}
    
    # Subir nuevos archivos
    archivos_subidos = st.file_uploader(
        "Selecciona archivos de referencia:",
        type=["txt", "json"],
        accept_multiple_files=True,
        key="archivos_referencia"
    )
    
    # Procesar archivos nuevos subidos (solo los que no están guardados)
    archivos_nuevos = []
    if archivos_subidos:
        for archivo in archivos_subidos:
            try:
                contenido = archivo.read().decode('utf-8')
                
                # Determinar tipo de archivo
                tipo = archivo.name.split('.')[-1].lower()
                
                # Verificar si el archivo ya está guardado
                nombre_sanitizado = "".join(c for c in archivo.name if c.isalnum() or c in "._- ").replace(" ", "_")
                
                if nombre_sanitizado not in nombres_guardados:
                    # Guardar el archivo de forma persistente solo si es nuevo
                    guardado = io_manager.guardar_archivo_referencia(archivo.name, contenido)
                    if guardado:
                        st.success(f"✅ {archivo.name} guardado")
                        archivos_nuevos.append(archivo.name)
                    else:
                        st.warning(f"⚠️ {archivo.name}: Error al guardar")
                else:
                    st.caption(f"ℹ️ {archivo.name} ya está guardado")
            except Exception as e:
                st.error(f"❌ Error al procesar {archivo.name}: {str(e)}")
    
    # Cargar TODOS los archivos guardados (incluyendo los nuevos)
    textos_referencia = io_manager.cargar_archivos_referencia_guardados()
    
    # Mostrar archivos guardados en un expander para que sea menos invasivo
    archivos_guardados = io_manager.listar_archivos_referencia()
    
    if archivos_guardados:
        with st.expander(f"📁 Archivos Guardados ({len(archivos_guardados)})", expanded=False):
            for archivo_info in archivos_guardados:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"📄 **{archivo_info['nombre']}**")
                    st.caption(f"Tipo: {archivo_info['tipo'].upper()} | "
                              f"Tamaño: {archivo_info['tamaño']} caracteres | "
                              f"Modificado: {archivo_info['fecha_modificacion']}")
                
                with col2:
                    # Botón para descargar
                    contenido_archivo = archivo_info.get('contenido', '')
                    if contenido_archivo:
                        mime_type = "text/plain" if archivo_info['tipo'] == "txt" else "application/json"
                        st.download_button(
                            "💾 Descargar",
                            data=contenido_archivo,
                            file_name=archivo_info['nombre'],
                            mime=mime_type,
                            key=f"descargar_{archivo_info['nombre']}",
                            use_container_width=True
                        )
                
                with col3:
                    # Botón para recargar (forzar recarga completa de todos los archivos)
                    if st.button("🔄 Recargar", key=f"recargar_{archivo_info['nombre']}", use_container_width=True):
                        # Los archivos ya se cargan automáticamente, solo necesitamos refrescar
                        st.success(f"✅ Archivos recargados")
                        st.rerun()
                
                with col4:
                    # Botón para eliminar
                    eliminar_key = f"eliminar_archivo_{archivo_info['nombre']}"
                    if st.button("🗑️ Eliminar", key=eliminar_key, use_container_width=True, type="secondary"):
                        # Agregar a la lista de archivos a eliminar
                        if "archivos_a_eliminar" not in st.session_state:
                            st.session_state.archivos_a_eliminar = []
                        st.session_state.archivos_a_eliminar.append({
                            'nombre': archivo_info['nombre'],
                            'ruta': archivo_info['ruta']
                        })
                        st.rerun()
    
    # Mostrar total de forma más discreta
    if textos_referencia:
        st.caption(f"📚 {len(textos_referencia)} texto(s) de referencia activo(s)")
    
    return textos_referencia

