"""
Unit tests for pipelines.
"""
import pytest
import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pipelines.pdf_to_topics import pdf_to_topics
from pipelines.topic_to_mindmap import topic_to_mindmap


def create_sample_pdf(text_content: str) -> str:
    """Helper function to create a sample PDF for testing."""
    tmp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    tmp_path = tmp_file.name
    tmp_file.close()
    
    # Create PDF with text
    c = canvas.Canvas(tmp_path, pagesize=letter)
    c.drawString(100, 750, text_content)
    c.save()
    
    return tmp_path


def test_pdf_to_topics_pipeline():
    """Test pdf_to_topics pipeline with sample PDF."""
    # Create sample PDF
    pdf_path = create_sample_pdf("Introduction to Machine Learning. Chapter 1: Basics. Chapter 2: Advanced Topics.")
    
    try:
        # Run pipeline
        result = pdf_to_topics(pdf_path)
        
        # Verify result structure
        assert "topics" in result
        assert isinstance(result["topics"], list)
        assert len(result["topics"]) > 0
        
    finally:
        # Cleanup
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)


def test_topic_to_mindmap_pipeline():
    """Test topic_to_mindmap pipeline with sample PDF and topic."""
    # Create sample PDF
    pdf_path = create_sample_pdf("Machine Learning is a field of AI. It includes supervised and unsupervised learning.")
    
    try:
        # Run pipeline
        result = topic_to_mindmap(pdf_path, "Machine Learning")
        
        # Verify result structure
        assert "mindmap" in result
        mindmap = result["mindmap"]
        assert "topic" in mindmap
        assert "nodes" in mindmap
        assert isinstance(mindmap["nodes"], list)
        assert len(mindmap["nodes"]) > 0
        
    finally:
        # Cleanup
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)


def test_pipeline_error_handling():
    """Test error handling in pipelines."""
    # Test with non-existent file
    with pytest.raises(Exception) as exc_info:
        pdf_to_topics("nonexistent.pdf")
    assert "Pipeline failed" in str(exc_info.value)
    
    # Test with invalid topic
    pdf_path = create_sample_pdf("Some content")
    try:
        with pytest.raises(Exception) as exc_info:
            topic_to_mindmap(pdf_path, "")
        assert "Pipeline failed" in str(exc_info.value)
    finally:
        if os.path.exists(pdf_path):
            os.unlink(pdf_path)
