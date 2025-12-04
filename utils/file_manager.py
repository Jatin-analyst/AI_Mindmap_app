"""
File management utilities for temporary file handling.
"""
import os
import time
import uuid
from typing import Optional
from datetime import datetime, timedelta


# Default temp directory
TEMP_DIR = os.getenv("TEMP_DIR", "./temp")

# File cleanup TTL (5 minutes)
FILE_CLEANUP_TTL = int(os.getenv("FILE_CLEANUP_INTERVAL", "300"))


def ensure_temp_directory():
    """Ensure the temporary directory exists."""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR, exist_ok=True)


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename for temporary storage.
    
    Args:
        original_filename: Original name of the uploaded file
        
    Returns:
        Unique filename with UUID prefix
    """
    # Generate UUID
    unique_id = str(uuid.uuid4())[:8]
    
    # Get file extension
    _, ext = os.path.splitext(original_filename)
    
    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{unique_id}_{timestamp}{ext}"
    
    return unique_filename


def save_uploaded_file(file_content: bytes, original_filename: str) -> str:
    """
    Save uploaded file to temporary directory.
    
    Args:
        file_content: Binary content of the file
        original_filename: Original name of the uploaded file
        
    Returns:
        Path to the saved file
    """
    ensure_temp_directory()
    
    # Generate unique filename
    unique_filename = generate_unique_filename(original_filename)
    file_path = os.path.join(TEMP_DIR, unique_filename)
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    return file_path


def cleanup_file(file_path: str) -> bool:
    """
    Clean up a temporary file.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        True if file was deleted, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error cleaning up file {file_path}: {str(e)}")
        return False


def cleanup_old_files(max_age_seconds: Optional[int] = None):
    """
    Clean up temporary files older than specified age.
    
    Args:
        max_age_seconds: Maximum age of files in seconds (default: FILE_CLEANUP_TTL)
    """
    if max_age_seconds is None:
        max_age_seconds = FILE_CLEANUP_TTL
    
    ensure_temp_directory()
    
    current_time = time.time()
    cutoff_time = current_time - max_age_seconds
    
    # Iterate through files in temp directory
    for filename in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, filename)
        
        # Skip directories and .gitkeep
        if os.path.isdir(file_path) or filename == '.gitkeep':
            continue
        
        try:
            # Get file modification time
            file_mtime = os.path.getmtime(file_path)
            
            # Delete if older than cutoff
            if file_mtime < cutoff_time:
                os.unlink(file_path)
                print(f"Cleaned up old file: {filename}")
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")


def cleanup_on_error(file_path: str):
    """
    Clean up file when an error occurs during processing.
    
    Args:
        file_path: Path to the file to clean up
    """
    cleanup_file(file_path)
