class TextExtractionWithPyMuPDF:
    def text_extraction(pdf_file):
        import os
        import pymupdf

        pdf_path = os.path.abspath(pdf_file)

        if not pdf_path.lower().endswith(".pdf"):
            raise ValueError("File must be a PDF")

        pdf = pymupdf.open(pdf_path)

        pages = []

        for page_number, page in enumerate(pdf):
            pages.append({
                "page": page_number + 1,
                "text": page.get_text()
            })

        pdf.close()

        return pages
