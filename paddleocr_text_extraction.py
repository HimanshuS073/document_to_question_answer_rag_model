import os
from collections.abc import Mapping

import pymupdf
from paddleocr import PaddleOCR


class TextExtractionWithPaddleOCR:
    """Extract page-level text using PaddleOCR's current and legacy APIs."""

    @staticmethod
    def _text_from_result(result):
        """Return recognized text only, never image bytes or other metadata."""
        if result is None or isinstance(result, (bytes, bytearray, memoryview)):
            return []

        if isinstance(result, str):
            return [result] if result.strip() else []

        if isinstance(result, Mapping):
            # PaddleOCR 3.x uses rec_texts in the result JSON.
            for key in ("rec_texts", "texts", "text"):
                value = result.get(key)
                if isinstance(value, (list, tuple)):
                    return [item for item in value if isinstance(item, str) and item.strip()]
                if isinstance(value, str) and value.strip():
                    return [value]

            texts = []
            for value in result.values():
                texts.extend(TextExtractionWithPaddleOCR._text_from_result(value))
            return texts

        if isinstance(result, (list, tuple)):
            # Legacy PaddleOCR output contains entries like [box, (text, score)].
            texts = []
            for item in result:
                if (
                    isinstance(item, (list, tuple))
                    and len(item) >= 1
                    and isinstance(item[-1], (list, tuple))
                    and item[-1]
                    and isinstance(item[-1][0], str)
                ):
                    texts.append(item[-1][0])
                else:
                    texts.extend(TextExtractionWithPaddleOCR._text_from_result(item))
            return texts

        # PaddleOCR 3.x result objects commonly expose json() or to_dict().
        for method_name in ("json", "to_dict"):
            method = getattr(result, method_name, None)
            if callable(method):
                try:
                    return TextExtractionWithPaddleOCR._text_from_result(method())
                except (TypeError, ValueError, AttributeError):
                    pass

        return []

    def text_extraction(self, pdf_file):
        pdf_path = os.path.abspath(pdf_file)
        if not pdf_path.lower().endswith(".pdf"):
            raise ValueError("File must be a PDF")
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        ocr = PaddleOCR(lang="en")
        pages = []
        pdf = pymupdf.open(pdf_path)
        try:
            for page_number, page in enumerate(pdf, start=1):
                print(f"PaddleOCR: processing page {page_number}...")
                image = page.get_pixmap(dpi=200).tobytes("png")
                result = ocr.predict(image)
                recognized_lines = self._text_from_result(result)
                pages.append({"page": page_number, "text": "\n".join(recognized_lines)})
        finally:
            pdf.close()

        return pages
