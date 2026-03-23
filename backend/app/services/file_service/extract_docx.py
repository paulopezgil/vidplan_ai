from pathlib import Path

import docx2txt


def extract_docx(path: Path) -> str:
    return docx2txt.process(str(path))
