from pathlib import Path

import fitz  # pymupdf


def extract_pdf(path: Path) -> str:
    doc = fitz.open(str(path))
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())
    doc.close()
    return "\n\n".join(pages_text)
