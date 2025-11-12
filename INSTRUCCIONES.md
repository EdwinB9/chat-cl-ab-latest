# 📚 Instrucciones de Instalación y Uso

## 🚀 Instalación

### 1. Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Una cuenta de OpenAI con API key

### 2. Instalación de Dependencias

```bash
# Crear un entorno virtual (recomendado)
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configuración de las API Keys

Crea un archivo `.env` en la raíz del proyecto con tus API keys (puedes usar una o ambas):

```env
# OpenAI (para modelos GPT-4o, GPT-4o-mini, etc.)
OPENAI_API_KEY=tu_api_key_openai_aqui

# Google Gemini (para modelos Gemini Pro, Gemini Flash, etc.)
GOOGLE_API_KEY=tu_api_key_google_aqui
```

O puedes ingresarlas directamente en la aplicación cuando la ejecutes (se pedirán en el sidebar).

**⚠️ Importante**: 
- No compartas tus API keys públicamente
- Puedes usar solo OpenAI, solo Gemini, o ambos
- Necesitas al menos una API key configurada para usar la aplicación
- Obtén tu API key de OpenAI en: https://platform.openai.com/api-keys
- Obtén tu API key de Google en: https://makersuite.google.com/app/apikey

## 🎯 Uso

### Ejecutar la Aplicación

**Importante**: Asegúrate de estar en el directorio raíz del proyecto al ejecutar el comando.

```bash
# Desde el directorio raíz del proyecto
streamlit run app/main.py
```

O usa los scripts proporcionados:
- **Windows**: Ejecuta `run.bat`
- **Linux/Mac**: Ejecuta `./run.sh` (primero dale permisos: `chmod +x run.sh`)

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

**Nota**: Si encuentras el error `ModuleNotFoundError: No module named 'app'`, asegúrate de:
1. Estar en el directorio raíz del proyecto (donde está el archivo `requirements.txt`)
2. Tener todas las dependencias instaladas: `pip install -r requirements.txt`

### Funcionalidades

#### 1. Generar Texto
- Ingresa un tema o prompt
- Configura la cantidad de palabras deseadas
- Opcionalmente, agrega instrucciones adicionales
- Haz clic en "Generar Texto"

#### 2. Corregir Texto
- Pega el texto que deseas corregir
- Opcionalmente, agrega instrucciones específicas de corrección
- Haz clic en "Corregir Texto"

#### 3. Resumir Texto
- Pega el texto que deseas resumir
- Configura la cantidad máxima de palabras para el resumen
- Opcionalmente, agrega instrucciones específicas
- Haz clic en "Resumir Texto"

### Archivos de Referencia

Puedes subir archivos `.txt` o `.json` con textos de referencia para mejorar el estilo de las generaciones:
- Los textos aprobados se usan automáticamente como referencia
- Los archivos subidos también se incluyen en el contexto

### Feedback

Después de cada generación, puedes:
- 👍 **Me gusta**: Aprobar el texto (se guarda como referencia)
- 👎 **No me gusta**: Rechazar el texto (se mueve a rechazados)
- 💬 **Comentario**: Agregar comentarios sobre el resultado

### Historial

- El historial se guarda automáticamente en `data/resultados/`
- Los archivos se organizan por mes (formato: `YYYY-MM.json`)
- Los textos rechazados se guardan en `data/rechazados/`

### Descargar Resultados

Puedes descargar los resultados en dos formatos:
- **TXT**: Texto plano
- **JSON**: Datos completos con metadata

## 📁 Estructura de Carpetas

```
Chat CL-AB LST/
├── app/
│   ├── components/       # Componentes de UI
│   ├── utils/           # Utilidades y lógica de negocio
│   └── main.py          # Aplicación principal
├── data/
│   ├── resultados/      # Resultados aprobados (JSON mensuales)
│   └── rechazados/      # Resultados rechazados (JSON mensuales)
├── requirements.txt     # Dependencias
├── README.md           # Documentación del proyecto
└── INSTRUCCIONES.md    # Este archivo
```

## 🔧 Configuración Avanzada

### Proveedores de IA

La aplicación soporta múltiples proveedores de IA:

#### OpenAI
- `gpt-4o-mini`: Más económico, recomendado para la mayoría de casos
- `gpt-4o`: Más potente, mejor calidad (más costoso)
- `gpt-4-turbo`: Versión turbo de GPT-4
- `gpt-3.5-turbo`: Modelo más económico y rápido

#### Google Gemini
- `gemini-1.5-pro`: Modelo más potente y avanzado
- `gemini-1.5-flash`: Versión rápida y eficiente
- `gemini-pro`: Modelo estándar de Gemini

### Selección de Proveedor

Puedes cambiar entre proveedores en el sidebar:
1. Selecciona el proveedor (OpenAI o Google Gemini)
2. Elige el modelo específico de ese proveedor
3. La aplicación solo mostrará los proveedores que tienen API key configurada

### Temperatura
- **Baja (0.0-0.3)**: Textos más consistentes y predecibles
- **Media (0.4-0.7)**: Balance entre creatividad y consistencia (recomendado)
- **Alta (0.8-1.0)**: Textos más creativos y variados

### Palabras Máximas
- Ajusta según tus necesidades
- Rango recomendado: 100-500 palabras
- Máximo: 2000 palabras

## ❓ Solución de Problemas

### Error: "API Key not found"
- Verifica que hayas creado el archivo `.env` con al menos una API key (OPENAI_API_KEY o GOOGLE_API_KEY)
- O ingresa la API key en el sidebar de la aplicación
- Asegúrate de que la API key corresponda al proveedor seleccionado

### Error: "Module not found"
- Asegúrate de haber instalado todas las dependencias: `pip install -r requirements.txt`
- Verifica que estés en el entorno virtual correcto

### Error: "Rate limit exceeded"
- Has excedido el límite de tu cuenta de OpenAI
- Espera unos minutos o actualiza tu plan de OpenAI

## 📝 Notas

- Los datos se guardan localmente en archivos JSON
- Los textos aprobados mejoran automáticamente el estilo de futuras generaciones
- El historial se mantiene por mes para facilitar la organización
- Todos los resultados incluyen metadata (modelo usado, configuración, feedback)

## 🆘 Soporte

Si tienes problemas o preguntas, revisa:
1. La documentación de OpenAI: https://platform.openai.com/docs
2. La documentación de Google Gemini: https://ai.google.dev/docs
3. La documentación de Streamlit: https://docs.streamlit.io
4. La documentación de LangChain: https://python.langchain.com

## 🔄 Cambiar entre Proveedores

Para cambiar entre OpenAI y Gemini:
1. Asegúrate de tener la API key del proveedor que deseas usar configurada
2. En el sidebar, selecciona el proveedor en el menú desplegable
3. Selecciona el modelo específico de ese proveedor
4. La aplicación reinicializará automáticamente el agente con el nuevo proveedor

**💡 Tip**: Puedes tener ambas API keys configuradas y cambiar entre proveedores en cualquier momento sin reiniciar la aplicación.

