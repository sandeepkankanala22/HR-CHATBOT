"""
Extract plain text from uploaded PDF files using PyPDF.
"""

from io import BytesIO

from pypdf import PdfReader


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Read PDF bytes and return combined text from all pages.

    Raises:
        ValueError: If PDF has no extractable text.
    """
    reader = PdfReader(BytesIO(file_bytes))
    pages_text: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages_text.append(page_text.strip())

    full_text = "\n\n".join(pages_text).strip()

    if not full_text:
        raise ValueError(
            "Could not extract text from PDF. The file may be empty or scanned images."
        )

    return full_text
