# 🚀 Deployment Rápido - Resumen

## ⚡ Opción Más Rápida: Railway (Recomendado)

### Pasos (5 minutos):

1. **Sube tu código a GitHub** (si no lo has hecho)
   ```bash
   git add .
   git commit -m "Preparado para deployment"
   git push origin main
   ```

2. **Ve a [railway.app](https://railway.app)** y crea cuenta (gratis)

3. **New Project → Deploy from GitHub**

4. **Selecciona tu repositorio**

5. **Variables → Agrega tus API keys:**
   - `GOOGLE_API_KEY` = tu_key
   - `GROQ_API_KEY` = tu_key
   - `OPENAI_API_KEY` = tu_key (si usas OpenAI)
   - etc.

6. **Settings → Deploy → Start Command:**
   ```
   streamlit run streamlit_app.py --server.port $PORT
   ```

7. **¡Listo!** Tu app estará en una URL tipo: `tu-app.railway.app`

---

## 🌐 Streamlit Cloud (Gratis, pero sin persistencia)

### Pasos:

1. **Sube tu código a GitHub**

2. **Ve a [share.streamlit.io](https://share.streamlit.io)**

3. **New app → Conecta tu repositorio**

4. **Settings → Secrets → Agrega:**
   ```toml
   GOOGLE_API_KEY = "tu_key"
   GROQ_API_KEY = "tu_key"
   # etc.
   ```

5. **Deploy**

⚠️ **Nota:** Los datos en `data/` se perderán. Solo funciona para pruebas.

---

## 📋 Comparación Rápida

| Plataforma | Gratis | Persistencia | Facilidad | Recomendado |
|------------|--------|--------------|-----------|-------------|
| **Railway** | ✅ (500h/mes) | ✅ | ⭐⭐⭐⭐⭐ | ✅ **SÍ** |
| **Streamlit Cloud** | ✅ | ❌ | ⭐⭐⭐⭐⭐ | ⚠️ Solo pruebas |
| **Render** | ✅ (se duerme) | ❌ (gratis) | ⭐⭐⭐⭐ | ⚠️ Limitado |
| **Fly.io** | ✅ | ✅ | ⭐⭐⭐ | ✅ Buena opción |

---

## 🔧 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` tenga todas las dependencias
- Railway/Render instalan automáticamente desde `requirements.txt`

### Error: "API Key not found"
- Verifica que agregaste las variables de entorno en la plataforma
- En Railway: Variables → New Variable
- En Streamlit Cloud: Settings → Secrets

### Error: "Port already in use"
- Usa: `streamlit run streamlit_app.py --server.port $PORT`
- El `$PORT` es la variable que la plataforma proporciona

---

## 📚 Documentación Completa

Para más detalles, ver: **[GUIA_DEPLOYMENT.md](GUIA_DEPLOYMENT.md)**

---

## ✅ Checklist Pre-Deployment

- [ ] Código subido a GitHub
- [ ] `.env` en `.gitignore` (ya está)
- [ ] `requirements.txt` actualizado
- [ ] `streamlit_app.py` en la raíz (ya está)
- [ ] API keys listas para agregar en la plataforma

---

## 🆘 ¿Problemas?

1. Revisa los logs de deployment en la plataforma
2. Verifica que todas las variables de entorno estén configuradas
3. Asegúrate de que `streamlit_app.py` esté en la raíz del proyecto

