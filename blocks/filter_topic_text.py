"""
Topic Filtering Block
Filters PDF text to extract only content relevant to a specified topic.
"""
from typing import Dict
from utils.ai_helper import llm, retry_on_failure, truncate_text


@retry_on_failure(max_retries=1)
def filter_topic_text(raw_text: str, topic: str) -> Dict[str, str]:
    """
    Filter PDF text to extract content related to a specific topic.
    
    Args:
        raw_text: Full text from PDF
        topic: User-specified topic to filter by
        
    Returns:
        Dictionary containing filtered text related to the topic
        
    Raises:
        ValueError: If topic is empty or filtering fails
        Exception: If AI processing fails after retry
    """
    # Validate topic
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty")
    
    # Truncate input text to 10000 tokens maximum
    truncated_text = truncate_text(raw_text, max_tokens=10000)
    
    # Construct prompt for AI
    prompt = f"""
    From this text, extract ONLY the content related to the topic: "{topic}".
    Keep it clean and structured.

    Text:
    {truncated_text}
    """
    
    # Call AI
    topic_text = llm(prompt)
    
    # Validate result
    if not topic_text or not topic_text.strip():
        return {
            "topic_text": "",
            "message": f"No relevant content found for topic: {topic}"
        }
    
    # Check minimum content length (50 characters)
    if len(topic_text.strip()) < 50:
        return {
            "topic_text": "",
            "message": f"Insufficient content found for topic: {topic}"
        }
    
    return {"topic_text": topic_text}
