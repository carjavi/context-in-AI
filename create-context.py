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