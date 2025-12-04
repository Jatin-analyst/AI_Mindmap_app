"""
Topic to Mind Map Pipeline
Generates a mind map for a specific topic from a PDF.
"""
from typing import Dict
from blocks.extract_pdf import extract_pdf
from blocks.filter_topic_text import filter_topic_text
from blocks.generate_mindmap import generate_mindmap


def topic_to_mindmap(file_path: str, topic: str) -> Dict[str, dict]:
    """
    Pipeline to generate a mind map for a specific topic from a PDF.
    
    Args:
        file_path: Path to the uploaded PDF
        topic: User-specified topic
        
    Returns:
        Dictionary containing the mind map structure
        
    Raises:
        Exception: If any step in the pipeline fails
    """
    try:
        # Step 1: Extract text from PDF
        pdf_data = extract_pdf(file_path)
        raw_text = pdf_data["raw_text"]
        
        # Step 2: Filter text by topic
        filtered_data = filter_topic_text(raw_text, topic)
        
        # Check if content was found
        if not filtered_data.get("topic_text"):
            raise ValueError(filtered_data.get("message", "No content found for topic"))
        
        topic_text = filtered_data["topic_text"]
        
        # Step 3: Generate mind map
        mindmap_data = generate_mindmap(topic_text)
        
        return mindmap_data
        
    except Exception as e:
        # Propagate the first error encountered
        raise Exception(f"Pipeline failed: {str(e)}")
