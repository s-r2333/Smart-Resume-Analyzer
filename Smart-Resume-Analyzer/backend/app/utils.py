import io
import re
import pdfplumber
import docx2txt

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf_bytes(file_bytes)
    elif name.endswith(".docx"):
        return docx2txt.process(io.BytesIO(file_bytes)) or ""
    elif name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        # try best-effort text
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return ""

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    text = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def clean_text(s: str) -> str:
    s = s.replace("\x00", " ")
    s = re.sub(r'\s+', ' ', s).strip()
    return s
