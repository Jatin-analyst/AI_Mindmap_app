"""
Mind Map Generation Block
Generates hierarchical mind map JSON from filtered text.
"""
import json
from typing import Dict
from utils.ai_helper import llm, retry_on_failure, validate_json_response


@retry_on_failure(max_retries=1)
def generate_mindmap(topic_text: str) -> Dict[str, dict]:
    """
    Generate a hierarchical mind map from filtered text.
    
    Args:
        topic_text: Filtered text content related to a topic
        
    Returns:
        Dictionary containing the mind map structure
        
    Raises:
        ValueError: If topic_text is empty or mind map generation fails
        Exception: If AI processing fails after retry
    """
    # Validate input
    if not topic_text or not topic_text.strip():
        raise ValueError("Topic text cannot be empty")
    
    # Construct detailed prompt with expected JSON format
    prompt = f"""
    Create a mind map in JSON format from the following text.

    Format:
    {{
      "topic": "Main Topic",
      "nodes": [
        {{"id": 1, "parent": 0, "text": "Subtopic"}},
        {{"id": 2, "parent": 1, "text": "Details"}}
      ]
    }}

    Rules:
    - The "topic" field should contain the main topic
    - Each node must have "id" (unique integer), "parent" (integer, 0 for root children), and "text" (string)
    - Support at least 4 levels of hierarchy
    - All parent IDs must reference valid node IDs or be 0

    Text:
    {topic_text}
    """
    
    # Call AI
    response = llm(prompt)
    
    # Validate and parse JSON response
    try:
        mindmap = validate_json_response(response)
        
        # Validate structure
        if not isinstance(mindmap, dict):
            raise ValueError("Mind map must be a dictionary")
        
        if "topic" not in mindmap:
            raise ValueError("Mind map must have a 'topic' field")
        
        if "nodes" not in mindmap:
            raise ValueError("Mind map must have a 'nodes' field")
        
        if not isinstance(mindmap["nodes"], list):
            raise ValueError("Nodes must be a list")
        
        if len(mindmap["nodes"]) == 0:
            raise ValueError("Mind map must have at least one node")
        
        # Validate each node
        node_ids = set()
        for node in mindmap["nodes"]:
            if not isinstance(node, dict):
                raise ValueError("Each node must be a dictionary")
            
            if "id" not in node or "parent" not in node or "text" not in node:
                raise ValueError("Each node must have 'id', 'parent', and 'text' fields")
            
            if not isinstance(node["id"], int):
                raise ValueError("Node ID must be an integer")
            
            if not isinstance(node["parent"], int):
                raise ValueError("Node parent must be an integer")
            
            if not isinstance(node["text"], str):
                raise ValueError("Node text must be a string")
            
            node_ids.add(node["id"])
        
        # Validate parent references
        for node in mindmap["nodes"]:
            if node["parent"] != 0 and node["parent"] not in node_ids:
                raise ValueError(f"Node {node['id']} has invalid parent reference: {node['parent']}")
        
        return {"mindmap": mindmap}
        
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Failed to generate valid mind map: {str(e)}")
