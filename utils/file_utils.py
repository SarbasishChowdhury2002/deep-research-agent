"""Text extraction helpers for uploaded files."""

import io


def extract_text(file_bytes: bytes, filename: str) -> str:
    import PyPDF2
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        print(f"Error extracting text from {filename}: {e}")
        return ""
