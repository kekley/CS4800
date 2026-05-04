from __future__ import annotations

import datetime
import os
import fitz
from PIL import Image
import pytesseract
from docx import Document


from constants import (
    MAX_EXTRACTED_TEXT_CHARS,
    OCR_MAX_PDF_PAGES,
    OCR_PDF_RENDER_DPI,
    OCR_TESSERACT_TIMEOUT_SECONDS,
)

TEXT_MIME_TYPES = {
    "application/json",
    "text/csv",
    "text/markdown",
    "text/plain",
}

DOCX_MIME_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


class UnsupportedExtractionType(Exception):
    pass


def extract_attachment_text(file_path: str, mime_type: str, file_name: str):
    try:
        text = extract_text(file_path, mime_type, file_name)
        text = normalize_text(text)
        text = limit_text(text)

        if not text:
            status = "no_text"
        else:
            status = "extracted"

        return {
            "status": status,
            "text": text or None,
            "error": None,
            "extracted_at": datetime.datetime.now(),
        }
    except UnsupportedExtractionType as error:
        return {
            "status": "unsupported",
            "text": None,
            "error": str(error),
            "extracted_at": datetime.datetime.now(),
        }
    except Exception as error:
        return {
            "status": "failed",
            "text": None,
            "error": str(error)[:1000],
            "extracted_at": datetime.datetime.now(),
        }


def extract_text(file_path: str, mime_type: str, file_name: str):
    extension = os.path.splitext(file_name)[1].lower()

    if mime_type in TEXT_MIME_TYPES or extension in {".csv", ".json", ".md", ".txt"}:
        return extract_plaintext(file_path)

    if mime_type.startswith("image/"):
        return ocr_image(file_path)

    if mime_type == "application/pdf" or extension == ".pdf":
        return extract_pdf_text(file_path)

    if mime_type == DOCX_MIME_TYPE or extension == ".docx":
        return extract_docx_text(file_path)

    raise UnsupportedExtractionType(f"Text extraction is not supported for {mime_type}")


def extract_plaintext(file_path: str):
    with open(file_path, "rb") as file:
        data = file.read(MAX_EXTRACTED_TEXT_CHARS * 4)

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="replace")


def ocr_image(file_path: str):

    with Image.open(file_path) as image:
        return pytesseract.image_to_string(
            image,
            timeout=OCR_TESSERACT_TIMEOUT_SECONDS,
        )


def extract_pdf_text(file_path: str):

    chunks = []
    with fitz.open(file_path) as document:
        page_count = min(document.page_count, OCR_MAX_PDF_PAGES)
        zoom = OCR_PDF_RENDER_DPI / 72
        matrix = fitz.Matrix(zoom, zoom)

        for page_index in range(page_count):
            page = document.load_page(page_index)
            text = normalize_text(page.get_text("text"))

            if len(text) < 40:
                pixmap = page.get_pixmap(matrix=matrix, alpha=False)
                image = Image.frombytes(
                    "RGB",
                    [pixmap.width, pixmap.height],
                    pixmap.samples,
                )
                text = pytesseract.image_to_string(
                    image,
                    timeout=OCR_TESSERACT_TIMEOUT_SECONDS,
                )

            if text:
                chunks.append(f"[Page {page_index + 1}]\n{text}")

        if document.page_count > OCR_MAX_PDF_PAGES:
            chunks.append(f"[Only the first {OCR_MAX_PDF_PAGES} pages were processed.]")

    return "\n\n".join(chunks)


def extract_docx_text(file_path: str):
    document = Document(file_path)
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()
    )


def normalize_text(text):
    if not text:
        return ""

    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()


def limit_text(text):
    if len(text) <= MAX_EXTRACTED_TEXT_CHARS:
        return text

    truncated = text[:MAX_EXTRACTED_TEXT_CHARS].rstrip()
    return f"{truncated}\n\n[Extracted text truncated.]"
