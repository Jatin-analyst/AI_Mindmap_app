from kiro import pipeline
from blocks.filter_topic_text import filter_topic_text
from blocks.generate_mindmap import generate_mindmap
from blocks.extract_pdf import extract_pdf

@pipeline
def topic_to_mindmap(file_path: str, topic: str):
    pdf_data = extract_pdf(file_path)
    filtered = filter_topic_text(pdf_data["raw_text"], topic)
    mindmap = generate_mindmap(filtered["topic_text"])
    return mindmap
