from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader


def extract_pdf_text(pdf_path: str) -> List[Dict]:
    """
    Extract text from each page of a PDF.

    Returns a list of dicts:
    [
        {
            "page_number": 1,
            "text": "...",
            "source": "file.pdf"
        },
        ...
    ]
    """
    path = Path(pdf_path)
    reader = PdfReader(str(path))

    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append(
            {
                "page_number": i + 1,
                "text": text.strip(),
                "source": path.name,
            }
        )

    return pages