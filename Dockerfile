# Dockerfile optimizado para Railway
# Usa imagen base ligera de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (mínimas)
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements.txt primero (para cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Crear directorios necesarios para datos
RUN mkdir -p data/resultados data/rechazados data/archivos_referencia

# Exponer el puerto que Railway asignará
ENV PORT=8501

# Comando para ejecutar Streamlit
# Railway proporciona la variable $PORT
CMD streamlit run streamlit_app.py --server.port=${PORT} --server.address=0.0.0.0

