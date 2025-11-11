"""
Módulo para manejar el feedback del usuario.
Gestiona la retroalimentación y actualiza los textos de referencia.
"""

from typing import Dict, List, Optional
from app.utils.io_manager import IOManager


class FeedbackManager:
    """Gestor de feedback del usuario."""
    
    def __init__(self, io_manager: IOManager):
        """
        Inicializa el gestor de feedback.
        
        Args:
            io_manager: Instancia de IOManager
        """
        self.io_manager = io_manager
    
    def registrar_feedback(
        self,
        resultado_id: str,
        aprobado: bool,
        comentario: Optional[str] = None,
        mes: Optional[str] = None
    ):
        """
        Registra el feedback del usuario.
        
        Args:
            resultado_id: ID del resultado
            aprobado: True si el usuario aprobó el texto
            comentario: Comentario opcional del usuario
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        """
        feedback = {
            "aprobado": aprobado,
            "comentario": comentario or "",
            "fecha": self.io_manager.generar_id()
        }
        
        self.io_manager.actualizar_feedback(resultado_id, feedback, mes)
        
        # Si no fue aprobado, mover a rechazados
        if not aprobado:
            self.io_manager.mover_a_rechazados(resultado_id, mes)
    
    def obtener_textos_aprobados(self, limite: int = 10) -> List[str]:
        """
        Obtiene textos aprobados para usar como referencia.
        
        Args:
            limite: Número máximo de textos a obtener
        
        Returns:
            Lista de textos aprobados
        """
        return self.io_manager.obtener_textos_aprobados(limite)
    
    def obtener_estadisticas(self, mes: Optional[str] = None) -> Dict:
        """
        Obtiene estadísticas de feedback del mes.
        
        Args:
            mes: Mes en formato YYYY-MM. Si es None, usa el mes actual.
        
        Returns:
            Dict con estadísticas
        """
        historial = self.io_manager.obtener_historial_mes(mes)
        
        total = len(historial)
        aprobados = sum(1 for r in historial if r.get("feedback", {}).get("aprobado") == True)
        rechazados = sum(1 for r in historial if r.get("feedback", {}).get("aprobado") == False)
        sin_feedback = total - aprobados - rechazados
        
        return {
            "total": total,
            "aprobados": aprobados,
            "rechazados": rechazados,
            "sin_feedback": sin_feedback,
            "tasa_aprobacion": (aprobados / total * 100) if total > 0 else 0
        }

