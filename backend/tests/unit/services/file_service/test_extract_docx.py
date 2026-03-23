from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from app.services.file_service.extract_docx import extract_docx


class TestExtractDocx:
    def test_returns_extracted_text(self):
        with patch("app.services.file_service.extract_docx.docx2txt.process", return_value="Resume content"):
            result = extract_docx(Path("resume.docx"))
        assert result == "Resume content"

    def test_passes_path_as_string(self):
        with patch("app.services.file_service.extract_docx.docx2txt.process", return_value="") as mock_process:
            extract_docx(Path("/tmp/file.docx"))
        mock_process.assert_called_once_with("/tmp/file.docx")
