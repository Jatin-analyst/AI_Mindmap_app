from kiro import pipeline
from blocks.extract_pdf import extract_pdf
from blocks.detect_topics import detect_topics

@pipeline
def pdf_to_topics(file_path: str):
    pdf_data = extract_pdf(file_path)
    topics = detect_topics(pdf_data["raw_text"])
    return topics
