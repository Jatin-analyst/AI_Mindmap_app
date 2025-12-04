"""
Error handling utilities for PDF Mind Map Generator.
"""
import logging
import traceback
from datetime import datetime
from typing import Dict, Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, error_type: str = "ApplicationError", details: Optional[Dict] = None):
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppError):
    """Exception for validation errors."""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "ValidationError", details)


class ProcessingError(AppError):
    """Exception for processing errors."""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "ProcessingError", details)


def sanitize_error_message(error: Exception) -> str:
    """
    Sanitize error message to remove internal details.
    
    Args:
        error: Exception to sanitize
        
    Returns:
        Sanitized error message
    """
    error_str = str(error)
    
    # Remove file paths (Windows and Unix)
    import re
    error_str = re.sub(r'[A-Za-z]:\\[^\s]+', '[PATH]', error_str)
    error_str = re.sub(r'/[^\s]+', '[PATH]', error_str)
    
    # Remove stack trace indicators
    error_str = error_str.split('\n')[0]  # Take only first line
    
    # Generic message if error is too revealing
    if any(keyword in error_str.lower() for keyword in ['traceback', 'line ', 'file ']):
        return "An error occurred during processing"
    
    return error_str


def log_error(error: Exception, context: Optional[Dict] = None):
    """
    Log error with timestamp and context.
    
    Args:
        error: Exception to log
        context: Additional context information
    """
    timestamp = datetime.now().isoformat()
    context_str = f" | Context: {context}" if context else ""
    
    logger.error(f"[{timestamp}] {type(error).__name__}: {str(error)}{context_str}")
    logger.debug(traceback.format_exc())


def create_error_response(error: Exception, include_details: bool = False) -> Dict:
    """
    Create standardized error response.
    
    Args:
        error: Exception to convert to response
        include_details: Whether to include error details (for debugging)
        
    Returns:
        Dictionary with error information
    """
    # Determine error type
    if isinstance(error, AppError):
        error_type = error.error_type
        message = error.message
        details = error.details if include_details else {}
    else:
        error_type = type(error).__name__
        message = sanitize_error_message(error)
        details = {}
    
    response = {
        "error": error_type,
        "message": message
    }
    
    if details:
        response["details"] = details
    
    return response


def handle_pipeline_error(error: Exception, cleanup_func: Optional[callable] = None) -> Exception:
    """
    Handle errors in pipeline execution.
    Returns the first critical error encountered.
    
    Args:
        error: Exception that occurred
        cleanup_func: Optional cleanup function to call
        
    Returns:
        The error to propagate
    """
    # Log the error
    log_error(error)
    
    # Perform cleanup if provided
    if cleanup_func:
        try:
            cleanup_func()
        except Exception as cleanup_error:
            logger.error(f"Cleanup failed: {str(cleanup_error)}")
    
    # Return the first error (don't wrap it)
    return error
