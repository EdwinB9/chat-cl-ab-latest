"""
Script para verificar qué modelos de Gemini están disponibles.
Ejecuta este script para ver qué modelos puedes usar.
"""

import os
import sys

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Intentar cargar desde dotenv si está disponible
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY no está configurada.")
    print("💡 Configura tu API key en el archivo .env o en el sidebar de la aplicación.")
    exit(1)

try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    print("🔍 Buscando modelos disponibles...\n")
    models = genai.list_models()
    
    available_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            model_name = model.name.replace('models/', '')
            available_models.append(model_name)
            print(f"✅ {model_name}")
    
    if not available_models:
        print("❌ No se encontraron modelos disponibles")
    else:
        print(f"\n📊 Total de modelos disponibles: {len(available_models)}")
        print("\n💡 Puedes usar cualquiera de estos modelos en el sidebar de la aplicación.")
        
except ImportError:
    print("❌ google-generativeai no está instalado. Ejecuta: pip install google-generativeai")
except Exception as e:
    print(f"❌ Error al listar modelos: {str(e)}")

