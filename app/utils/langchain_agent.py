"""
Módulo para manejar las operaciones con LangChain.
Soporta OpenAI y Google Gemini como proveedores de IA.
"""

import os
from typing import Optional, Dict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

# Importar OpenAI
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Importar Google Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Intentar importar callback para OpenAI
try:
    from langchain_community.callbacks import get_openai_callback
except ImportError:
    try:
        from langchain.callbacks import get_openai_callback
    except ImportError:
        # Si no está disponible, crear un stub
        class get_openai_callback:
            def __init__(self):
                self.total_tokens = 0
                self.total_cost = 0.0
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass


class LangChainAgent:
    """Agente LangChain para operaciones de texto con soporte multi-proveedor."""
    
    # Modelos disponibles por proveedor
    OPENAI_MODELS = {
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4o": "gpt-4o",
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-3.5-turbo": "gpt-3.5-turbo"
    }
    
    GEMINI_MODELS = {
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash",
        "gemini-pro": "gemini-pro"
    }
    
    def __init__(
        self, 
        provider: str = "openai",
        model_name: str = "gpt-4o-mini", 
        temperature: float = 0.7
    ):
        """
        Inicializa el agente LangChain.
        
        Args:
            provider: Proveedor de IA ("openai" o "gemini")
            model_name: Nombre del modelo a usar
            temperature: Temperatura para la generación (0.0 a 1.0)
        """
        self.provider = provider.lower()
        self.model_name = model_name
        self.temperature = temperature
        self.reference_texts: List[str] = []
        
        # Validar proveedor
        if self.provider not in ["openai", "gemini"]:
            raise ValueError(f"Proveedor '{provider}' no soportado. Use 'openai' o 'gemini'.")
        
        # Inicializar LLM según el proveedor
        if self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("langchain-openai no está instalado. Instálelo con: pip install langchain-openai")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY no está configurada. Por favor, configura tu API key.")
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                openai_api_key=api_key
            )
        elif self.provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise ImportError("langchain-google-genai no está instalado. Instálelo con: pip install langchain-google-genai")
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY no está configurada. Por favor, configura tu API key.")
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                google_api_key=api_key
            )
    
    def set_reference_texts(self, texts: List[str]):
        """Establece textos de referencia para mejorar el estilo."""
        self.reference_texts = texts
    
    def _get_style_context(self) -> str:
        """Genera contexto de estilo a partir de textos de referencia."""
        if not self.reference_texts:
            return ""
        
        context = "\n\n--- Textos de Referencia (estilo deseado) ---\n"
        for i, text in enumerate(self.reference_texts[:3], 1):  # Máximo 3 textos
            context += f"\nEjemplo {i}:\n{text}\n"
        return context
    
    def _invoke_llm(self, messages: List, use_callback: bool = True) -> Dict[str, any]:
        """
        Invoca el LLM con los mensajes proporcionados.
        
        Args:
            messages: Lista de mensajes para el LLM
            use_callback: Si usar callback para tracking (solo OpenAI)
        
        Returns:
            Dict con el texto generado y metadata
        """
        try:
            if self.provider == "openai" and use_callback:
                with get_openai_callback() as cb:
                    response = self.llm.invoke(messages)
                    texto = response.content
                    return {
                        "texto": texto,
                        "tokens_usados": cb.total_tokens if cb else 0,
                        "costo": cb.total_cost if cb else 0.0
                    }
            else:
                # Gemini o OpenAI sin callback
                response = self.llm.invoke(messages)
                texto = response.content
                return {
                    "texto": texto,
                    "tokens_usados": 0,  # Gemini no tiene callback fácil
                    "costo": 0.0
                }
        except Exception as e:
            return {
                "texto": f"Error al procesar: {str(e)}",
                "tokens_usados": 0,
                "costo": 0.0
            }
    
    def generar_texto(
        self, 
        tema: str, 
        max_palabras: int = 200,
        instrucciones_adicionales: str = ""
    ) -> Dict[str, any]:
        """
        Genera un nuevo texto a partir de un tema.
        
        Args:
            tema: Tema o prompt para generar el texto
            max_palabras: Número máximo de palabras
            instrucciones_adicionales: Instrucciones adicionales opcionales
            
        Returns:
            Dict con el texto generado y metadata
        """
        style_context = self._get_style_context()
        
        prompt = f"""Eres un asistente experto en comunicación empresarial. 
Tu tarea es generar un texto profesional, claro y coherente sobre el siguiente tema:

TEMA: {tema}

REQUISITOS:
- El texto debe tener aproximadamente {max_palabras} palabras
- Debe ser profesional pero cercano
- Debe mantener un tono empresarial apropiado
- Estructura clara con párrafos bien organizados
{instrucciones_adicionales if instrucciones_adicionales else ''}

{style_context}

Por favor, genera el texto completo:"""
        
        messages = [
            SystemMessage(content="Eres un experto en comunicación empresarial y redacción profesional."),
            HumanMessage(content=prompt)
        ]
        
        return self._invoke_llm(messages)
    
    def corregir_texto(
        self, 
        texto: str,
        instrucciones_adicionales: str = ""
    ) -> Dict[str, any]:
        """
        Corrige y mejora un texto existente.
        
        Args:
            texto: Texto a corregir
            instrucciones_adicionales: Instrucciones específicas de corrección
            
        Returns:
            Dict con el texto corregido y metadata
        """
        style_context = self._get_style_context()
        
        prompt = f"""Eres un editor experto en comunicación empresarial.
Tu tarea es corregir y mejorar el siguiente texto, mejorando:
- Ortografía y gramática
- Claridad y fluidez
- Estilo profesional
- Estructura y organización
- Coherencia

TEXTO ORIGINAL:
{texto}

{instrucciones_adicionales if instrucciones_adicionales else ''}

{style_context}

Por favor, proporciona el texto corregido y mejorado:"""
        
        messages = [
            SystemMessage(content="Eres un editor experto en comunicación empresarial y redacción profesional."),
            HumanMessage(content=prompt)
        ]
        
        return self._invoke_llm(messages)
    
    def resumir_texto(
        self, 
        texto: str,
        max_palabras: int = 100,
        instrucciones_adicionales: str = ""
    ) -> Dict[str, any]:
        """
        Resume un texto manteniendo las ideas principales.
        
        Args:
            texto: Texto a resumir
            max_palabras: Número máximo de palabras para el resumen
            instrucciones_adicionales: Instrucciones específicas de resumen
            
        Returns:
            Dict con el texto resumido y metadata
        """
        prompt = f"""Eres un experto en comunicación empresarial.
Tu tarea es crear un resumen conciso y profesional del siguiente texto:

TEXTO ORIGINAL:
{texto}

REQUISITOS:
- El resumen debe tener aproximadamente {max_palabras} palabras
- Debe mantener las ideas principales y el mensaje clave
- Debe ser claro y profesional
- Mantener el tono original
{instrucciones_adicionales if instrucciones_adicionales else ''}

Por favor, proporciona el resumen:"""
        
        messages = [
            SystemMessage(content="Eres un experto en comunicación empresarial y creación de resúmenes profesionales."),
            HumanMessage(content=prompt)
        ]
        
        return self._invoke_llm(messages)
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """Retorna la lista de proveedores disponibles."""
        providers = []
        if OPENAI_AVAILABLE:
            providers.append("openai")
        if GEMINI_AVAILABLE:
            providers.append("gemini")
        return providers
    
    @staticmethod
    def get_available_models(provider: str) -> Dict[str, str]:
        """Retorna los modelos disponibles para un proveedor."""
        provider = provider.lower()
        if provider == "openai":
            return LangChainAgent.OPENAI_MODELS
        elif provider == "gemini":
            return LangChainAgent.GEMINI_MODELS
        else:
            return {}
