"""
Módulo para cargar y gestionar la configuración de la empresa.
"""

import json
from pathlib import Path
from typing import Dict, Optional, List


class EmpresaConfig:
    """Gestiona la configuración de la empresa desde un archivo JSON."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa el gestor de configuración de la empresa.
        
        Args:
            config_path: Ruta al archivo de configuración. Si es None, busca en config/empresa_config.json
        """
        if config_path is None:
            # Buscar el archivo de configuración relativo al proyecto
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "empresa_config.json"
        
        self.config_path = Path(config_path)
        self.config: Dict = {}
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Carga la configuración desde el archivo JSON.
        
        Returns:
            True si se cargó correctamente, False en caso contrario
        """
        try:
            if not self.config_path.exists():
                print(f"⚠️ Advertencia: No se encontró el archivo de configuración en {self.config_path}")
                print(f"💡 Creando archivo de configuración por defecto...")
                self._create_default_config()
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear el archivo JSON: {e}")
            return False
        except Exception as e:
            print(f"❌ Error al cargar la configuración: {e}")
            return False
    
    def _create_default_config(self):
        """Crea un archivo de configuración por defecto si no existe."""
        default_config = {
            "nombre_empresa": "Mi Empresa",
            "sector": "Servicios",
            "descripcion": "Descripción de la empresa",
            "mision": "Misión de la empresa",
            "vision": "Visión de la empresa",
            "valores": ["Valor 1", "Valor 2"],
            "tono_comunicacion": {
                "estilo": "Profesional",
                "caracteristicas": ["Claro", "Directo"]
            },
            "contexto_adicional": {
                "servicios_principales": [],
                "puntos_destacados": [],
                "enfoque": ""
            },
            "palabras_clave": [],
            "mensajes_frecuentes": []
        }
        
        # Crear directorio si no existe
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        self.config = default_config
    
    def get_nombre_empresa(self) -> str:
        """Retorna el nombre de la empresa."""
        return self.config.get("nombre_empresa", "")
    
    def get_descripcion(self) -> str:
        """Retorna la descripción de la empresa."""
        return self.config.get("descripcion", "")
    
    def get_mision(self) -> str:
        """Retorna la misión de la empresa."""
        return self.config.get("mision", "")
    
    def get_vision(self) -> str:
        """Retorna la visión de la empresa."""
        return self.config.get("vision", "")
    
    def get_valores(self) -> List[str]:
        """Retorna la lista de valores de la empresa."""
        return self.config.get("valores", [])
    
    def get_valores_texto(self) -> str:
        """Retorna los valores como texto formateado."""
        valores = self.get_valores()
        if not valores:
            return ""
        return "\n".join([f"- {valor}" for valor in valores])
    
    def get_tono_comunicacion(self) -> Dict:
        """Retorna la configuración del tono de comunicación."""
        return self.config.get("tono_comunicacion", {})
    
    def get_contexto_adicional(self) -> Dict:
        """Retorna el contexto adicional de la empresa."""
        return self.config.get("contexto_adicional", {})
    
    def get_palabras_clave(self) -> List[str]:
        """Retorna las palabras clave de la empresa."""
        return self.config.get("palabras_clave", [])
    
    def get_mensajes_frecuentes(self) -> List[str]:
        """Retorna los mensajes frecuentes de la empresa."""
        return self.config.get("mensajes_frecuentes", [])
    
    def get_contexto_completo(self) -> str:
        """
        Genera un contexto completo formateado para usar en prompts.
        
        Returns:
            String con toda la información de la empresa formateada
        """
        partes = []
        
        # Información básica
        descripcion = self.get_descripcion()
        if descripcion:
            partes.append(f"CONTEXTO: {descripcion}")
        
        # Misión y Visión
        mision = self.get_mision()
        vision = self.get_vision()
        if mision:
            partes.append(f"\nMISIÓN: {mision}")
        if vision:
            partes.append(f"VISIÓN: {vision}")
        
        # Valores
        valores_texto = self.get_valores_texto()
        if valores_texto:
            partes.append(f"\nVALORES DE LA EMPRESA:\n{valores_texto}")
        
        # Tono de comunicación
        tono = self.get_tono_comunicacion()
        if tono:
            estilo = tono.get("estilo", "")
            caracteristicas = tono.get("caracteristicas", [])
            if estilo:
                partes.append(f"\nTONO DE COMUNICACIÓN: {estilo}")
            if caracteristicas:
                partes.append("Características del tono:")
                for car in caracteristicas:
                    partes.append(f"  - {car}")
        
        # Contexto adicional
        contexto = self.get_contexto_adicional()
        if contexto:
            servicios = contexto.get("servicios_principales", [])
            puntos = contexto.get("puntos_destacados", [])
            enfoque = contexto.get("enfoque", "")
            
            if servicios:
                partes.append(f"\nSERVICIOS PRINCIPALES:")
                for servicio in servicios:
                    partes.append(f"  - {servicio}")
            
            if puntos:
                partes.append(f"\nPUNTOS DESTACADOS:")
                for punto in puntos:
                    partes.append(f"  - {punto}")
            
            if enfoque:
                partes.append(f"\nENFOQUE: {enfoque}")
        
        # Mensajes frecuentes
        mensajes = self.get_mensajes_frecuentes()
        if mensajes:
            partes.append(f"\nMENSAJES FRECUENTES:")
            for mensaje in mensajes:
                partes.append(f"  - {mensaje}")
        
        return "\n".join(partes)
    
    def reload(self) -> bool:
        """Recarga la configuración desde el archivo."""
        return self.load_config()


# Instancia global para uso en toda la aplicación
_empresa_config_instance: Optional[EmpresaConfig] = None


def get_empresa_config(config_path: Optional[str] = None) -> EmpresaConfig:
    """
    Obtiene la instancia global de configuración de la empresa.
    
    Args:
        config_path: Ruta opcional al archivo de configuración
        
    Returns:
        Instancia de EmpresaConfig
    """
    global _empresa_config_instance
    if _empresa_config_instance is None:
        _empresa_config_instance = EmpresaConfig(config_path)
    return _empresa_config_instance

