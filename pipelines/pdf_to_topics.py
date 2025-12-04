"""
PDF to Topics Pipeline
Extracts and detects topics from a PDF file.
"""
from typing import Dict, List
from blocks.extract_pdf import extract_pdf
from blocks.detect_topics import detect_topics


def pdf_to_topics(file_path: str) -> Dict[str, List[str]]:
    """
    Pipeline to extract topics from a PDF file.
    
    Args:
        file_path: Path to the uploaded PDF
        
    Returns:
        Dictionary containing list of detected topics
        
    Raises:
        Exception: If any step in the pipeline fails
    """
    try:
        # Step 1: Extract text from PDF
        pdf_data = extract_pdf(file_path)
        raw_text = pdf_data["raw_text"]
        
        # Step 2: Detect topics from text
        topics_data = detect_topics(raw_text)
        
        return topics_data
        
    except Exception as e:
        # Propagate the first error encountered
        raise Exception(f"Pipeline failed: {str(e)}")
