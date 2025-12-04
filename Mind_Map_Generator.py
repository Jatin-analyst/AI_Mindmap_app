from kiro import block, llm

@block
def generate_mindmap(topic_text: str) -> dict:
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

    Text:
    {topic_text}
    """

    mindmap_json = llm(prompt)
    return {"mindmap": mindmap_json}
