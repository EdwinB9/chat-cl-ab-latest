# 🚀 Guía Completa de Deployment

## 📋 Problemas Comunes con Streamlit Cloud

Tu aplicación tiene dos características que pueden causar problemas en Streamlit Cloud:

1. **Variables de entorno (.env)**: Streamlit Cloud no lee archivos `.env`, usa "Secrets"
2. **Almacenamiento local (data/)**: Streamlit Cloud no persiste archivos locales entre reinicios

---

## 🌐 Opciones de Deployment

### 1. **Streamlit Cloud** (Gratis, pero con limitaciones)

**Ventajas:**
- ✅ Completamente gratuito
- ✅ Deployment automático desde GitHub
- ✅ Fácil de configurar

**Desventajas:**
- ❌ No persiste archivos locales (se pierden datos en `data/`)
- ❌ Requiere usar "Secrets" en lugar de `.env`
- ❌ Límites de recursos

**Cómo deployar:**

1. **Sube tu código a GitHub** (si no lo has hecho)
2. **Ve a [share.streamlit.io](https://share.streamlit.io)**
3. **Conecta tu repositorio**
4. **Configura Secrets:**
   - En la configuración de la app, ve a "Secrets"
   - Agrega tus API keys en formato TOML:
   ```toml
   GOOGLE_API_KEY = "tu_api_key_aqui"
   GROQ_API_KEY = "tu_api_key_aqui"
   OPENAI_API_KEY = "tu_api_key_aqui"
   # ... etc
   ```
5. **Configura el archivo principal:**
   - Asegúrate de que `streamlit_app.py` esté en la raíz (ya lo tienes)
   - Streamlit Cloud buscará `streamlit_app.py` o `app/main.py`

**⚠️ Problema del almacenamiento:**
Los datos en `data/` se perderán. Necesitarás migrar a una base de datos (ver sección "Soluciones" abajo).

---

### 2. **Railway** (Recomendado - Gratis con límites)

**Ventajas:**
- ✅ Persistencia de archivos (volúmenes)
- ✅ Variables de entorno fáciles
- ✅ Plan gratuito generoso
- ✅ Deployment automático desde GitHub

**Desventajas:**
- ⚠️ Límites en el plan gratuito (500 horas/mes)

**Cómo deployar:**

1. **Crea cuenta en [railway.app](https://railway.app)**
2. **Nuevo proyecto → Deploy from GitHub**
3. **Configura variables de entorno:**
   - Ve a Variables → New Variable
   - Agrega cada API key: `GOOGLE_API_KEY`, `GROQ_API_KEY`, etc.
4. **Configura el comando de inicio:**
   - Settings → Deploy → Start Command: `streamlit run streamlit_app.py --server.port $PORT`
5. **Agrega persistencia (opcional):**
   - Si quieres que `data/` persista, agrega un volumen en Settings

**Costo:** Gratis hasta 500 horas/mes, luego $5/mes

---

### 3. **Render** (Gratis con límites)

**Ventajas:**
- ✅ Plan gratuito disponible
- ✅ Variables de entorno fáciles
- ✅ Persistencia con discos (de pago)

**Desventajas:**
- ❌ Plan gratuito: se duerme después de 15 min de inactividad
- ❌ Sin persistencia en plan gratuito

**Cómo deployar:**

1. **Crea cuenta en [render.com](https://render.com)**
2. **New → Web Service**
3. **Conecta tu repositorio de GitHub**
4. **Configuración:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
5. **Variables de entorno:**
   - Environment → Add Environment Variable
   - Agrega todas tus API keys

**Costo:** Gratis (con limitaciones), $7/mes para persistencia

---

### 4. **Fly.io** (Gratis con límites)

**Ventajas:**
- ✅ Plan gratuito generoso
- ✅ Persistencia con volúmenes
- ✅ Muy rápido

**Desventajas:**
- ⚠️ Requiere CLI y configuración más técnica

**Cómo deployar:**

1. **Instala Fly CLI:** `curl -L https://fly.io/install.sh | sh`
2. **Login:** `fly auth login`
3. **Crea app:** `fly launch`
4. **Configura variables:** `fly secrets set GOOGLE_API_KEY=tu_key`
5. **Agrega volumen para datos:** `fly volumes create data --size 1`

**Costo:** Gratis hasta cierto uso, luego pay-as-you-go

---

### 5. **Heroku** (De pago, pero confiable)

**Ventajas:**
- ✅ Muy confiable
- ✅ Persistencia con add-ons
- ✅ Fácil de usar

**Desventajas:**
- ❌ Ya no tiene plan gratuito (desde 2022)
- ❌ Más caro que alternativas

**Costo:** Desde $5/mes

---

### 6. **DigitalOcean App Platform** (Recomendado para producción)

**Ventajas:**
- ✅ Persistencia incluida
- ✅ Muy confiable
- ✅ Escalable

**Desventajas:**
- ❌ Plan mínimo de pago ($5/mes)

**Costo:** Desde $5/mes

---

## 🔧 Soluciones para los Problemas

### Solución 1: Adaptar código para Streamlit Secrets

Si quieres usar Streamlit Cloud, necesitas modificar cómo se cargan las variables de entorno.

**Modificar `app/main.py` y otros archivos que usan `load_dotenv()`:**

```python
import os
from dotenv import load_dotenv

# Intentar cargar .env local (para desarrollo)
load_dotenv()

# Si estamos en Streamlit Cloud, usar secrets
if hasattr(st, "secrets"):
    # Streamlit Cloud usa secrets
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    # ... etc para todas las API keys
```

### Solución 2: Migrar almacenamiento a base de datos

Para que los datos persistan en Streamlit Cloud o cualquier plataforma, necesitas usar una base de datos.

**Opciones gratuitas:**

1. **SQLite en memoria** (no persiste, pero funciona)
2. **Supabase** (PostgreSQL gratuito)
3. **MongoDB Atlas** (gratis hasta 512MB)
4. **Firebase** (gratis con límites)
5. **Google Cloud Storage** (para archivos JSON)

**Ejemplo con Supabase (PostgreSQL gratuito):**

1. Crea cuenta en [supabase.com](https://supabase.com)
2. Crea un proyecto
3. Obtén la connection string
4. Modifica `IOManager` para usar PostgreSQL en lugar de archivos

---

## 📝 Recomendación Final

### Para desarrollo/pruebas:
- **Streamlit Cloud** (gratis, pero sin persistencia)
- O **Railway** (gratis, con persistencia)

### Para producción:
- **Railway** ($5/mes) o **Render** ($7/mes)
- Con base de datos (Supabase gratis o MongoDB Atlas gratis)

---

## 🛠️ Pasos Rápidos para Railway (Recomendado)

1. **Sube tu código a GitHub**
2. **Ve a [railway.app](https://railway.app) y crea cuenta**
3. **New Project → Deploy from GitHub**
4. **Selecciona tu repositorio**
5. **Variables → Agrega todas tus API keys:**
   - `GOOGLE_API_KEY`
   - `GROQ_API_KEY`
   - `OPENAI_API_KEY`
   - etc.
6. **Settings → Deploy → Start Command:**
   ```
   streamlit run streamlit_app.py --server.port $PORT
   ```
7. **¡Listo!** Tu app estará disponible en una URL de Railway

---

## 🔐 Seguridad

**NUNCA:**
- ❌ Subas tu archivo `.env` a GitHub
- ❌ Compartas tus API keys públicamente
- ❌ Hardcodees API keys en el código

**SÍ:**
- ✅ Usa variables de entorno o secrets
- ✅ Agrega `.env` a `.gitignore` (ya lo tienes)
- ✅ Rota tus API keys si se filtran

---

## 📚 Recursos Adicionales

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [Supabase Docs](https://supabase.com/docs)

---

## ❓ ¿Necesitas ayuda?

Si tienes problemas específicos con alguna plataforma, revisa:
1. Los logs de deployment
2. Las variables de entorno configuradas
3. El formato del archivo principal (`streamlit_app.py`)

