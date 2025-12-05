# 📋 Configuración de la Empresa

Este directorio contiene el archivo de configuración con la información de la empresa que se utiliza para alinear todos los textos generados.

## 📁 Archivo de Configuración

El archivo `empresa_config.json` contiene toda la información relevante de la empresa que se incluye automáticamente en los prompts de generación de textos.

## 🔧 Personalización

Puedes editar el archivo `empresa_config.json` para personalizar la información de tu empresa. El archivo incluye las siguientes secciones:

### Estructura del Archivo

```json
{
  "nombre_empresa": "Nombre de tu empresa",
  "sector": "Sector al que pertenece",
  "descripcion": "Descripción breve de la empresa",
  
  "mision": "Misión de la empresa",
  "vision": "Visión de la empresa",
  
  "valores": [
    "Valor 1: Descripción",
    "Valor 2: Descripción"
  ],
  
  "tono_comunicacion": {
    "estilo": "Estilo de comunicación deseado",
    "caracteristicas": [
      "Característica 1",
      "Característica 2"
    ]
  },
  
  "contexto_adicional": {
    "servicios_principales": [
      "Servicio 1",
      "Servicio 2"
    ],
    "puntos_destacados": [
      "Punto destacado 1",
      "Punto destacado 2"
    ],
    "enfoque": "Enfoque o filosofía de la empresa"
  },
  
  "palabras_clave": [
    "palabra1",
    "palabra2"
  ],
  
  "mensajes_frecuentes": [
    "Mensaje frecuente 1",
    "Mensaje frecuente 2"
  ]
}
```

## 📝 Cómo Editar

1. Abre el archivo `empresa_config.json` en un editor de texto
2. Modifica los campos según la información de tu empresa
3. Guarda el archivo
4. La aplicación cargará automáticamente los cambios la próxima vez que se ejecute

## ✅ Campos Requeridos vs Opcionales

Todos los campos son opcionales, pero se recomienda completar al menos:
- `nombre_empresa`
- `descripcion`
- `valores`
- `tono_comunicacion`

## 🎯 Uso en la Aplicación

La información de este archivo se incluye automáticamente en:
- ✅ Generación de textos nuevos
- ✅ Corrección de textos existentes
- ✅ Resumen de textos

Esto asegura que todos los textos generados estén alineados con la identidad, valores y tono de comunicación de la empresa.

## 💡 Ejemplo: Casa Limpia

El archivo viene pre-configurado con información de ejemplo de "Casa Limpia", una empresa de servicios de limpieza. Puedes usar este ejemplo como base y modificarlo según tus necesidades.

## 🔄 Recarga de Configuración

La configuración se carga automáticamente al iniciar la aplicación. Si modificas el archivo mientras la aplicación está en ejecución, reinicia la aplicación para que los cambios surtan efecto.

