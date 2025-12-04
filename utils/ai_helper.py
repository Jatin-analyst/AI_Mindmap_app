"""
AI Helper utilities for interacting with Llama 3 via Kiro.
Includes retry logic and response validation.
"""
import json
import time
from typing import Any, Callable
from functools import wraps


# Mock LLM function for development
# In production, this would be: from kiro import llm
def llm(prompt: str) -> str:
    """
    Mock LLM function that simulates AI responses.
    In production, this would call the actual Kiro llm function.
    
    Args:
        prompt: The prompt to send to the AI
        
    Returns:
        AI-generated response as a string
    """
    # This is a mock implementation
    # In production, replace with: from kiro import llm
    
    # Simulate AI processing
    time.sleep(0.1)
    
    # Parse the prompt to determine what kind of response to generate
    if "topics" in prompt.lower() or "headings" in prompt.lower():
        # Return mock topics
        return json.dumps([
            "Introduction",
            "Background",
            "Methodology",
            "Results",
            "Discussion",
            "Conclusion",
            "References",
            "Appendix",
            "Future Work",
            "Acknowledgments"
        ])
    elif "mind map" in prompt.lower():
        # Return mock mind map
        return json.dumps({
            "topic": "Main Topic",
            "nodes": [
                {"id": 1, "parent": 0, "text": "Subtopic 1"},
                {"id": 2, "parent": 0, "text": "Subtopic 2"},
                {"id": 3, "parent": 1, "text": "Detail 1.1"},
                {"id": 4, "parent": 1, "text": "Detail 1.2"},
                {"id": 5, "parent": 2, "text": "Detail 2.1"}
            ]
        })
    else:
        # Return filtered text
        return "This is filtered content related to the specified topic. " * 10


def retry_on_failure(max_retries: int = 1, timeout: int = 60):
    """
    Decorator to retry AI operations on failure.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 1)
        timeout: Timeout in seconds for each attempt (default: 60)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        # Log retry attempt
                        print(f"AI operation failed, retrying... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(1)  # Brief delay before retry
                    else:
                        # Max retries reached
                        break
            
            # If we get here, all retries failed
            raise Exception(f"AI operation failed after {max_retries + 1} attempts: {str(last_exception)}")
        
        return wrapper
    return decorator


def validate_json_response(response: str) -> dict:
    """
    Validate and parse JSON response from AI.
    
    Args:
        response: JSON string from AI
        
    Returns:
        Parsed JSON as dictionary
        
    Raises:
        ValueError: If response is not valid JSON
    """
    try:
        parsed = json.loads(response)
        return parsed
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from AI: {str(e)}")


def truncate_text(text: str, max_tokens: int = 10000) -> str:
    """
    Truncate text to approximate token limit.
    Rough approximation: 1 token ≈ 4 characters.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens
        
    Returns:
        Truncated text
    """
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    return text[:max_chars]
