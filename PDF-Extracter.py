from kiro import block
import pdfplumber

@block
def extract_pdf(file_path: str) -> dict:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return {"raw_text": text}
