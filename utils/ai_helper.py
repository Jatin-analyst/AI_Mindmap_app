"""
AI Helper utilities for interacting with AI models.
Supports OpenAI, Groq, and other providers.
"""
import json
import time
import os
from typing import Any, Callable
from functools import wraps


def llm(prompt: str) -> str:
    """
    Call AI model to generate response.
    Supports multiple providers via environment variables.
    
    Args:
        prompt: The prompt to send to the AI
        
    Returns:
        AI-generated response as a string
    """
    # Check which AI provider to use
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return _call_openai(prompt)
    elif provider == "groq":
        return _call_groq(prompt)
    elif provider == "anthropic":
        return _call_anthropic(prompt)
    else:
        raise ValueError(f"Unsupported AI provider: {provider}")


def _call_openai(prompt: str) -> str:
    """Call OpenAI API."""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        client = OpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes documents and creates structured outputs. Always respond with valid JSON when requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        raise ImportError("OpenAI package not installed. Run: pip install openai")
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def _call_groq(prompt: str) -> str:
    """Call Groq API (fast Llama models)."""
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        client = Groq(api_key=api_key)
        model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes documents and creates structured outputs. Always respond with valid JSON when requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except ImportError:
        raise ImportError("Groq package not installed. Run: pip install groq")
    except Exception as e:
        raise Exception(f"Groq API error: {str(e)}")


def _call_anthropic(prompt: str) -> str:
    """Call Anthropic Claude API."""
    try:
        import anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        client = anthropic.Anthropic(api_key=api_key)
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
        
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
        
    except ImportError:
        raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    except Exception as e:
        raise Exception(f"Anthropic API error: {str(e)}")


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
