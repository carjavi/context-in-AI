# AGENTS.md

# Perfil del proyecto

## Proyecto orientado a:
- Desarrollo Fullstack
- Sistemas embebidos
- Automatización
- Electrónica
- APIs y servicios cloud
- Electrónica

## Stack principal:
- Javascript / NodeJs
- Python
- C++
- C
- FreeRTOS
- Arduino IDE
- Docker

## Desarrollo firmware profesional para:
- ESP32 S3, C6, C3
- STM32 
- Raspberry Pi 5, 4, 3, Zero, Pico

## Sistemas Operativos 
- Windows 11
- Ubuntu GNU/Linux 
- Raspbian
- FreeRTOS

---

# Reglas generales
- Todas las variables y funciones deben incluir un bloque de comentario JSDoc / Docstrings o Doxygen encima dependiendo su usamos Javascript/ Python / C o C++
- Lee todos los archivos .md dentro del directorio context para que tus respuestas esten basadas en mis fuentes ya investigadas, sino lo que pregunto no esta alli siente libre de buscar en internet.
- Priorizar código simple y mantenible.
- No usar dependencias innecesarias.
- Explicar decisiones técnicas importantes.
- Preferir soluciones offline/local-first.
- Siempre manejar errores y timeouts.
- Verificar el uso de librerias actualizadas
- Suguerir alternativas fuera del agents.md si hay muchos errores o hay muchas interacciones sin resultados.
- Código reutilizable.
- Modularidad.
- Fácil debugging.
- Máximo 1 responsabilidad por módulo.
- Evitar duplicación.

# Reglas obligatorias
- No inventar información técnica.
- Si faltan datos:
  - preguntar
  - asumir explícitamente
- Explicar riesgos técnicos.
- Priorizar estabilidad sobre complejidad.

---

# Estándares por lenguaje

## Python
- Priorizar la última versión de Python 
- Toda API debe tener timeout.

### Reglas Python
- Usar type hints.
- Preferir async cuando aplique.
- Separar:
  - services
  - models
  - api
  - utils

### APIs
Framework:
- FastAPI
Toda API debe incluir:
- OpenAPI
- validación Pydantic
- manejo global de errores
- autenticación JWT

### Logs
Usar logging estructurado JSON.
Incluir:
- timestamp
- nivel
- módulo
- request_id

### Automatización
Soportar:
- Modbus TCP
- MQTT
- Serial RS485
Toda comunicación:
- retry
- timeout
- watchdog

---

## C++
- Usar C++17 mínimo.
- Documentar ISR y tareas críticas.

---

## Javascript
- Usar async/await.
- No usar callbacks antiguos.
- Mantener separación:
  - UI
  - lógica
  - acceso a datos
- Priorizar la última versión de NodeJS

---

# Sistemas Embebidos
- Prioridad a bajo consumo.
- No bloquear tareas FreeRTOS.
- Toda tarea debe tener watchdog strategy.
- Separar:
  - drivers
  - HAL
  - lógica de aplicación

## Reglas FreeRTOS
- No usar delay bloqueante.
- Usar:
  - queues
  - semaphores
  - event groups
- Toda tarea:
  - stack definida
  - prioridad justificada
  - timeout definido

### Memoria
- Minimizar heap fragmentation.
- No usar malloc.
- Preferir buffers estáticos.
- Monitorear:
  - heap
  - stack watermark

### Logging
Usar niveles:
- ERROR
- WARN
- INFO
- DEBUG
No imprimir dentro de ISR.

### Hardware
Documentar:
- pines
- voltajes
- protocolos
- timing crítico

### Protocolos
Soportados:
- UART
- SPI
- I2C
- CAN
- RS485
- Modbus
- LoRaWAN
- MQTT

### Testing
Todo driver debe tener:
- test funcional
- test de timeout
- test de reconexión

---

# APIs
- Preferir REST JSON.
- Toda API:
  - retry
  - timeout
  - logging
  - manejo de errores
- Nunca hardcodear API keys.

---

# Documentación
Toda función pública debe tener:
- descripción
- parámetros
- retorno
- ejemplo de uso

---

# Seguridad
- Nunca subir secretos.
- Nunca hardcodear secretos.
- Validar input externo.
- Sanitizar datos seriales y MQTT.
- Sanitizar JSON externo.

---

# Docker
Todos los servicios deben poder correr en Docker.

---

# Electrónica
Siempre considerar:
- niveles lógicos
- consumo
- ruido eléctrico
- protección ESD
- fuentes de alimentación

## Comunicación
Protocolos frecuentes:
- MQTT
- BLE
- WiFi
- LoRa
- UART

---

# UI
Frontend:
- React
- WebSerial
- WebSocket
Backend:
- Nodejs