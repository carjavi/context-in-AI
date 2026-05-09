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
  - [Markitdown](#markitdown)
    - [¿Por qué Markdown?](#por-qué-markdown)
  - [Markitdown + OCR local (OFFLINE)](#markitdown--ocr-local-offline)
    - [Features](#features)
    - [Install Project:](#install-project)
  - [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Links](#links)
- [OpenCode + context for AI agents](#opencode--context-for-ai-agents)
  - [AGENTS.MD en los Chat LLM](#agentsmd-en-los-chat-llm)

<br>

En IA, el contexto se refiere a la información a la que un sistema de inteligencia artificial puede acceder, comprender y utilizar para generar respuestas relevantes durante una interacción. Una de las mejores formas de obtener respuestas precisas, resúmenes personalizados y análisis profundos.

<br>

# How to pass context to AI
Los documentos y fuentes deben agregarse a un directorio llamado ```context``` en la raiz de mi proyecto idealmente en texto plano como ***Markdowns***.

## Markitdown
Es una herramienta Python que convierte documentos a Markdown (.md). Para alimentar con contexto (documentos) a la AI con y ahorrar tokens en las AI pagas. ¿Cómo? la idea seria generar documentos planos con Markitdown + (OCR IA)/(OCR local) para alimentar la AI pagas y ahorrar tokens.

Soporta: ```PDF | Documentos Office | Excel | PowerPoint | HTML | JSON / CSV / XML | imágenes con OCR | audio con transcripción | YouTube | EPUB |```

Está pensada para usar documentos con LLMs/IA.

### ¿Por qué Markdown?
Markdown es extremadamente similar al texto plano, con un mínimo de formato o marcado, pero aun así permite representar la estructura importante de un documento. Las convenciones de Markdown son muy eficientes en cuanto al uso de tokens.

MarkItDown es bueno para pipelines IA porque:
* preserva tablas y títulos mejor que muchos extractores
* genera markdown limpio
* es liviano
* funciona bien con RAG y embeddings
  
Pero:
* NO preserva diseño visual
* NO reemplaza OCR profesional
* PDFs complejos pueden romperse
* para documentos difíciles, a veces docling o pandoc funcionan mejor

<br>

## Markitdown + OCR local (OFFLINE)
Con este proyecto vamos a poder convertir cualquier documento a .md para darle contexto a la AI. 
* Se usar tesseract + ghostscript + ocrmypdf
* Se generar un PDF con OCR
* Luego convertirlo con markitdown a .md

### Features  
* Directorio de entrada de documento: ```documents```
* Directorio de Salida: ```markdowns```
* Comando Python: ```create-context.py```

### Install Project:

1. Instalar ```Tesseract``` de "https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe"
   
> :memo: **Note:** Durante la instalación hay que instalar tambien los idiomas "español/ingles"

<p align="center"><img src="./img/ocr1.png" width="400" alt=" " /></p>

<p align="center"><img src="./img/ocr.png" width="400" alt=" " /></p>


Agregar al PATH de Windows. Usar Powershell como administrador:
```PowerShell
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\Program Files\Tesseract-OCR",
    "Machine"
)
```
Verificar con:
```bash
tesseract --version	# Verificar Tesseract en una nueva ventana
```
> :memo: **Note:** 
> * Tal vez necesite reiniciar
> * Verificar idiomas en ***C:\Program Files\Tesseract-OCR\tessdata*** deberian estar ```spa.traineddata``` & ```eng.traineddata```

<br>

2. Descargar ```Ghostscript``` (gs10070w64.exe) de :https://github.com/ArtifexSoftware/ghostpdl-downloads/releases
   
Agregar al Path de windows. Correr PowerShell como administrador
```PowerShell
# C:\Program Files\gs\gs10.07.0\bin
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\Program Files\gs\gs10.07.0\bin",
    "Machine"
)
```
Verificar con:
```bash
gswin64c --version	# en una nueva ventana
```
> :memo: **Note:** Tal vez necesite reiniciar.

<br>

3. Instalación del entorno virtual y librerias
```Python
python3 -m venv venv    # Crear un entorno virtual llamado venv
source venv/Scripts/activate
pip install ocrmypdf 	# Se instala en el entorno virtual, no se necesita agregar al path de windows
pip install "markitdown[all]"  # Install markitdown [all]Instala todas las dependencias opcionales.
pip install markitdown-ocr  # Plugin markitdown-ocr complemento añade compatibilidad con OCR a los convertidores de PDF, DOCX, PPTX y XLSX, extrayendo texto de imágenes incrustadas mediante LLM Vision
```
verificar con:
```bash
ocrmypdf --version
```

<br>

```create-context.py```
```Python
from pathlib import Path
from markitdown import MarkItDown
import subprocess
import tempfile
import shutil
import argparse
import time
import sys

# =========================================================
# ARGUMENTOS
# =========================================================

parser = argparse.ArgumentParser()

parser.add_argument(
    "--verbose",
    action="store_true",
    help="Mostrar logs detallados"
)

args = parser.parse_args()

VERBOSE = args.verbose

# =========================================================
# CONFIG
# =========================================================

INPUT_DIR = Path("documents")
OUTPUT_DIR = Path("markdowns")

OCR_LANGS = "spa+eng"

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".doc",
    ".xlsx",
    ".xls",
    ".pptx",
    ".ppt",
    ".epub",
    ".html",
    ".htm",
    ".csv",
    ".xml",
    ".json",
    ".txt",
    ".rtf",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
}

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
}

INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

md = MarkItDown(enable_plugins=True)

# =========================================================
# LOGGING
# =========================================================

def log(message):

    if VERBOSE:
        print(message)

# =========================================================
# BARRA PROGRESO
# =========================================================

def progress(current, total, filename):

    if VERBOSE:
        return

    percent = int((current / total) * 100)

    bar_length = 30
    filled = int(bar_length * current // total)

    bar = "█" * filled + "-" * (bar_length - filled)

    sys.stdout.write(
        f"\r[{bar}] {percent}% | {current}/{total} | {filename[:40]}"
    )

    sys.stdout.flush()

# =========================================================
# OCR PDF
# =========================================================

def apply_ocr_to_pdf(input_pdf: Path, output_pdf: Path):

    command = [
    "ocrmypdf",

    "-l", OCR_LANGS,

    "--skip-text",

    "--rotate-pages",
    "--deskew",

    "--optimize", "1",

    str(input_pdf),
    str(output_pdf)
    ]

    if VERBOSE:
        subprocess.run(command, check=True)

    else:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

# =========================================================
# IMAGEN -> PDF
# =========================================================

def image_to_pdf(image_path: Path, output_pdf: Path):

    from PIL import Image

    image = Image.open(image_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    image.save(output_pdf, "PDF")

# =========================================================
# BUSCAR ARCHIVOS
# =========================================================

files = [
    f for f in INPUT_DIR.iterdir()
    if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
]

if not files:

    print("[INFO] No se encontraron documentos")
    exit()

print(f"[INFO] Archivos encontrados: {len(files)}")

# =========================================================
# PROCESAMIENTO
# =========================================================

start_time = time.time()

errors = []

for index, file_path in enumerate(files, start=1):

    try:

        progress(index, len(files), file_path.name)

        extension = file_path.suffix.lower()

        result = None

        # =================================================
        # PDFs
        # =================================================

        if extension == ".pdf":

            log(f"\n[INFO] OCR PDF: {file_path.name}")

            temp_dir = Path(tempfile.mkdtemp())

            ocr_pdf = temp_dir / f"{file_path.stem}_ocr.pdf"

            apply_ocr_to_pdf(file_path, ocr_pdf)

            result = md.convert(str(ocr_pdf))

            shutil.rmtree(temp_dir)

        # =================================================
        # IMAGENES
        # =================================================

        elif extension in IMAGE_EXTENSIONS:

            log(f"\n[INFO] OCR Imagen: {file_path.name}")

            temp_dir = Path(tempfile.mkdtemp())

            image_pdf = temp_dir / f"{file_path.stem}.pdf"

            ocr_pdf = temp_dir / f"{file_path.stem}_ocr.pdf"

            image_to_pdf(file_path, image_pdf)

            apply_ocr_to_pdf(image_pdf, ocr_pdf)

            result = md.convert(str(ocr_pdf))

            shutil.rmtree(temp_dir)

        # =================================================
        # OTROS
        # =================================================

        else:

            log(f"\n[INFO] Documento: {file_path.name}")

            result = md.convert(str(file_path))

        # =================================================
        # GUARDAR
        # =================================================

        output_md = OUTPUT_DIR / f"{file_path.stem}.md"

        with open(output_md, "w", encoding="utf-8") as f:
            f.write(result.text_content)

        log(f"[OK] {output_md.name}")

    except Exception as e:

        errors.append((file_path.name, str(e)))

        if VERBOSE:
            print(f"[ERROR] {file_path.name}")
            print(e)

# =========================================================
# FINAL
# =========================================================

elapsed = round(time.time() - start_time, 2)

print("\n")

print(f"[INFO] Finalizado en {elapsed}s")

print(f"[INFO] Procesados: {len(files)}")

print(f"[INFO] Errores: {len(errors)}")

if errors:

    print("\n[ERRORS]")

    for filename, error in errors:
        print(f"- {filename}")
```
## Usage
Metemos todos los documentos en el directorio de entrada ```documents``` y al correr el Script se convertiran ***.md*** en el directorio de salida ```markdowns```
```bash
python create-context.py
python create-context.py --verbose  # muestra el proceso de la conversion 
```

> :warning: **Warning:** Cada vez que entres en terminal para correr el script se debe activar el entorno virtual.

<br>

# Troubleshooting
En Windows a veces falla con PDFs. Instala esto si tienes problemas:
```bash
pip install pymupdf pdfminer.six
```
# Links
Repositorio oficial: https://github.com/microsoft/markitdown

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

> :bulb: **Tip:** En los Chats enormes (muchas horas/días) puede degradarse el contexto. Ahí convine:
* Re-subir el archivo
* Resumir reglas críticas
* Abrir un chat nuevo

> :bulb: **Tip:** OpenCode también puede usar otros archivos.
> Muchos agentes toman contexto de:
* README.md
* docs/
* comentarios del código
* .cursorrules
* .github/copilot-instructions.md
  
depende del proveedor/modelo.

<br>

AGENTS.md
```PowerShell
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



