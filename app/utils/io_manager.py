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
        
        # Crear directorios si no existen
        self.resultados_dir.mkdir(parents=True, exist_ok=True)
        self.rechazados_dir.mkdir(parents=True, exist_ok=True)
    
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
        
        Args:
            resultado_id: ID del resultado
            feedback: Diccionario con el feedback
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        """
        datos = self.cargar_datos_mes(mes)
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                registro["feedback"] = feedback
                break
        
        archivo = self._get_archivo_mes(mes)
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    
    def mover_a_rechazados(self, resultado_id: str, mes: Optional[str] = None):
        """
        Mueve un resultado al directorio de rechazados.
        
        Args:
            resultado_id: ID del resultado
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        """
        datos = self.cargar_datos_mes(mes)
        resultado = None
        
        for registro in datos["datos"]:
            if registro["id"] == resultado_id:
                resultado = registro
                datos["datos"].remove(registro)
                break
        
        if resultado:
            # Guardar datos actualizados
            archivo = self._get_archivo_mes(mes)
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            
            # Guardar en rechazados
            archivo_rechazados = self.rechazados_dir / f"{mes or self._get_mes_actual()}.json"
            if archivo_rechazados.exists():
                with open(archivo_rechazados, 'r', encoding='utf-8') as f:
                    rechazados = json.load(f)
            else:
                rechazados = {"mes": mes or self._get_mes_actual(), "datos": []}
            
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
        
        Args:
            contenido: Contenido del archivo
            tipo: Tipo de archivo (txt o json)
        
        Returns:
            Lista de textos extraídos
        """
        textos = []
        
        if tipo == "txt":
            # Dividir por líneas vacías o párrafos
            paragrafos = [p.strip() for p in contenido.split("\n\n") if p.strip()]
            textos.extend(paragrafos)
        elif tipo == "json":
            try:
                data = json.loads(contenido)
                if isinstance(data, list):
                    textos = [str(item) for item in data]
                elif isinstance(data, dict):
                    # Intentar extraer textos de campos comunes
                    for key in ["texto", "contenido", "resultado", "textos"]:
                        if key in data:
                            if isinstance(data[key], list):
                                textos.extend([str(t) for t in data[key]])
                            else:
                                textos.append(str(data[key]))
            except:
                pass
        
        return textos
    
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
        Obtiene el historial de un mes.
        
        Args:
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Lista de registros del mes
        """
        datos = self.cargar_datos_mes(mes)
        return datos.get("datos", [])

