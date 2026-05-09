# AGENTS RULES

# Perfil del Proyecto

## Áreas principales
- Desarrollo Fullstack
- Sistemas embebidos
- Automatización industrial
- Electrónica
- APIs y servicios cloud

## Stack principal
- Python
- JavaScript / Node.js
- C / C++
- FreeRTOS
- Arduino IDE
- Docker

## Hardware objetivo
- ESP32 (S3, C6, C3)
- STM32
- Raspberry Pi (5, 4, 3, Zero, Pico)

---

# Reglas Generales

- Priorizar código simple, mantenible y reutilizable.
- Mantener arquitectura modular.
- Cada módulo debe tener una sola responsabilidad.
- Evitar duplicación de código.
- No usar dependencias innecesarias.
- Priorizar soluciones offline/local-first.
- Siempre manejar:
  - errores
  - retries
  - timeouts
- Explicar decisiones técnicas importantes.
- Verificar que las librerías utilizadas estén actualizadas y mantenidas.
- Si el contexto no es suficiente:
  - leer todos los archivos `.md` dentro del directorio `context`
  - luego buscar información externa si es necesario
- Si existen demasiados errores o iteraciones sin resultados:
  - sugerir alternativas técnicas fuera del enfoque actual

---

# Convenciones de Código

- Todas las variables y funciones deben:
  - escribirse en inglés
  - usar `snake_case`
- No usar `camelCase`.

## Documentación obligatoria

Toda función, método, clase, estructura o variable importante debe incluir documentación usando el estándar correspondiente:

| Lenguaje | Estándar |
|---|---|
| JavaScript / TypeScript | JSDoc |
| Python | Docstrings |
| C / C++ | Doxygen |

### Requisitos mínimos

Toda función pública debe documentar:
- descripción
- parámetros
- retorno
- errores relevantes
- ejemplo de uso cuando aplique

También deben documentarse:
- variables globales
- constantes
- configuraciones
- GPIO
- buffers importantes
- ISR
- callbacks
- threads
- interfaces
- templates genéricos

### Reglas de documentación

- La documentación debe ubicarse encima de la declaración.
- Mantener comentarios técnicos y útiles.
- Evitar comentarios redundantes o triviales.
- Si cambia el comportamiento del código:
  - actualizar automáticamente la documentación.

---

# Metadata y Versionado

Todo archivo generado o modificado debe incluir un bloque de metadata al inicio absoluto del archivo.

## Campos obligatorios

- Descripción breve del script (máximo 2 líneas)
- `@author`
- `@date`
- `@copyright`
- `@version`
- `@library`

## Formato requerido

### Autor
```text
@author: Carlos Briceño <carjavi@hotmail.com>
```

### Fecha
Formato:
```text
dd-mm-aaaa
```

### Copyright
```text
@copyright: Copyright (c) 2026 www.carjavi.com
```

### Versionado
Usar versionado incremental:
- `V1.0` → versión inicial
- `V1.1` → mejoras menores
- `V2.0` → cambios importantes

Actualizar automáticamente:
- `@version`
- `@date`

cuando el archivo sea modificado.

### Librerías
- Detectar automáticamente dependencias externas.
- Incluir comandos reales de instalación.
- No incluir librerías no utilizadas.

Ejemplo:
```text
@library:
- pip install pyserial
- npm install mqtt
```

Si no existen dependencias:
```text
@library: No external dependencies
```

## Comentarios por lenguaje

| Lenguaje | Formato |
|---|---|
| Python / Shell / YAML | `#` |
| JS / TS / C / C++ / Java | `//` o `/** */` |
| HTML / XML | `<!-- -->` |
| SQL / Lua | `--` |

---

# Estándares por Lenguaje

## Python

- Priorizar la última versión estable de Python.
- Usar type hints.
- Preferir `async`/`await` cuando aplique.
- Toda API debe incluir timeout.
- Logging estructurado JSON con:
  - timestamp
  - nivel
  - módulo
  - request_id

### Arquitectura recomendada
Separar:
- services
- models
- api
- utils

### APIs
Framework preferido:
- FastAPI

Toda API debe incluir:
- OpenAPI
- validación Pydantic
- manejo global de errores
- autenticación JWT

### Automatización y comunicaciones
Soportar:
- MQTT
- Modbus TCP
- RS485

Toda comunicación debe manejar:
- retry
- timeout
- watchdog

---

## JavaScript / Node.js

- Priorizar la última versión LTS de Node.js.
- Usar `async/await`.
- No usar callbacks legacy.
- Separar:
  - UI
  - lógica
  - acceso a datos

---

## C / C++

- Usar mínimo:
  - C++17
- Documentar ISR y tareas críticas.
- Priorizar bajo consumo y estabilidad.
- Evitar asignación dinámica innecesaria.

---

# Sistemas Embebidos

## FreeRTOS

- No usar delays bloqueantes.
- Usar:
  - queues
  - semaphores
  - event groups

Toda tarea debe definir:
- stack
- prioridad
- timeout

## Memoria

- Minimizar fragmentación del heap.
- Evitar `malloc` cuando sea posible.
- Preferir buffers estáticos.
- Monitorear:
  - heap
  - stack watermark

## Logging

Usar niveles:
- ERROR
- WARN
- INFO
- DEBUG

No imprimir dentro de ISR.

## Hardware

Siempre documentar:
- GPIO
- voltajes
- protocolos
- timing crítico

Considerar:
- ruido eléctrico
- consumo
- protección ESD
- fuentes de alimentación

## Protocolos frecuentes

- UART
- SPI
- I2C
- CAN
- RS485
- Modbus
- MQTT
- BLE
- WiFi
- LoRa / LoRaWAN

## Testing

Todo driver debe incluir:
- test funcional
- test de timeout
- test de reconexión

---

# APIs y Seguridad

## APIs

- Preferir REST JSON.
- Nunca hardcodear API keys.
- Toda API debe manejar:
  - retry
  - timeout
  - logging
  - errores

## Seguridad

- Nunca subir secretos al repositorio.
- Nunca hardcodear secretos.
- Validar y sanitizar:
  - JSON externo
  - datos seriales
  - payloads MQTT
  - input del usuario

---

# Docker

Todos los servicios deben poder ejecutarse en Docker.

---

# UI

## Frontend
- React
- WebSerial
- WebSocket

## Backend
- Node.js

---

# Investigación y Referencias

- Antes de generar ejemplos de código, revisar primero:
  - documentación interna ubicada en el directorio `context`
  - ejemplos existentes del proyecto
  - patrones ya utilizados en el código base

- Si la información no existe o es insuficiente:
  - buscar proyectos similares en:
    - GitHub
    - documentación oficial
    - repositorios open source relevantes
    - ejemplos oficiales de librerías/frameworks

- Priorizar referencias:
  - mantenidas recientemente
  - con buena documentación
  - con arquitectura limpia
  - usadas ampliamente por la comunidad
  - compatibles con el stack del proyecto

- Al generar ejemplos complejos o arquitecturas nuevas:
  - incluir una sección final llamada `Referencias`
  - agregar links relevantes utilizados como inspiración técnica

## Formato de referencias

```text
Referencias:
- https://github.com/espressif/esp-idf
- https://github.com/micropython/micropython
- https://github.com/fastapi/fastapi
```

## Reglas adicionales

- Usar referencias como guía técnica o arquitectónica.
- Adaptar siempre el código al contexto del proyecto actual.
- Priorizar documentación oficial sobre blogs externos.
- Si existen múltiples enfoques:
  - explicar brevemente ventajas y desventajas.
- Cuando sea posible:
  - indicar cuál referencia es la más recomendable.