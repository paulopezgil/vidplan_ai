from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.services.file_service.save_upload import save_upload
from app.services.file_service.extract_pdf import extract_pdf
from app.services.file_service.extract_image import extract_image
from app.services.file_service.extract_docx import extract_docx

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".tiff", ".tif"}


async def extract_text_from_upload(file: UploadFile) -> str:
    suffix = Path(file.filename).suffix.lower() if file.filename else ""

    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{suffix}'. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
        )

    tmp_path = await save_upload(file)
    try:
        if suffix == ".pdf":
            text = extract_pdf(tmp_path)
        elif suffix == ".docx":
            text = extract_docx(tmp_path)
        else:
            text = extract_image(tmp_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not extract text from file: {e}")
    finally:
        tmp_path.unlink(missing_ok=True)

    if not text or not text.strip():
        raise HTTPException(status_code=422, detail="No text could be extracted from the uploaded file.")

    return text.strip()
