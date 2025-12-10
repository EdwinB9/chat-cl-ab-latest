# 🧠 Chatbot CL-AB con Streamlit + LangChain

## 🎯 Objetivo General
Desarrollar una aplicación en **Streamlit** que permita a un usuario sin conocimientos de programación **generar, corregir y resumir textos empresariales**, con un estilo coherente basado en textos de referencia (por ejemplo, comunicados creados por una líder de comunicaciones).

El sistema debe permitir **retroalimentación directa** del usuario sobre la calidad de los textos generados, para mejorar progresivamente las recomendaciones y mantener una base de datos limpia y relevante.

---

## 🚀 Instalación y Configuración

### 1️⃣ Requisitos Previos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- Cuenta(s) con API key(s) de al menos uno de los proveedores de IA soportados

### 2️⃣ Instalación

#### Opción A: Instalación Inicial

```bash
# 1. Clonar o descargar el proyecto
cd "Chat CL-AB LST"

# 2. Crear un entorno virtual (recomendado)
python -m venv venv

# 3. Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

#### Opción B: Actualizar Dependencias

Si ya tienes el proyecto instalado y quieres actualizar a la última versión:

```bash
# 1. Activar el entorno virtual (si usas uno)
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/Mac

# 2. Actualizar pip primero
python -m pip install --upgrade pip

# 3. Actualizar todas las dependencias
pip install --upgrade -r requirements.txt

# 4. Si tienes problemas, reinstalar todas las dependencias
pip install --force-reinstall -r requirements.txt
```

### 3️⃣ Configuración de API Keys

#### Crear el archivo `.env`

1. **Copia el archivo de ejemplo:**
   ```bash
   # En Windows (PowerShell):
   copy example.env .env
   
   # En Windows (CMD):
   copy example.env .env
   
   # En Linux/Mac:
   cp example.env .env
   ```

2. **Edita el archivo `.env`** con tu editor de texto favorito y agrega tus API keys:

```env
# APIs de IA Gratuitas (configurar al menos una)

# Google Gemini - IA generativa avanzada (RECOMENDADO - GRATUITO)
# Obtén tu API key en: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=tu_gemini_api_key_aqui

# Groq - Ultra rápido y gratuito
# Obtén tu API key en: https://console.groq.com
GROQ_API_KEY=tu_groq_api_key_aqui

# Hugging Face - Completamente gratuito
# Obtén tu token en: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=tu_huggingface_token_aqui

# Together AI - Modelos open source
# Obtén tu API key en: https://api.together.xyz
TOGETHER_API_KEY=tu_together_api_key_aqui

# Cohere - Gratuito para desarrollo
# Obtén tu API key en: https://dashboard.cohere.ai
COHERE_API_KEY=tu_cohere_api_key_aqui

# OpenAI - Requiere pago (opcional)
# Obtén tu API key en: https://platform.openai.com/api-keys
OPENAI_API_KEY=tu_openai_api_key_aqui

# Configuración de la aplicación
APP_DEBUG=false
MAX_REQUESTS_PER_MINUTE=30
```

#### 📝 Instrucciones para obtener API Keys

##### 🟢 Google Gemini (Gratuito - Recomendado)
1. Visita: **https://makersuite.google.com/app/apikey**
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la API key y pégala en tu archivo `.env`

##### 🟢 Groq (Gratuito - Muy Rápido)
1. Visita: **https://console.groq.com**
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" en el menú
4. Genera una nueva API key
5. Copia la API key y pégala en tu archivo `.env`

##### 🟢 Hugging Face (Gratuito)
1. Visita: **https://huggingface.co**
2. Crea una cuenta o inicia sesión
3. Ve a Settings → Access Tokens: **https://huggingface.co/settings/tokens**
4. Genera un nuevo token con permisos de lectura
5. Copia el token y pégala en tu archivo `.env`

##### 🟢 Together AI (Gratuito - Modelos Open Source)
1. Visita: **https://api.together.xyz**
2. Crea una cuenta o inicia sesión
3. Ve a la sección de API Keys
4. Genera una nueva API key
5. Copia la API key y pégala en tu archivo `.env`

##### 🟢 Cohere (Gratuito para Desarrollo)
1. Visita: **https://dashboard.cohere.ai**
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" en el dashboard
4. Genera una nueva API key
5. Copia la API key y pégala en tu archivo `.env`
6. **Nota**: Solo el modelo `command-nightly` está disponible actualmente

##### 🔵 OpenAI (Requiere Pago)
1. Visita: **https://platform.openai.com/api-keys**
2. Inicia sesión con tu cuenta de OpenAI
3. Haz clic en "Create new secret key"
4. Copia la API key y pégala en tu archivo `.env`
5. **Nota**: Requiere créditos en tu cuenta de OpenAI

**⚠️ Importante:**
- No compartas tu archivo `.env` públicamente
- Agrega `.env` a tu `.gitignore` si usas control de versiones
- Puedes configurar solo las API keys que vayas a usar (mínimo una)
- La aplicación solo mostrará los proveedores que tengan API key configurada

### 4️⃣ Agregar Logo de Casa Limpia (Opcional)

Para personalizar la aplicación con el logo de Casa Limpia, coloca el archivo del logo en la carpeta `static/` con uno de los siguientes nombres:

- `logo.png` o `casa_limpia_logo.png` (recomendado)
- `logo.jpg` o `casa_limpia_logo.jpg`
- `logo.svg` o `casa_limpia_logo.svg`

**Ubicación del archivo:**
```
/static/
└── logo.png  (o cualquiera de los nombres mencionados)
```

El logo se mostrará automáticamente:
- En el título principal de la aplicación (arriba del título "Chatbot CL-AB")
- En el sidebar (arriba de la sección de configuración)

**Formatos soportados:**
- PNG (recomendado para mejor calidad)
- JPG/JPEG
- SVG (escalable, ideal para diferentes tamaños)

**Tamaño recomendado:**
- Para el título principal: máximo 80px de altura
- Para el sidebar: máximo 60px de altura

Si no colocas ningún logo, la aplicación funcionará normalmente sin mostrar ningún logo.

### 5️⃣ Ejecutar la Aplicación

**Importante**: Asegúrate de estar en el directorio raíz del proyecto al ejecutar el comando.

```bash
# Opción 1: Usando Streamlit directamente
streamlit run app/main.py

# Opción 2: Usando los scripts proporcionados
# Windows:
run.bat

# Linux/Mac:
chmod +x run.sh
./run.sh
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

**Nota**: Si encuentras el error `ModuleNotFoundError: No module named 'app'`, asegúrate de:
1. Estar en el directorio raíz del proyecto (donde está el archivo `requirements.txt`)
2. Tener todas las dependencias instaladas: `pip install -r requirements.txt`
3. Estar usando el entorno virtual correcto (si usas uno)

---

## 🧩 Funcionalidades Principales

### 1️⃣ Módulos principales
- 📝 **Generar** → Crea nuevos textos a partir de un prompt o tema.  
- ✏️ **Corregir** → Mejora redacción, ortografía y estilo.  
- 🔍 **Resumir** → Condensa textos con control de longitud.

### 2️⃣ Configuraciones accesibles al usuario
- Seleccionar acción: *Generar*, *Corregir* o *Resumir*  
- Seleccionar proveedor de IA y modelo  
- Definir cantidad de palabras y temperatura  
- Subir archivos `.txt` o `.json` de referencia  
- Descargar resultados en `.txt` o `.json`  
- Consultar historial mensual con paginación  
- **Evaluar resultados**: *"Me gusta / No me gusta"* o *"Guardar / Descartar"*

---

## 🤖 Proveedores de IA Soportados

La aplicación soporta múltiples proveedores de IA. Solo necesitas configurar las API keys que vayas a usar.

### 🟢 Proveedores Gratuitos (Recomendados)

#### Google Gemini
- **Modelo disponible**: `gemini-flash-latest`
- **Enlace para API key**: https://makersuite.google.com/app/apikey
- **Características**: Gratuito, rápido, buena calidad

#### Groq
- **Modelos disponibles**: Varios modelos Llama y Mistral
- **Enlace para API key**: https://console.groq.com
- **Características**: Ultra rápido, completamente gratuito

#### Together AI
- **Modelos disponibles**: Modelos open source (Llama, Mistral, etc.)
- **Enlace para API key**: https://api.together.xyz
- **Características**: Modelos open source, gratuito con límites

#### Hugging Face
- **Modelos disponibles**: Varios modelos de Hugging Face
- **Enlace para token**: https://huggingface.co/settings/tokens
- **Características**: Completamente gratuito, amplia variedad de modelos

#### Cohere
- **Modelos disponibles**: `command-nightly` (único disponible actualmente)
- **Enlace para API key**: https://dashboard.cohere.ai
- **Características**: Gratuito para desarrollo
- **Nota**: Los modelos `command` y `command-light` fueron removidos el 15 de septiembre de 2025

### 🔵 Proveedores de Pago

#### OpenAI
- **Modelos disponibles**: `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`
- **Enlace para API key**: https://platform.openai.com/api-keys
- **Características**: Alta calidad, requiere créditos

**Nota**: `gpt-4-turbo` no está disponible en todas las cuentas.

---

## 💾 Almacenamiento y Organización de Datos

### Estructura de Carpetas
```
/data/
├── resultados/      # Resultados aprobados (JSON mensuales)
└── rechazados/      # Resultados rechazados (JSON mensuales)
```

### Estructura de JSON Mensual
```json
{
  "mes": "2025-11",
  "datos": [
    {
      "id": "2025-11-04T19-30-00",
      "accion": "generar",
      "tema": "Día del Operario de Limpieza",
      "resultado": "Celebramos este día con el objetivo...",
      "palabras": 150,
      "modelo": "gpt-4o-mini",
      "provider": "openai",
      "config": {"temperature": 0.4, "max_palabras": 200},
      "feedback": {
        "aprobado": true,
        "comentario": "El tono fue muy cercano al estilo deseado"
      }
    }
  ]
}
```

---

## 💡 Feedback Loop (Retroalimentación)

El usuario evalúa cada texto generado:

- 👍 **"Me gusta"** → Se guarda como aprobado y sirve de referencia futura  
- 👎 **"No me gusta"** → Se marca como rechazado y puede eliminarse  
- ✍️ **Comentario opcional** sobre el resultado

Los textos aprobados alimentan un **corpus interno** para mejorar el estilo.  
Los rechazados se guardan aparte o se descartan.

---

## ⚙️ Tecnologías

- **Frontend:** Streamlit  
- **Framework IA:** LangChain  
- **Proveedores de IA:** OpenAI, Google Gemini, Groq, Together AI, Cohere, Hugging Face
- **Modelos OpenAI:** GPT-4o, GPT-4o-mini, GPT-3.5-turbo
- **Modelos Gemini:** gemini-flash-latest
- **Persistencia:** Archivos JSON mensuales  
- **Procesamiento:** Pandas

---

## 🧱 Estructura de Código

```
/app/
├── main.py              # Aplicación principal
├── components/
│   ├── sidebar.py      # Configuración del sidebar
│   ├── result_display.py
│   ├── uploader.py
│   └── help_modal.py   # Mensajes de ayuda
├── utils/
│   ├── io_manager.py
│   ├── feedback_manager.py
│   ├── text_tools.py
│   └── langchain_agent.py  # Lógica de IA
└── data/
    ├── resultados/
    └── rechazados/
```

---

## 🌐 Flujo del Usuario

1. El usuario abre la app Streamlit  
2. Configura las API keys (si no están en `.env`)
3. Selecciona una acción (Generar / Corregir / Resumir)  
4. Configura longitud y creatividad  
5. (Opcional) Sube textos base  
6. El sistema genera o corrige el texto  
7. El usuario lo evalúa (Me gusta / No me gusta / Comenta)  
8. Se guarda automáticamente con su feedback

---

## ❓ Solución de Problemas

### Error: "API Key not found"
- Verifica que hayas creado el archivo `.env` en la raíz del proyecto
- Asegúrate de que la API key corresponda al proveedor seleccionado
- Verifica que el nombre de la variable en `.env` sea correcto (por ejemplo, `GOOGLE_API_KEY`)

### Error: "Module not found"
- Asegúrate de haber instalado todas las dependencias: `pip install -r requirements.txt`
- Verifica que estés en el entorno virtual correcto
- Intenta reinstalar: `pip install --force-reinstall -r requirements.txt`

### Error: "Rate limit exceeded" o "Quota exceeded"
- Has excedido el límite de tu cuenta del proveedor
- Espera unos minutos o actualiza tu plan
- Prueba con otro proveedor gratuito

### Error: "Model not found" o "404"
- El modelo seleccionado puede no estar disponible en tu cuenta
- Para Cohere: usa solo `command-nightly` (los otros modelos fueron removidos)
- Verifica que el modelo esté disponible en el proveedor seleccionado

### Proveedores no aparecen en el listado
- Verifica que la API key esté correctamente configurada en el archivo `.env`
- Asegúrate de que el paquete del proveedor esté instalado: `pip install -r requirements.txt`
- Reinicia Streamlit después de agregar nuevas API keys

---

## 📚 Documentación Adicional

- **Instrucciones detalladas**: Ver `INSTRUCCIONES.md`
- **Configuración de ejemplo**: Ver `example.env`
- **Ayuda en la aplicación**: Haz clic en el botón "❓ Ayuda de Configuración" en el sidebar

---

## 🔒 Futuras Mejoras

- Dashboard de métricas  
- Filtros por tono, tema o fecha  
- Sugerencias automáticas según feedback  
- Entrenamiento semántico con textos aprobados  

---

## ✅ Resumen Final

> Crear un chatbot empresarial configurable con Streamlit + LangChain, capaz de **generar, corregir y resumir textos** en el estilo de una líder de comunicaciones.  
> Soporta **múltiples proveedores de IA** (OpenAI, Google Gemini, Groq, Together AI, Cohere, Hugging Face) con selector de modelo integrado.  
> Los datos se almacenan en **JSON mensuales**, con retroalimentación del usuario para limpiar y mejorar continuamente la base.

---

## 🚀 Deployment (Despliegue en la Nube)

¿Quieres deployar tu aplicación en la nube? Tenemos guías completas:

- **[DEPLOYMENT_RAPIDO.md](DEPLOYMENT_RAPIDO.md)** - Guía rápida (5 minutos) para deployment
- **[GUIA_DEPLOYMENT.md](GUIA_DEPLOYMENT.md)** - Guía completa con todas las opciones

### Opciones Recomendadas:

1. **Railway** (⭐ Recomendado) - Gratis, con persistencia, fácil de usar
2. **Streamlit Cloud** - Gratis, pero sin persistencia de datos
3. **Render** - Gratis con limitaciones

La aplicación ya está preparada para funcionar en todas estas plataformas.

---

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de **Solución de Problemas** arriba
2. Verifica que todas las dependencias estén instaladas correctamente
3. Asegúrate de tener al menos una API key válida configurada en el archivo `.env`
4. Consulta la ayuda integrada en la aplicación (botón "❓ Ayuda de Configuración")
5. Para problemas de deployment, consulta las guías de deployment arriba

---

## 📝 Notas Importantes

- **Seguridad**: Nunca compartas tu archivo `.env` o tus API keys públicamente
- **Límites**: Los proveedores gratuitos tienen límites de uso
- **Actualizaciones**: Actualiza regularmente las dependencias con `pip install --upgrade -r requirements.txt`
- **Backup**: Los datos se guardan localmente en `data/`, haz backup regularmente
