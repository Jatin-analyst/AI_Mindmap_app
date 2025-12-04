from kiro import block, llm

@block
def detect_topics(raw_text: str) -> dict:
    prompt = f"""
    Extract a clean list of topics/headings from the following text.
    Return JSON list only:
    ["Topic 1", "Topic 2", ...]
    
    Text:
    {raw_text[:6000]}  # keep trimmed for tokens
    """

    topics = llm(prompt)
    return {"topics": topics}
