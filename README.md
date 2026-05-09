<p align="center"><img src="./img/context-ai.png" width="800"   alt=" " /></p>
<h1 align="center"> Context in AI </h1> 
<h4 align="right">May 26</h4>

<p>
  <img src="https://img.shields.io/badge/OS-Linux%20GNU-yellowgreen">
  <img src="https://img.shields.io/badge/OS-Windows%2011-blue">
</p>

<br>

# Table of contents
- [Table of contents](#table-of-contents)
- [How to pass context to AI](#how-to-pass-context-to-ai)
- [OpenCode + context for AI agents](#opencode--context-for-ai-agents)
  - [AGENTS.MD en los Chat LLM](#agentsmd-en-los-chat-llm)

<br>

En IA, el contexto se refiere a la información a la que un sistema de inteligencia artificial puede acceder, comprender y utilizar para generar respuestas relevantes durante una interacción. Una de las mejores formas de obtener respuestas precisas, resúmenes personalizados y análisis profundos.

<br>

# How to pass context to AI
Los documentos y fuentes deben agregarse a un directorio llamado ```context``` en la raiz de mi proyecto idealmente en texto plano como ***Markdowns***.

<br>

# OpenCode + context for AI agents
```AGENTS.md``` es básicamente un archivo de instrucciones/contexto persistente para el LLM que trabaja sobre tu proyecto.

Le dice cosas como:
* cómo debe programar
* qué arquitectura usar
* qué librerías preferir
* qué evitar
* cómo responder
* cómo organizar el código
* cómo compilar
* cómo testear
* estándares del proyecto
* restricciones hardware
* estilo de commits
* convenciones

Es como un “system prompt local del proyecto”.

En OpenCode normalmente no necesitas “decirle” manualmente a la AI que use AGENTS.md.
Si el archivo está en la raíz del proyecto, OpenCode lo detecta automáticamente y lo inyecta como contexto al agente. Pero en algunos casos conviene reforzarlo explícitamente:  ```usa las reglas definidas en AGENTS.md ``` porque algunos modelos pequeños o proveedores externos pueden ignorar parte del contexto.

<br>

## AGENTS.MD en los Chat LLM
En ChatGPT, Gemini, Claude, etc. que corren en navegador, normalmente debes subir el archivo manualmente o copiar el contenido al chat.
Por eso en navegador el AGENTS.md funciona más como: ***contexto manual reusable***, mientras que en OpenCode es:
* Contexto automático del proyecto.
* Persistente.
* Integrado al workflow del agente.

> :bulb: **Tip:** En los Chat enorme (muchas horas/días)
> Puede degradarse el contexto.
> Ahí convine:
* Re-subir el archivo
* Resumir reglas críticas
* Abrir un chat nuevo

> :bulb: **Tip:** OpenCode también puede usar otros archivos
> Muchos agentes toman contexto de:
* README.md
* docs/
* comentarios del código
* .cursorrules
* .github/copilot-instructions.md
depende del proveedor/modelo.

<br>

AGENTS.md
```bash
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

```

<br>

---

<div>
  <p>
    <img  align="top" width="42" style="padding:0px 0px 0px 0px;" src="./img/carjavi.png"/> Copyright &nbsp;&copy; 2023 Instinto Digital <a href="https://carjavi.github.io/" title="carjavi.github">carjavi</a>
  </p>
</div>

<p align="center">
    <a href="https://instintodigital.net/" target="_blank"><img src="./img/developer.png" height="100" alt="www.instintodigital.net"></a>
</p>



