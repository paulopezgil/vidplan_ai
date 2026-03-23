import shutil
import tempfile
from pathlib import Path

from fastapi import UploadFile


async def save_upload(file: UploadFile) -> Path:
    suffix = Path(file.filename).suffix if file.filename else ""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        shutil.copyfileobj(file.file, tmp)
    finally:
        tmp.close()
    return Path(tmp.name)
