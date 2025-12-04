"""
Topic Detection Block
Analyzes PDF text and extracts prominent topics using AI.
"""
import json
from typing import Dict, List
from utils.ai_helper import llm, retry_on_failure, validate_json_response


@retry_on_failure(max_retries=1)
def detect_topics(raw_text: str) -> Dict[str, List[str]]:
    """
    Detect topics from raw PDF text using AI.
    
    Args:
        raw_text: Raw text extracted from PDF
        
    Returns:
        Dictionary containing list of detected topics
        
    Raises:
        ValueError: If AI response is invalid
        Exception: If AI processing fails after retry
    """
    # Truncate text to prevent token overflow (~6000 characters)
    truncated_text = raw_text[:6000] if len(raw_text) > 6000 else raw_text
    
    # Construct prompt for AI
    prompt = f"""Extract the main topics and headings from this text.

IMPORTANT: Return ONLY a JSON array, no explanations or markdown.

Format: ["Topic 1", "Topic 2", "Topic 3"]

Text to analyze:
{truncated_text}

Return only the JSON array:"""
    
    # Call AI
    response = llm(prompt)
    
    # Validate and parse JSON response
    try:
        topics = validate_json_response(response)
        
        # Ensure it's a list
        if not isinstance(topics, list):
            raise ValueError("AI response is not a list")
        
        # Ensure all items are strings
        if not all(isinstance(topic, str) for topic in topics):
            raise ValueError("AI response contains non-string topics")
        
        # Return at least top 10 topics if available
        return {"topics": topics[:10] if len(topics) > 10 else topics}
        
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Failed to parse AI response: {str(e)}")
