from kiro import block, llm

@block
def filter_topic_text(raw_text: str, topic: str) -> dict:
    prompt = f"""
    From this text, extract ONLY the content related to the topic: "{topic}".
    Keep it clean and structured.

    Text:
    {raw_text}
    """
    topic_text = llm(prompt)
    return {"topic_text": topic_text}
