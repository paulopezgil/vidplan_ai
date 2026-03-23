from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.services.file_service.extract_text import extract_text_from_upload


def _make_upload(filename: str) -> MagicMock:
    f = MagicMock()
    f.filename = filename
    return f


class TestExtractTextFromUpload:
    @pytest.mark.asyncio
    async def test_dispatches_pdf(self):
        upload = _make_upload("cv.pdf")
        with (
            patch("app.services.file_service.extract_text.save_upload", new_callable=AsyncMock, return_value=Path("/tmp/cv.pdf")),
            patch("app.services.file_service.extract_text.extract_pdf", return_value="PDF text") as mock_pdf,
            patch("pathlib.Path.unlink"),
        ):
            result = await extract_text_from_upload(upload)
        mock_pdf.assert_called_once()
        assert result == "PDF text"

    @pytest.mark.asyncio
    async def test_dispatches_docx(self):
        upload = _make_upload("cv.docx")
        with (
            patch("app.services.file_service.extract_text.save_upload", new_callable=AsyncMock, return_value=Path("/tmp/cv.docx")),
            patch("app.services.file_service.extract_text.extract_docx", return_value="DOCX text") as mock_docx,
            patch("pathlib.Path.unlink"),
        ):
            result = await extract_text_from_upload(upload)
        mock_docx.assert_called_once()
        assert result == "DOCX text"

    @pytest.mark.asyncio
    async def test_dispatches_image(self):
        upload = _make_upload("photo.png")
        with (
            patch("app.services.file_service.extract_text.save_upload", new_callable=AsyncMock, return_value=Path("/tmp/photo.png")),
            patch("app.services.file_service.extract_text.extract_image", return_value="Image text") as mock_img,
            patch("pathlib.Path.unlink"),
        ):
            result = await extract_text_from_upload(upload)
        mock_img.assert_called_once()
        assert result == "Image text"

    @pytest.mark.asyncio
    async def test_unsupported_extension_raises_415(self):
        upload = _make_upload("cv.xlsx")
        with pytest.raises(HTTPException) as exc_info:
            await extract_text_from_upload(upload)
        assert exc_info.value.status_code == 415

    @pytest.mark.asyncio
    async def test_empty_text_raises_422(self):
        upload = _make_upload("cv.pdf")
        with (
            patch("app.services.file_service.extract_text.save_upload", new_callable=AsyncMock, return_value=Path("/tmp/cv.pdf")),
            patch("app.services.file_service.extract_text.extract_pdf", return_value="   "),
            patch("pathlib.Path.unlink"),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await extract_text_from_upload(upload)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_extractor_exception_raises_422(self):
        upload = _make_upload("cv.pdf")
        with (
            patch("app.services.file_service.extract_text.save_upload", new_callable=AsyncMock, return_value=Path("/tmp/cv.pdf")),
            patch("app.services.file_service.extract_text.extract_pdf", side_effect=RuntimeError("corrupted")),
            patch("pathlib.Path.unlink"),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await extract_text_from_upload(upload)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_strips_whitespace_from_result(self):
        upload = _make_upload("cv.docx")
        with (
            patch("app.services.file_service.extract_text.save_upload", new_callable=AsyncMock, return_value=Path("/tmp/cv.docx")),
            patch("app.services.file_service.extract_text.extract_docx", return_value="  hello world  "),
            patch("pathlib.Path.unlink"),
        ):
            result = await extract_text_from_upload(upload)
        assert result == "hello world"
