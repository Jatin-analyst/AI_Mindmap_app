"""
PDF Extraction Block
Extracts text content from PDF files using pdfplumber.
"""
import pdfplumber
from typing import Dict


def extract_pdf(file_path: str) -> Dict[str, str]:
    """
    Extract text content from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Dictionary containing the extracted raw text
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If the PDF is corrupted or unreadable
    """
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        
        if not text.strip():
            raise ValueError("No extractable text found in PDF")
            
        return {"raw_text": text}
        
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")
