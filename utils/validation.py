"""
Input validation utilities for PDF Mind Map Generator.
"""
import os
from typing import Tuple


# Maximum file size: 80MB
MAX_FILE_SIZE = 80 * 1024 * 1024

# Maximum topic length
MAX_TOPIC_LENGTH = 200


def validate_pdf_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate that a file is a valid PDF.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False, "File not found"
    
    # Check file extension
    if not file_path.lower().endswith('.pdf'):
        return False, "File type not supported. Please upload a PDF file."
    
    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        size_mb = file_size / (1024 * 1024)
        return False, f"File size ({size_mb:.1f}MB) exceeds maximum allowed size (80MB)"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, ""


def validate_topic(topic: str) -> Tuple[bool, str, str]:
    """
    Validate and process topic string.
    
    Args:
        topic: Topic string to validate
        
    Returns:
        Tuple of (is_valid, processed_topic, error_message)
    """
    # Check if topic is empty or whitespace only
    if not topic or not topic.strip():
        return False, "", "Topic cannot be empty or contain only whitespace"
    
    # Truncate if exceeds maximum length
    processed_topic = topic.strip()
    if len(processed_topic) > MAX_TOPIC_LENGTH:
        processed_topic = processed_topic[:MAX_TOPIC_LENGTH]
    
    return True, processed_topic, ""


def validate_file_upload(file_path: str, file_size: int) -> Tuple[bool, str]:
    """
    Validate file upload parameters.
    
    Args:
        file_path: Path to uploaded file
        file_size: Size of uploaded file in bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size
    if file_size > MAX_FILE_SIZE:
        size_mb = file_size / (1024 * 1024)
        return False, f"File size ({size_mb:.1f}MB) exceeds maximum allowed size (80MB)"
    
    if file_size == 0:
        return False, "File is empty"
    
    # Check file extension
    if not file_path.lower().endswith('.pdf'):
        return False, "File type not supported. Please upload a PDF file."
    
    return True, ""
