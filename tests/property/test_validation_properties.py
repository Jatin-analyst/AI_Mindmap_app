"""
Property-based tests for input validation.
Tests Properties 1, 3, and 4 from the design document.
"""
import pytest
from hypothesis import given, strategies as st, settings
import os
import tempfile
from blocks.extract_pdf import extract_pdf


# Feature: pdf-mindmap-generator, Property 1: PDF format validation
@settings(max_examples=100)
@given(
    file_content=st.binary(min_size=10, max_size=1000),
    file_extension=st.sampled_from(['.txt', '.doc', '.jpg', '.png', '.pdf'])
)
def test_pdf_format_validation(file_content, file_extension):
    """
    For any uploaded file, the system should accept it if and only if 
    it is a valid PDF format, rejecting all other file types with an 
    appropriate error message.
    
    Validates: Requirements 1.2, 1.3
    """
    # Create a temporary file with the given extension
    with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as tmp_file:
        tmp_file.write(file_content)
        tmp_path = tmp_file.name
    
    try:
        if file_extension == '.pdf':
            # For PDF files, we expect either success or a specific PDF error
            # (not a file type error)
            try:
                result = extract_pdf(tmp_path)
                # If it succeeds, it should return raw_text
                assert "raw_text" in result
            except Exception as e:
                # Should be a PDF-specific error, not a file type error
                error_msg = str(e).lower()
                assert "pdf" in error_msg or "extract" in error_msg or "corrupted" in error_msg
        else:
            # For non-PDF files, we expect an error
            with pytest.raises(Exception) as exc_info:
                extract_pdf(tmp_path)
            # The error should indicate it's not a valid PDF
            error_msg = str(exc_info.value).lower()
            assert any(keyword in error_msg for keyword in ['pdf', 'format', 'invalid', 'failed'])
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)



from utils.validation import validate_topic


# Feature: pdf-mindmap-generator, Property 3: Whitespace topic rejection
@settings(max_examples=100)
@given(
    whitespace_chars=st.lists(
        st.sampled_from([' ', '\t', '\n', '\r']),
        min_size=1,
        max_size=50
    )
)
def test_whitespace_topic_rejection(whitespace_chars):
    """
    For any string composed entirely of whitespace characters (spaces, tabs, newlines), 
    submitting it as a topic should be rejected with a validation error.
    
    Validates: Requirements 2.2
    """
    # Create whitespace-only string
    whitespace_topic = ''.join(whitespace_chars)
    
    # Validate topic
    is_valid, processed_topic, error_message = validate_topic(whitespace_topic)
    
    # Should be rejected
    assert not is_valid, "Whitespace-only topic should be rejected"
    assert error_message, "Should return an error message"
    assert "empty" in error_message.lower() or "whitespace" in error_message.lower()


# Feature: pdf-mindmap-generator, Property 4: Topic truncation
@settings(max_examples=100)
@given(
    topic_text=st.text(min_size=201, max_size=500, alphabet=st.characters(whitelist_categories=('L', 'N', 'P')))
)
def test_topic_truncation(topic_text):
    """
    For any topic string exceeding 200 characters, the system should 
    truncate it to exactly 200 characters before processing.
    
    Validates: Requirements 2.3
    """
    # Ensure topic exceeds 200 characters
    assume(len(topic_text.strip()) > 200)
    
    # Validate topic
    is_valid, processed_topic, error_message = validate_topic(topic_text)
    
    # Should be valid (truncated, not rejected)
    assert is_valid, "Long topics should be truncated, not rejected"
    
    # Should be truncated to exactly 200 characters
    assert len(processed_topic) == 200, f"Topic should be truncated to 200 chars, got {len(processed_topic)}"
