"""
Módulo para manejar la entrada y salida de archivos.
Gestiona el almacenamiento en JSON mensuales y la carga de textos de referencia.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class IOManager:
    """Gestor de entrada/salida de archivos."""
    
    def __init__(self, base_dir: str = "data"):
        """
        Inicializa el gestor de IO.
        
        Args:
            base_dir: Directorio base para almacenar datos
        """
        self.base_dir = Path(base_dir)
        self.resultados_dir = self.base_dir / "resultados"
        self.rechazados_dir = self.base_dir / "rechazados"
        self.archivos_referencia_dir = self.base_dir / "archivos_referencia"
        
        # Crear directorios si no existen
        self.resultados_dir.mkdir(parents=True, exist_ok=True)
        self.rechazados_dir.mkdir(parents=True, exist_ok=True)
        self.archivos_referencia_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_mes_actual(self) -> str:
        """Obtiene el mes actual en formato YYYY-MM."""
        return datetime.now().strftime("%Y-%m")
    
    def _get_archivo_mes(self, mes: Optional[str] = None) -> Path:
        """
        Obtiene la ruta del archivo JSON del mes.
        
        Args:
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Path al archivo JSON
        """
        if mes is None:
            mes = self._get_mes_actual()
        return self.resultados_dir / f"{mes}.json"
    
    def _generar_id(self) -> str:
        """Genera un ID único basado en timestamp."""
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    
    def generar_id(self) -> str:
        """Genera un ID único basado en timestamp (método público)."""
        return self._generar_id()
    
    def cargar_datos_mes(self, mes: Optional[str] = None) -> Dict:
        """
        Carga los datos del mes desde el archivo JSON.
        
        Args:
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Dict con los datos del mes
        """
        archivo = self._get_archivo_mes(mes)
        
        if not archivo.exists():
            return {
                "mes": mes or self._get_mes_actual(),
                "datos": []
            }
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {
                "mes": mes or self._get_mes_actual(),
                "datos": []
            }
    
    def guardar_resultado(
        self,
        accion: str,
        tema: str,
        resultado: str,
        palabras: int,
        modelo: str,
        config: Dict,
        feedback: Optional[Dict] = None
    ) -> str:
        """
        Guarda un resultado en el archivo JSON del mes.
        
        Args:
            accion: Acción realizada (generar, corregir, resumir)
            tema: Tema o texto original
            resultado: Texto resultante
            palabras: Número de palabras
            modelo: Modelo usado
            config: Configuración usada
            feedback: Feedback del usuario (opcional)
        
        Returns:
            ID del resultado guardado
        """
        datos = self.cargar_datos_mes()
        resultado_id = self.generar_id()
        
        nuevo_registro = {
            "id": resultado_id,
            "accion": accion,
            "tema": tema,
            "resultado": resultado,
            "palabras": palabras,
            "modelo": modelo,
            "config": config,
            "feedback": feedback or {}
        }
        
        datos["datos"].append(nuevo_registro)
        
        archivo = self._get_archivo_mes()
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        
        return resultado_id
    
    def actualizar_feedback(self, resultado_id: str, feedback: Dict, mes: Optional[str] = None):
        """
        Actualiza el feedback de un resultado existente.
        Busca tanto en resultados como en rechazados.
        Si se aprueba un resultado rechazado, lo mueve de vuelta a resultados.
        
        Args:
            resultado_id: ID del resultado
            feedback: Diccionario con el feedback
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        """
        if mes is None:
            mes = self._get_mes_actual()
        
        # Primero buscar en resultados
        datos = self.cargar_datos_mes(mes)
        encontrado_en_resultados = False
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                registro["feedback"] = feedback
                encontrado_en_resultados = True
                break
        
        # Si no se encuentra en resultados, buscar en rechazados
        if not encontrado_en_resultados:
            archivo_rechazados = self.rechazados_dir / f"{mes}.json"
            if archivo_rechazados.exists():
                try:
                    with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                        rechazados = json.load(f)
                    
                    resultado_encontrado = None
                    for registro in rechazados.get("datos", []):
                        if registro["id"] == resultado_id:
                            resultado_encontrado = registro
                            resultado_encontrado["feedback"] = feedback
                            break
                    
                    # Si se aprueba un resultado rechazado, moverlo de vuelta a resultados
                    if resultado_encontrado and feedback.get("aprobado") is True:
                        # Agregar a resultados
                        datos["datos"].append(resultado_encontrado)
                        # Remover de rechazados
                        rechazados["datos"].remove(resultado_encontrado)
                        # Guardar ambos archivos
                        archivo = self._get_archivo_mes(mes)
                        with open(archivo, 'w', encoding='utf-8') as f:
                            json.dump(datos, f, ensure_ascii=False, indent=2)
                        with open(archivo_rechazados, 'w', encoding='utf-8') as f:
                            json.dump(rechazados, f, ensure_ascii=False, indent=2)
                        return
                    elif resultado_encontrado:
                        # Solo actualizar feedback en rechazados
                        with open(archivo_rechazados, 'w', encoding='utf-8') as f:
                            json.dump(rechazados, f, ensure_ascii=False, indent=2)
                        return
                except Exception as e:
                    pass
        
        # Guardar resultados si se encontró ahí
        if encontrado_en_resultados:
            archivo = self._get_archivo_mes(mes)
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
    
    def mover_a_rechazados(self, resultado_id: str, mes: Optional[str] = None):
        """
        Mueve un resultado al directorio de rechazados.
        Solo mueve si no está ya en rechazados.
        
        Args:
            resultado_id: ID del resultado
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        """
        if mes is None:
            mes = self._get_mes_actual()
        
        # Verificar si ya está en rechazados
        archivo_rechazados = self.rechazados_dir / f"{mes}.json"
        if archivo_rechazados.exists():
            try:
                with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                    rechazados = json.load(f)
                # Verificar si ya existe
                for registro in rechazados.get("datos", []):
                    if registro["id"] == resultado_id:
                        # Ya está en rechazados, no hacer nada
                        return
            except:
                pass
        
        # Buscar en resultados
        datos = self.cargar_datos_mes(mes)
        resultado = None
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                resultado = registro
                datos["datos"].remove(registro)
                break
        
        if resultado:
            # Guardar datos actualizados (sin el resultado movido)
            archivo = self._get_archivo_mes(mes)
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            # Guardar en rechazados
            if archivo_rechazados.exists():
                with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                    rechazados = json.load(f)
            else:
                rechazados = {"mes": mes, "datos": []}
            
            # Verificar que no esté duplicado antes de agregar
            ya_existe = any(r["id"] == resultado_id for r in rechazados.get("datos", []))
            if not ya_existe:
                rechazados["datos"].append(resultado)
                with open(archivo_rechazados, 'w', encoding='utf-8') as f:
                    json.dump(rechazados, f, ensure_ascii=False, indent=2)
    
    def obtener_textos_aprobados(self, limite: int = 10) -> List[str]:
        """
        Obtiene textos aprobados para usar como referencia.
        
        Args:
            limite: Número máximo de textos a obtener
        
        Returns:
            Lista de textos aprobados
        """
        textos = []
        datos = self.cargar_datos_mes()
        
        for registro in datos["datos"]:
            if registro.get("feedback", {}).get("aprobado") == True:
                textos.append(registro["resultado"])
                if len(textos) >= limite:
                    break
        
        return textos
    
    def cargar_archivo_referencia(self, contenido: str, tipo: str = "txt") -> List[str]:
        """
        Carga textos de referencia desde un archivo.
        Cada archivo se trata como un solo texto (no se divide por párrafos).
        
        Args:
            contenido: Contenido del archivo
            tipo: Tipo de archivo (txt o json)
        
        Returns:
            Lista con un solo texto (el contenido completo del archivo)
        """
        textos = []
        
        if tipo == "txt":
            # Tratar el archivo completo como un solo texto
            texto_limpio = contenido.strip()
            if texto_limpio:
                textos.append(texto_limpio)
        elif tipo == "json":
            try:
                data = json.loads(contenido)
                if isinstance(data, list):
                    # Si es una lista, convertir a string
                    textos.append(json.dumps(data, ensure_ascii=False, indent=2))
                elif isinstance(data, dict):
                    # Intentar extraer textos de campos comunes
                    texto_encontrado = False
                    for key in ["texto", "contenido", "resultado", "textos"]:
                        if key in data:
                            if isinstance(data[key], list):
                                textos.append("\n".join([str(t) for t in data[key]]))
                            else:
                                textos.append(str(data[key]))
                            texto_encontrado = True
                            break
                    # Si no se encontró un campo específico, usar todo el JSON
                    if not texto_encontrado:
                        textos.append(json.dumps(data, ensure_ascii=False, indent=2))
            except:
                # Si no es JSON válido, tratarlo como texto plano
                if contenido.strip():
                    textos.append(contenido.strip())
        
        return textos
    
    def guardar_archivo_referencia(self, nombre_archivo: str, contenido: str) -> bool:
        """
        Guarda un archivo de referencia de forma persistente.
        
        Args:
            nombre_archivo: Nombre del archivo
            contenido: Contenido del archivo
        
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            # Sanitizar el nombre del archivo
            nombre_sanitizado = "".join(c for c in nombre_archivo if c.isalnum() or c in "._- ")
            nombre_sanitizado = nombre_sanitizado.replace(" ", "_")
            
            archivo_path = self.archivos_referencia_dir / nombre_sanitizado
            
            # Guardar el archivo
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            return True
        except Exception as e:
            return False
    
    def listar_archivos_referencia(self) -> List[Dict[str, str]]:
        """
        Lista todos los archivos de referencia guardados.
        
        Returns:
            Lista de diccionarios con información de los archivos
        """
        archivos = []
        
        if not self.archivos_referencia_dir.exists():
            return archivos
        
        for archivo_path in self.archivos_referencia_dir.iterdir():
            if archivo_path.is_file():
                try:
                    # Leer el contenido para obtener estadísticas
                    with open(archivo_path, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    
                    tipo = archivo_path.suffix.lower().replace('.', '')
                    
                    archivos.append({
                        "nombre": archivo_path.name,
                        "ruta": str(archivo_path),
                        "tipo": tipo,
                        "tamaño": len(contenido),
                        "textos_extraidos": 1,  # Cada archivo cuenta como 1 texto
                        "contenido": contenido,  # Guardar contenido para descarga
                        "fecha_modificacion": datetime.fromtimestamp(archivo_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
                except:
                    pass
        
        # Ordenar por fecha de modificación (más recientes primero)
        archivos.sort(key=lambda x: x["fecha_modificacion"], reverse=True)
        return archivos
    
    def cargar_archivos_referencia_guardados(self) -> List[str]:
        """
        Carga todos los textos de referencia de los archivos guardados.
        
        Returns:
            Lista de textos extraídos de todos los archivos guardados
        """
        textos_totales = []
        archivos = self.listar_archivos_referencia()
        
        for archivo_info in archivos:
            try:
                with open(archivo_info["ruta"], 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                textos = self.cargar_archivo_referencia(contenido, archivo_info["tipo"])
                textos_totales.extend(textos)
            except:
                pass
        
        return textos_totales
    
    def eliminar_archivo_referencia(self, nombre_archivo: str) -> bool:
        """
        Elimina un archivo de referencia guardado.
        
        Args:
            nombre_archivo: Nombre del archivo a eliminar
        
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            archivo_path = self.archivos_referencia_dir / nombre_archivo
            if archivo_path.exists() and archivo_path.is_file():
                archivo_path.unlink()
                return True
            return False
        except:
            return False
    
    def exportar_resultado(self, resultado_id: str, formato: str = "txt", mes: Optional[str] = None) -> Optional[str]:
        """
        Exporta un resultado a un formato específico.
        
        Args:
            resultado_id: ID del resultado
            formato: Formato de exportación (txt o json)
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Contenido del archivo a exportar
        """
        datos = self.cargar_datos_mes(mes)
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                if formato == "txt":
                    return registro["resultado"]
                elif formato == "json":
                    return json.dumps(registro, ensure_ascii=False, indent=2)
        
        return None
    
    def obtener_historial_mes(self, mes: Optional[str] = None) -> List[Dict]:
        """
        Obtiene el historial de un mes (solo resultados aprobados).
        
        Args:
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Lista de registros del mes
        """
        datos = self.cargar_datos_mes(mes)
        return datos.get("datos", [])
    
    def obtener_historial_rechazados(self, mes: Optional[str] = None) -> List[Dict]:
        """
        Obtiene el historial de rechazados de un mes.
        
        Args:
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Lista de registros rechazados del mes
        """
        if mes is None:
            mes = self._get_mes_actual()
        
        archivo_rechazados = self.rechazados_dir / f"{mes}.json"
        
        if not archivo_rechazados.exists():
            return []
        
        try:
            with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                rechazados = json.load(f)
            return rechazados.get("datos", [])
        except:
            return []
    
    def obtener_historial_completo(self, mes: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Obtiene el historial completo (aprobados, rechazados y todos) de un mes.
        Filtra correctamente los resultados según su feedback.
        
        Args:
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Dict con 'aprobados', 'rechazados' y 'todos'
        """
        # Obtener todos los resultados del mes (incluye aprobados y sin feedback)
        todos_resultados = self.obtener_historial_mes(mes)
        # Obtener rechazados
        rechazados = self.obtener_historial_rechazados(mes)
        
        # Filtrar aprobados: solo los que tienen feedback.aprobado == True
        aprobados = [
            registro for registro in todos_resultados
            if registro.get("feedback", {}).get("aprobado") is True
        ]
        
        # Combinar todos los resultados: aprobados + rechazados + sin feedback
        # Crear un set de IDs de rechazados para evitar duplicados
        ids_rechazados = {r.get("id") for r in rechazados}
        ids_aprobados = {r.get("id") for r in aprobados}
        
        # Todos incluye: aprobados + rechazados + resultados sin feedback
        todos = aprobados + rechazados + [
            registro for registro in todos_resultados
            if registro.get("id") not in ids_rechazados and registro.get("id") not in ids_aprobados
        ]
        
        return {
            "aprobados": aprobados,
            "rechazados": rechazados,
            "todos": todos
        }
    
    def eliminar_resultado(self, resultado_id: str, mes: Optional[str] = None) -> bool:
        """
        Elimina un resultado del historial (busca tanto en aprobados como rechazados).
        
        Args:
            resultado_id: ID del resultado a eliminar
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            True si se eliminó, False si no se encontró
        """
        if mes is None:
            mes = self._get_mes_actual()
        
        # Intentar eliminar de resultados aprobados
        datos = self.cargar_datos_mes(mes)
        eliminado = False
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                datos["datos"].remove(registro)
                eliminado = True
                break
        
        if eliminado:
            archivo = self._get_archivo_mes(mes)
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        
        # Si no se encontró en aprobados, buscar en rechazados
        archivo_rechazados = self.rechazados_dir / f"{mes}.json"
        if archivo_rechazados.exists():
            try:
                with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                    rechazados = json.load(f)
                
                for registro in rechazados.get("datos", []):
                    if registro["id"] == resultado_id:
                        rechazados["datos"].remove(registro)
                        eliminado = True
                        break
                
                if eliminado:
                    with open(archivo_rechazados, 'w', encoding='utf-8') as f:
                        json.dump(rechazados, f, ensure_ascii=False, indent=2)
                    return True
            except:
                pass
        
        return False
    
    def obtener_feedback_resultado(self, resultado_id: str, mes: Optional[str] = None) -> Optional[Dict]:
        """
        Obtiene el feedback de un resultado específico.
        Busca tanto en resultados como en rechazados.
        
        Args:
            resultado_id: ID del resultado
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Dict con el feedback o None si no existe
        """
        # Buscar primero en resultados
        datos = self.cargar_datos_mes(mes)
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                feedback = registro.get("feedback", {})
                # Retornar None si el feedback está vacío
                if feedback and feedback.get("aprobado") is not None:
                    return feedback
                return None
        
        # Si no se encuentra en resultados, buscar en rechazados
        if mes is None:
            mes = self._get_mes_actual()
        archivo_rechazados = self.rechazados_dir / f"{mes}.json"
        
        if archivo_rechazados.exists():
            try:
                with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                    rechazados = json.load(f)
                
                for registro in rechazados.get("datos", []):
                    if registro["id"] == resultado_id:
                        feedback = registro.get("feedback", {})
                        if feedback and feedback.get("aprobado") is not None:
                            return feedback
            except:
                pass
        
        return None
    
    def obtener_resultado_por_id(self, resultado_id: str, mes: Optional[str] = None) -> Optional[Dict]:
        """
        Obtiene un resultado completo por su ID.
        Busca tanto en resultados como en rechazados.
        
        Args:
            resultado_id: ID del resultado
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Dict con el resultado completo o None si no existe
        """
        if mes is None:
            mes = self._get_mes_actual()
        
        # Buscar primero en resultados
        datos = self.cargar_datos_mes(mes)
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                return registro
        
        # Si no se encuentra en resultados, buscar en rechazados
        archivo_rechazados = self.rechazados_dir / f"{mes}.json"
        if archivo_rechazados.exists():
            try:
                with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                    rechazados = json.load(f)
                
                for registro in rechazados.get("datos", []):
                    if registro["id"] == resultado_id:
                        return registro
            except:
                pass
        
        return None

