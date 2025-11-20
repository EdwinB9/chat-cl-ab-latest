"""
Módulo para manejar las operaciones con LangChain.
Soporta OpenAI y Google Gemini como proveedores de IA.
"""

import os
from typing import Optional, Dict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from app.utils.empresa_config import get_empresa_config

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

# Intentar importar google-generativeai para listar modelos
try:
    import google.generativeai as genai
    GEMINI_GENAI_AVAILABLE = True
except ImportError:
    GEMINI_GENAI_AVAILABLE = False

# Intentar importar requests para API REST directa
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

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
    """
    Agente LangChain para operaciones de texto con soporte multi-proveedor.
    
    Notas sobre modelos soportados:
    - ChatOpenAI (OpenAI): Acepta cualquier modelo válido de OpenAI API.
      Los modelos disponibles dependen de tu cuenta y plan de OpenAI.
      Modelos comunes: gpt-4o, gpt-4o-mini, gpt-3.5-turbo, gpt-4, etc.
    
    - ChatGoogleGenerativeAI (Gemini): Acepta cualquier modelo válido de Gemini API.
      Los modelos disponibles dependen de tu API key y acceso a Google Cloud.
      Modelos gratuitos: gemini-1.5-flash, gemini-1.5-pro, gemini-pro
    """
    
    # Modelos disponibles por proveedor (solo modelos actuales y accesibles)
    # Nota: LangChain acepta cualquier modelo válido, estos son los recomendados
    OPENAI_MODELS = {
        "gpt-4o-mini": "gpt-4o-mini",      # Recomendado: económico y rápido
        "gpt-4o": "gpt-4o",                # Más potente
        "gpt-3.5-turbo": "gpt-3.5-turbo"   # Modelo estándar
    }
    
    # Modelos Gemini - Solo gemini-flash-latest según solicitud
    # Documentación: https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai
    GEMINI_MODELS = {
        "gemini-flash-latest": "gemini-flash-latest"  # Único modelo configurado
    }
    
    def __init__(
        self, 
        provider: str = "openai",
        model_name: str = "gpt-4o-mini", 
        temperature: float = 0.7,
        empresa_config_path: Optional[str] = None
    ):
        """
        Inicializa el agente LangChain.
        
        Args:
            provider: Proveedor de IA ("openai" o "gemini")
            model_name: Nombre del modelo a usar
            temperature: Temperatura para la generación (0.0 a 1.0)
            empresa_config_path: Ruta opcional al archivo de configuración de la empresa
        """
        self.provider = provider.lower()
        self.model_name = model_name
        self.temperature = temperature
        self.reference_texts: List[str] = []
        self.empresa_config = get_empresa_config(empresa_config_path)
        
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
            
            # ChatOpenAI acepta cualquier modelo válido de OpenAI
            # Validamos que el modelo esté en nuestra lista recomendada, pero LangChain puede aceptar otros
            try:
                self.llm = ChatOpenAI(
                    model=model_name,
                    temperature=temperature,
                    openai_api_key=api_key
                )
            except Exception as e:
                # Si el modelo no es válido, LangChain lanzará un error
                # Esto puede pasar si el modelo no existe o no tienes acceso
                error_msg = str(e)
                if "model" in error_msg.lower() and ("not found" in error_msg.lower() or "does not exist" in error_msg.lower()):
                    raise ValueError(
                        f"El modelo '{model_name}' no está disponible o no tienes acceso.\n"
                        f"Modelos recomendados disponibles: {', '.join(self.OPENAI_MODELS.keys())}\n"
                        f"Error: {error_msg}"
                    )
                raise
        elif self.provider == "gemini":
            # Usar ChatGoogleGenerativeAI de LangChain según documentación oficial
            # https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai
            if not GEMINI_AVAILABLE:
                raise ImportError("langchain-google-genai no está instalado. Instálelo con: pip install langchain-google-genai")
            
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY o GEMINI_API_KEY no está configurada. Por favor, configura tu API key.")
            
            try:
                # Usar ChatGoogleGenerativeAI de LangChain (método correcto según documentación)
                self.llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    temperature=temperature,
                    google_api_key=api_key
                )
            except Exception as e:
                error_msg = str(e)
                # Si el modelo falla, mostrar error claro
                if "404" in error_msg or "not found" in error_msg.lower():
                    raise ValueError(
                        f"No se pudo inicializar el modelo '{model_name}' de Gemini.\n"
                        f"Error: {error_msg}\n\n"
                        f"💡 Verifica:\n"
                        f"1. Que tu API key (GOOGLE_API_KEY) sea válida\n"
                        f"2. Que la API de Gemini esté habilitada en Google Cloud\n"
                        f"3. Que el modelo 'gemini-flash-latest' esté disponible en tu cuenta\n"
                        f"4. Actualiza langchain-google-genai: pip install --upgrade langchain-google-genai"
                    )
                else:
                    raise
    
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
    
    def _get_empresa_context(self) -> str:
        """Genera contexto de la empresa desde la configuración."""
        contexto_completo = self.empresa_config.get_contexto_completo()
        if not contexto_completo:
            return ""
        
        return f"\n\n--- CONTEXTO Y VALORES EMPRESARIALES ---\n{contexto_completo}\n\nIMPORTANTE: El texto generado debe estar alineado con estos valores, misión, visión y contexto empresarial. Usa el tono de comunicación especificado.\n"
    
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
            if self.provider == "gemini":
                # Usar ChatGoogleGenerativeAI de LangChain (método correcto)
                response = self.llm.invoke(messages)
                
                # Extraer el texto de la respuesta de Gemini
                # Según la documentación de LangChain, usar response.content directamente
                texto = ""
                
                try:
                    # Intentar obtener el contenido directamente
                    if hasattr(response, 'content'):
                        contenido = response.content
                        
                        # Verificar que no sea una función
                        if callable(contenido):
                            # Si es una función, no podemos usarla directamente
                            # Intentar obtener el texto de otra manera
                            contenido = str(response)
                        elif isinstance(contenido, list):
                            # Si es una lista (Gemini 3), extraer el texto de cada elemento
                            textos = []
                            for item in contenido:
                                if isinstance(item, dict):
                                    # Si tiene 'text', usarlo
                                    if 'text' in item:
                                        textos.append(str(item['text']))
                                    # Si tiene 'type' y 'text'
                                    elif item.get('type') == 'text' and 'text' in item:
                                        textos.append(str(item['text']))
                                    else:
                                        textos.append(str(item))
                                else:
                                    textos.append(str(item))
                            texto = " ".join(textos)
                        elif isinstance(contenido, str):
                            texto = contenido
                        else:
                            texto = str(contenido)
                    else:
                        # Si no tiene content, convertir toda la respuesta a string
                        texto = str(response)
                    
                    # Asegurar que texto sea un string válido y no una función
                    if callable(texto):
                        texto = str(response)
                    
                    if not isinstance(texto, str):
                        texto = str(texto)
                    
                    # Limpiar el texto
                    texto = texto.strip()
                    
                except Exception as e:
                    # Si hay algún error al extraer el texto, usar str(response)
                    texto = str(response)
                    if callable(texto):
                        texto = f"Error al extraer texto: {str(e)}"
                
                return {
                    "texto": texto,
                    "tokens_usados": response.usage_metadata.get('total_tokens', 0) if hasattr(response, 'usage_metadata') and response.usage_metadata else 0,
                    "costo": 0.0  # Gemini gratuito
                }
            elif self.provider == "openai" and use_callback:
                with get_openai_callback() as cb:
                    response = self.llm.invoke(messages)
                    texto = response.content
                    return {
                        "texto": texto,
                        "tokens_usados": cb.total_tokens if cb else 0,
                        "costo": cb.total_cost if cb else 0.0
                    }
            else:
                # OpenAI sin callback
                response = self.llm.invoke(messages)
                texto = response.content
                return {
                    "texto": texto,
                    "tokens_usados": 0,
                    "costo": 0.0
                }
        except Exception as e:
            error_msg = str(e)
            # Mejorar mensajes de error para Gemini
            if self.provider == "gemini":
                if "404" in error_msg or "not found" in error_msg.lower() or "not supported" in error_msg.lower():
                    sugerencia = (
                        f"\n\n💡 El modelo '{self.model_name}' no está disponible.\n\n"
                        f"Verifica que:\n"
                        f"1. Tu API key (GOOGLE_API_KEY) sea válida\n"
                        f"2. La API de Gemini esté habilitada en Google Cloud\n"
                        f"3. El modelo 'gemini-flash-latest' esté disponible en tu cuenta\n"
                        f"4. Actualiza langchain-google-genai: pip install --upgrade langchain-google-genai\n"
                        f"5. Revisa la documentación: https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai"
                    )
                    
                    return {
                        "texto": f"Error al procesar con Gemini: {error_msg}{sugerencia}",
                        "tokens_usados": 0,
                        "costo": 0.0
                    }
            # Detectar errores específicos de OpenAI
            if self.provider == "openai":
                if "429" in error_msg or "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                    sugerencia = (
                        f"\n\n⚠️ Has excedido tu cuota de OpenAI.\n\n"
                        f"💡 Soluciones:\n"
                        f"1. **Usa Gemini (GRATUITO)**: Cambia al proveedor 'Google Gemini' en el sidebar\n"
                        f"   - Gemini es completamente gratuito y no tiene límites de cuota\n"
                        f"   - Modelos disponibles: gemini-1.5-flash (recomendado), gemini-1.5-pro, gemini-pro\n\n"
                        f"2. **Espera**: Espera unos minutos y vuelve a intentar con OpenAI\n\n"
                        f"3. **Verifica tu cuenta**: Revisa tu plan y facturación en https://platform.openai.com/account/billing\n\n"
                        f"💡 Recomendación: Usa Gemini para evitar problemas de cuota."
                    )
                    return {
                        "texto": f"Error al procesar con OpenAI: {error_msg}{sugerencia}",
                        "tokens_usados": 0,
                        "costo": 0.0
                    }
                elif "model_not_found" in error_msg.lower() or "does not exist" in error_msg.lower():
                    sugerencia = (
                        f"\n\n⚠️ El modelo seleccionado no está disponible.\n\n"
                        f"💡 Soluciones:\n"
                        f"1. Cambia a otro modelo de OpenAI en el sidebar (gpt-4o-mini o gpt-3.5-turbo)\n"
                        f"2. Usa Gemini (GRATUITO) cambiando al proveedor 'Google Gemini' en el sidebar\n"
                    )
                    return {
                        "texto": f"Error al procesar con OpenAI: {error_msg}{sugerencia}",
                        "tokens_usados": 0,
                        "costo": 0.0
                    }
            
            return {
                "texto": f"Error al procesar: {error_msg}",
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
        empresa_context = self._get_empresa_context()
        
        prompt = f"""Eres un asistente experto en comunicación empresarial. 
Tu tarea es generar un texto profesional, claro y coherente sobre el siguiente tema:

TEMA: {tema}

{empresa_context}

REQUISITOS:
- El texto debe tener aproximadamente {max_palabras} palabras (puede variar ligeramente, pero intenta mantenerte cerca de este número)
- Debe ser profesional pero cercano
- Debe mantener un tono empresarial apropiado
- Estructura clara con párrafos bien organizados
- Debe reflejar y alinearse con los valores, misión y visión proporcionados
{instrucciones_adicionales if instrucciones_adicionales else ''}

{style_context}

Por favor, genera el texto completo asegurándote de que esté alineado con la identidad y valores proporcionados y que se acerque al objetivo de aproximadamente {max_palabras} palabras:"""
        
        system_content = f"Eres un experto en comunicación empresarial y redacción profesional. Generas textos que reflejan los valores, misión y cultura empresarial de manera natural y coherente. Intentas respetar los límites de longitud especificados cuando es posible."
        
        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=prompt)
        ]
        
        resultado = self._invoke_llm(messages)
        
        return resultado
    
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
        empresa_context = self._get_empresa_context()
        
        prompt = f"""Eres un editor experto en comunicación empresarial.
Tu tarea es corregir y mejorar el siguiente texto, mejorando:
- Ortografía y gramática
- Claridad y fluidez
- Estilo profesional
- Estructura y organización
- Coherencia
- Alineación con los valores y contexto proporcionados

{empresa_context}

TEXTO ORIGINAL:
{texto}

{instrucciones_adicionales if instrucciones_adicionales else ''}

{style_context}

Por favor, proporciona el texto corregido y mejorado, asegurándote de que esté alineado con los valores proporcionados:"""
        
        system_content = "Eres un editor experto en comunicación empresarial y redacción profesional. Mejoras textos manteniendo la alineación con los valores y la identidad empresarial de manera natural."
        
        messages = [
            SystemMessage(content=system_content),
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
        empresa_context = self._get_empresa_context()
        
        prompt = f"""Eres un experto en comunicación empresarial.
Tu tarea es crear un resumen conciso y profesional del siguiente texto:

{empresa_context}

TEXTO ORIGINAL:
{texto}

REQUISITOS:
- El resumen debe tener aproximadamente {max_palabras} palabras
- Debe mantener las ideas principales y el mensaje clave
- Debe ser claro y profesional
- Mantener el tono original y alineado con la identidad proporcionada
{instrucciones_adicionales if instrucciones_adicionales else ''}

Por favor, proporciona el resumen:"""
        
        system_content = "Eres un experto en comunicación empresarial y creación de resúmenes profesionales."
        
        messages = [
            SystemMessage(content=system_content),
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
    
    @staticmethod
    def list_available_gemini_models() -> List[str]:
        """
        Lista los modelos de Gemini disponibles usando la API de Google.
        
        Returns:
            Lista de nombres de modelos disponibles
        """
        if not GEMINI_GENAI_AVAILABLE:
            return []
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return []
        
        try:
            genai.configure(api_key=api_key)
            models = genai.list_models()
            
            # Solo usar gemini-flash-latest
            target_model = 'gemini-flash-latest'
            
            # Filtrar solo modelos que soportan generateContent Y es gemini-flash-latest
            available_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    # Extraer solo el nombre del modelo (sin el prefijo "models/")
                    model_name = model.name.replace('models/', '')
                    # Solo incluir si es gemini-flash-latest
                    if model_name == target_model:
                        available_models.append(model_name)
                        break  # Solo necesitamos uno
            
            return available_models
        except Exception as e:
            # Si falla, retornar lista vacía
            return []
