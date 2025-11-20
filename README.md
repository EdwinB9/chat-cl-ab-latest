 # 🧠 Chatbot CL-AB con Streamlit + LangChain

## 🎯 Objetivo General
Desarrollar una aplicación en **Streamlit** que permita a un usuario sin conocimientos de programación **generar, corregir y resumir textos empresariales**, con un estilo coherente basado en textos de referencia (por ejemplo, comunicados creados por una líder de comunicaciones).

El sistema debe permitir **retroalimentación directa** del usuario sobre la calidad de los textos generados, para mejorar progresivamente las recomendaciones y mantener una base de datos limpia y relevante.

---

## 🧩 Funcionalidades Principales

### 1️⃣ Módulos principales
- 📝 **Generar** → Crea nuevos textos a partir de un prompt o tema.  
- ✏️ **Corregir** → Mejora redacción, ortografía y estilo.  
- 🔍 **Resumir** → Condensa textos con control de longitud.

### 2️⃣ Configuraciones accesibles al usuario
- Seleccionar acción: *Generar*, *Corregir* o *Resumir*  
- Definir cantidad de palabras y temperatura  
- Subir archivos `.txt` o `.json` de referencia  
- Descargar resultados en `.txt` o `.json`  
- Consultar historial mensual  
- **Evaluar resultados**: *“Me gusta / No me gusta”* o *“Guardar / Descartar”*

---

## 💾 Almacenamiento y Organización de Datos

### Estructura de Carpetas
```
/data/
└── resultados/
    ├── 2025-01.json
    ├── 2025-02.json
    └── ...
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

- 👍 “Me gusta” → Se guarda como aprobado y sirve de referencia futura  
- 👎 “No me gusta” → Se marca como rechazado y puede eliminarse  
- ✍️ Comentario opcional sobre el resultado

Los textos aprobados alimentan un **corpus interno** para mejorar el estilo.  
Los rechazados se guardan aparte o se descartan.

---

## ⚙️ Tecnologías

- **Frontend:** Streamlit  
- **Framework IA:** LangChain  
- **Proveedores de IA:** OpenAI y Google Gemini
- **Modelos OpenAI:** GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- **Modelos Gemini:** Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini Pro
- **Embeddings:** OpenAI / HuggingFace (futuro)
- **Persistencia:** Archivos JSON mensuales  
- **Procesamiento:** Pandas / SQLite (opcional)

---

## 🧱 Estructura de Código

```
/app/
├── main.py
├── components/
│   ├── sidebar.py
│   ├── result_display.py
│   └── uploader.py
├── utils/
│   ├── io_manager.py
│   ├── feedback_manager.py
│   ├── text_tools.py
│   └── langchain_agent.py
└── data/
    ├── resultados/
    └── rechazados/
```

---

## 🌐 Flujo del Usuario

1. El usuario abre la app Streamlit  
2. Selecciona una acción (Generar / Corregir / Resumir)  
3. Configura longitud y creatividad  
4. (Opcional) Sube textos base  
5. El sistema genera o corrige el texto  
6. El usuario lo evalúa (Me gusta / No me gusta / Comenta)  
7. Se guarda automáticamente con su feedback

---

## 🔒 Futuras Mejoras

- Dashboard de métricas  
- Filtros por tono, tema o fecha  
- Sugerencias automáticas según feedback  
- Entrenamiento semántico con textos aprobados  

---

## ✅ Resumen Final

> Crear un chatbot empresarial configurable con Streamlit + LangChain, capaz de **generar, corregir y resumir textos** en el estilo de una líder de comunicaciones.  
> Soporta **múltiples proveedores de IA** (OpenAI y Google Gemini) con selector de modelo integrado.  
> Los datos se almacenan en **JSON mensuales**, con retroalimentación del usuario para limpiar y mejorar continuamente la base.

