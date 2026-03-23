from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch


from app.services.file_service.extract_image import extract_image


class TestExtractImage:
    def test_returns_ocr_text(self):
        mock_image = MagicMock()
        with (
            patch("app.services.file_service.extract_image.Image.open", return_value=mock_image),
            patch("app.services.file_service.extract_image.pytesseract.image_to_string", return_value="OCR result"),
        ):
            result = extract_image(Path("photo.jpg"))
        assert result == "OCR result"

    def test_passes_image_to_tesseract(self):
        mock_image = MagicMock()
        with (
            patch("app.services.file_service.extract_image.Image.open", return_value=mock_image) as mock_open,
            patch("app.services.file_service.extract_image.pytesseract.image_to_string", return_value="") as mock_ocr,
        ):
            extract_image(Path("photo.png"))
        mock_open.assert_called_once_with("photo.png")
        mock_ocr.assert_called_once_with(mock_image)
