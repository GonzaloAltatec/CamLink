# Guía generada por IA (Revisar y poner en común)

# Guía de Contribución para CamLink

¡Gracias por tu interés en contribuir a CamLink! Esta guía te ayudará a entender cómo puedes ayudar a mejorar el proyecto.

## Tabla de Contenidos
- [Cómo Contribuir](#cómo-contribuir)
- [Flujo de Trabajo](#flujo-de-trabajo)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Guía de Código](#guía-de-código)
- [Testing](#testing)
- [Documentación](#documentación)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## Cómo Contribuir

1. **Reportar Bugs**
   - Usa la plantilla de reporte de bugs
   - Incluye pasos para reproducir el problema
   - Indica la versión del dispositivo afectado

2. **Solicitar Nuevas Funcionalidades**
   - Usa la plantilla de solicitud de características
   - Describe claramente la funcionalidad deseada
   - Explica cómo se beneficiaría el proyecto

3. **Enviar Pull Requests**
   - Crea una rama para tu feature/fix
   - Asegúrate de que los tests pasen
   - Documenta tu código
   - Actualiza la documentación relevante

## Flujo de Trabajo

1. **Configuración del Entorno**
   ```bash
   # Clonar el repositorio
   git clone https://github.com/GonzaloAltatec/CamLink.git
   cd CamLink

   # Crear entorno virtual
   python -m venv venv
   source venv/bin/activate
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

2. **Desarrollo**
   - Usa ramas descriptivas: `feature/nombre-feature` o `fix/numero-issue`
   - Realiza commits pequeños y descriptivos
   - Usa mensajes de commit en inglés

## Estructura del Proyecto

```
CamLink/
├── src/
│   ├── routers/            # Endpoints de la API
│   │   ├── configurator.py # Configuración de dispositivos
│   │   ├── reviser.py     # Revisión de dispositivos
│   │   ├── erp.py         # Integración con ERP
│   │   ├── health.py      # Monitoreo de salud
│   │   └── info.py        # Información del sistema
│   ├── utils/            # Utilidades y operaciones
│   │   ├── db/           # Modelos y esquemas de base de datos
│   │   ├── exceptions/   # Manejo de excepciones
│   │   └── operations/   # Operaciones con dispositivos
│   └── main.py           # Punto de entrada de la aplicación
├── tests/                # Pruebas unitarias
├── docker/               # Configuración de Docker
└── docs/                 # Documentación
```

## Guía de Código

1. **Convenciones de Código**
   - Sigue PEP 8 para estilo de código
   - Usa type hints
   - Documenta funciones y clases con docstrings
   - Mantén una consistencia en el manejo de errores

2. **Manejo de Errores**
   - Usa excepciones personalizadas para errores específicos
   - Implementa logging para errores y eventos importantes
   - Maneja timeouts y errores de conexión

## Testing

1. **Escribir Tests**
   - Crea tests unitarios para nuevas funcionalidades
   - Usa mocks para dependencias externas
   - Prueba casos de error

2. **Ejecutar Tests**
   ```bash
   pytest
   ```

## Documentación

1. **Documentar Código**
   - Usa docstrings para funciones y clases
   - Documenta parámetros y returns
   - Explica lógica compleja

2. **Actualizar Documentación**
   - Actualiza el README.md
   - Documenta nuevas funcionalidades
   - Mantén la documentación actualizada

## Preguntas Frecuentes

### ¿Cómo puedo agregar soporte para un nuevo modelo de cámara?
1. Crea una nueva clase en `src/utils/operations/` que herede de la clase base
2. Implementa los métodos específicos del modelo
3. Actualiza la documentación
4. Agrega tests para el nuevo modelo

### ¿Cómo puedo contribuir a la documentación?
- Mejora la documentación existente
- Agrega ejemplos de uso
- Documenta nuevas funcionalidades
- Corrige errores en la documentación

### ¿Cómo puedo reportar un problema?
1. Busca si el problema ya existe
2. Usa la plantilla de reporte de bugs
3. Proporciona información detallada
4. Incluye logs si es posible

## Código de Conducta

Este proyecto sigue el [Código de Conducta de Contributor Covenant](CODE_OF_CONDUCT.md). Por favor, asegúrate de seguirlo en todas tus interacciones con el proyecto.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
