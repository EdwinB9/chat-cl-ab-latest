"""
Script para verificar qué modelos soporta LangChain.
"""

import sys
import os

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("🔍 Verificando modelos soportados por LangChain...\n")

# Verificar OpenAI
print("=" * 60)
print("📋 MODELOS DE OPENAI (ChatOpenAI)")
print("=" * 60)
try:
    from langchain_openai import ChatOpenAI
    print("✅ langchain-openai está instalado")
    
    # Modelos comunes de OpenAI que soporta ChatOpenAI
    openai_models = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k"
    ]
    
    print("\n📝 Modelos comúnmente soportados por ChatOpenAI:")
    for model in openai_models:
        print(f"   - {model}")
    
    print("\n💡 Nota: ChatOpenAI acepta cualquier nombre de modelo válido de OpenAI.")
    print("   Los modelos disponibles dependen de tu cuenta y plan de OpenAI.")
    
except ImportError:
    print("❌ langchain-openai no está instalado")
    print("   Instala con: pip install langchain-openai")

print("\n" + "=" * 60)
print("📋 MODELOS DE GEMINI (ChatGoogleGenerativeAI)")
print("=" * 60)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("✅ langchain-google-genai está instalado")
    
    # Modelos comunes de Gemini
    gemini_models = [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest"
    ]
    
    print("\n📝 Modelos comúnmente soportados por ChatGoogleGenerativeAI:")
    for model in gemini_models:
        print(f"   - {model}")
    
    print("\n💡 Nota: ChatGoogleGenerativeAI acepta cualquier nombre de modelo válido de Gemini.")
    print("   Los modelos disponibles dependen de tu API key y acceso a Google Cloud.")
    
except ImportError:
    print("❌ langchain-google-genai no está instalado")
    print("   Instala con: pip install langchain-google-genai")

print("\n" + "=" * 60)
print("📋 VERIFICACIÓN DE MODELOS EN NUESTRA APP")
print("=" * 60)

try:
    from app.utils.langchain_agent import LangChainAgent
    
    print("\n✅ Nuestros modelos configurados para OpenAI:")
    openai_models = LangChainAgent.get_available_models("openai")
    for key, value in openai_models.items():
        print(f"   - {key}")
    
    print("\n✅ Nuestros modelos configurados para Gemini (gratuitos):")
    gemini_models = LangChainAgent.get_available_models("gemini")
    for key, value in gemini_models.items():
        print(f"   - {key}")
    
except Exception as e:
    print(f"❌ Error al verificar modelos: {str(e)}")

print("\n" + "=" * 60)
print("💡 RECOMENDACIONES")
print("=" * 60)
print("""
1. Para OpenAI:
   - Usa modelos que estén disponibles en tu cuenta
   - gpt-4o-mini es el más económico y recomendado
   - gpt-3.5-turbo es el estándar más económico

2. Para Gemini:
   - Usa solo modelos gratuitos si quieres evitar costos
   - gemini-1.5-flash es el más rápido y recomendado
   - gemini-1.5-pro es más potente pero con límites

3. Si un modelo no funciona:
   - Verifica que esté disponible en tu cuenta
   - Revisa que tu API key tenga acceso
   - Considera usar modelos alternativos
""")

