from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.services.file_service.extract_pdf import extract_pdf


def _make_mock_doc(page_texts: list[str]):
    pages = [MagicMock(**{"get_text.return_value": t}) for t in page_texts]
    doc = MagicMock()
    doc.__iter__ = MagicMock(return_value=iter(pages))
    return doc


class TestExtractPdf:
    def test_joins_pages_with_double_newline(self):
        mock_doc = _make_mock_doc(["Page one text.", "Page two text."])
        with patch("app.services.file_service.extract_pdf.fitz.open", return_value=mock_doc):
            result = extract_pdf(Path("dummy.pdf"))
        assert result == "Page one text.\n\nPage two text."

    def test_single_page(self):
        mock_doc = _make_mock_doc(["Only page."])
        with patch("app.services.file_service.extract_pdf.fitz.open", return_value=mock_doc):
            result = extract_pdf(Path("dummy.pdf"))
        assert result == "Only page."

    def test_empty_pdf_returns_empty_string(self):
        mock_doc = _make_mock_doc([])
        with patch("app.services.file_service.extract_pdf.fitz.open", return_value=mock_doc):
            result = extract_pdf(Path("dummy.pdf"))
        assert result == ""

    def test_closes_document(self):
        mock_doc = _make_mock_doc(["text"])
        with patch("app.services.file_service.extract_pdf.fitz.open", return_value=mock_doc):
            extract_pdf(Path("dummy.pdf"))
        mock_doc.close.assert_called_once()
