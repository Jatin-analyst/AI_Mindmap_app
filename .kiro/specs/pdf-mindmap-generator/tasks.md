# Implementation Plan

- [x] 1. Set up project structure and dependencies


  - Create directory structure for blocks, pipelines, tests, and frontend
  - Set up virtual environment and install dependencies (fastapi, uvicorn, pdfplumber, kiro, hypothesis, pytest, streamlit, streamlit-agraph)
  - Create requirements.txt with all dependencies
  - Initialize temp directory for file storage
  - _Requirements: 1.1, 9.4_



- [ ] 2. Implement PDF extraction block
  - Create blocks/extract_pdf.py with @block decorator
  - Implement pdfplumber integration to extract text from all pages
  - Handle pages with no extractable text gracefully
  - Add error handling for corrupted PDFs
  - Return raw_text in dictionary format


  - _Requirements: 1.1, 1.2_


- [ ]* 2.1 Write property test for PDF extraction
  - **Property 1: PDF format validation**
  - **Validates: Requirements 1.2, 1.3**

- [x] 3. Implement topic detection block

  - Create blocks/detect_topics.py with @block decorator
  - Implement AI prompt construction for topic extraction
  - Truncate input text to ~6000 characters to prevent token overflow
  - Parse AI response as JSON list
  - Handle AI parsing errors with retry logic
  - _Requirements: 2.4, 2.5_

- [x]* 3.1 Write property test for topic detection


  - **Property 5: Topic detection returns results**
  - **Validates: Requirements 2.4**

- [x]* 3.2 Write property test for minimum topic count

  - **Property 6: Minimum topic count**
  - **Validates: Requirements 2.5**

- [x] 4. Implement topic filtering block


  - Create blocks/filter_topic_text.py with @block decorator
  - Implement AI prompt for extracting topic-related content
  - Limit input text to 10000 tokens maximum
  - Preserve structure and context in filtered content
  - Return empty string with message if topic not found
  - Validate minimum content length (50 characters)
  - _Requirements: 3.1, 3.2, 3.4, 3.5_

- [x]* 4.1 Write property test for topic filtering


  - **Property 7: Topic filtering relevance**
  - **Validates: Requirements 3.1**

- [x]* 4.2 Write property test for filtered content length

  - **Property 8: Filtered content minimum length**
  - **Validates: Requirements 3.4**

- [x]* 4.3 Write property test for input truncation

  - **Property 9: Input text truncation**
  - **Validates: Requirements 3.5**

- [x] 5. Implement mind map generation block


  - Create blocks/generate_mindmap.py with @block decorator
  - Construct detailed AI prompt with expected JSON schema
  - Parse and validate JSON response structure
  - Ensure all parent references point to valid node IDs
  - Support minimum 4 levels of hierarchy
  - Implement retry logic on AI failure
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x]* 5.1 Write property test for mind map structure


  - **Property 10: Mind map structure validity**
  - **Validates: Requirements 4.1, 4.5**

- [x]* 5.2 Write property test for referential integrity

  - **Property 11: Mind map referential integrity**
  - **Validates: Requirements 4.3**

- [x]* 5.3 Write property test for hierarchy depth

  - **Property 12: Mind map hierarchy depth**
  - **Validates: Requirements 4.4**

- [x] 6. Implement Kiro pipelines


  - Create pipelines/pdf_to_topics.py with @pipeline decorator
  - Chain extract_pdf → detect_topics blocks
  - Create pipelines/topic_to_mindmap.py with @pipeline decorator
  - Chain extract_pdf → filter_topic_text → generate_mindmap blocks
  - Add error propagation between blocks
  - _Requirements: 2.4, 4.1_

- [x]* 6.1 Write unit tests for pipelines


  - Test pdf_to_topics pipeline with sample PDF
  - Test topic_to_mindmap pipeline with sample PDF and topic
  - Test error handling in pipeline execution
  - _Requirements: 2.4, 4.1_

- [x] 7. Implement input validation utilities


  - Create utils/validation.py module
  - Implement PDF file format validation
  - Implement file size validation (80MB limit)
  - Implement topic string validation (whitespace check, length truncation)
  - Return appropriate error messages for each validation failure
  - _Requirements: 1.2, 1.3, 1.4, 2.1, 2.2, 2.3_

- [x]* 7.1 Write property test for whitespace topic rejection


  - **Property 3: Whitespace topic rejection**
  - **Validates: Requirements 2.2**

- [x]* 7.2 Write property test for topic truncation

  - **Property 4: Topic truncation**
  - **Validates: Requirements 2.3**

- [x] 8. Implement file management utilities


  - Create utils/file_manager.py module
  - Implement temporary file storage with unique identifiers
  - Implement file cleanup function with 5-minute TTL
  - Add background task for periodic cleanup
  - Ensure cleanup on error conditions
  - _Requirements: 1.1, 1.5, 6.3, 9.4_


- [ ]* 8.1 Write property test for file cleanup
  - **Property 16: Temporary file cleanup on error**
  - **Validates: Requirements 6.3**


- [ ]* 8.2 Write property test for TTL cleanup
  - **Property 22: Temporary file cleanup after completion**


  - **Validates: Requirements 9.4**

- [ ] 9. Implement error handling utilities
  - Create utils/error_handler.py module
  - Implement error sanitization (remove internal details, stack traces, paths)
  - Create error response models with type and message

  - Implement logging with timestamp and context
  - Add first-error precedence logic for pipelines
  - _Requirements: 6.1, 6.2, 6.4, 6.5_


- [ ]* 9.1 Write property test for error message safety
  - **Property 15: Error message safety**

  - **Validates: Requirements 6.2, 6.4**

- [ ]* 9.2 Write property test for error precedence
  - **Property 17: First error precedence**
  - **Validates: Requirements 6.5**

- [x] 10. Implement AI retry logic

  - Create utils/ai_helper.py module
  - Wrap Kiro llm function with retry decorator
  - Implement single retry on AI failure

  - Add timeout handling (60 seconds)
  - Validate AI response format before returning
  - _Requirements: 5.3, 5.4, 5.5_



- [ ]* 10.1 Write property test for AI response validation
  - **Property 13: AI response validation**
  - **Validates: Requirements 5.3, 5.5**

- [ ]* 10.2 Write property test for AI retry
  - **Property 14: AI retry on failure**
  - **Validates: Requirements 5.4**


- [ ] 11. Implement FastAPI endpoints
  - Create api/main.py with FastAPI app initialization
  - Implement POST /pdf/topics endpoint with file upload
  - Implement POST /pdf/mindmap endpoint with file and topic parameters
  - Add request validation using Pydantic models

  - Add response formatting with proper HTTP status codes
  - Implement error handling middleware
  - Add CORS middleware for frontend integration
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3_

- [ ]* 11.1 Write unit tests for API endpoints
  - Test /pdf/topics with valid PDF
  - Test /pdf/mindmap with valid PDF and topic
  - Test error responses for invalid inputs
  - Test file size limit enforcement
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ]* 11.2 Write property test for successful upload
  - **Property 2: Successful upload confirmation**
  - **Validates: Requirements 1.5**

- [x] 12. Checkpoint - Ensure all tests pass


  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Implement Streamlit frontend structure


  - Create streamlit_app.py with basic layout
  - Add custom CSS for colorful, interactive design
  - Implement color scheme (blues, purples, oranges, greens)
  - Create header with gradient background
  - Set up session state management
  - _Requirements: 7.1_

- [x] 14. Implement file upload UI component

  - Add st.file_uploader with PDF type restriction
  - Create interactive drag-and-drop area with hover effects
  - Display uploaded file name and size with success message
  - Add visual feedback animations
  - _Requirements: 7.2_

- [x] 15. Implement topic detection UI

  - Add "Detect Topics" button with loading spinner
  - Call FastAPI /pdf/topics endpoint
  - Display detected topics as colorful, clickable pills/badges
  - Implement hover effects and animations on topic buttons
  - Store selected topic in session state
  - _Requirements: 7.4_

- [x]* 15.1 Write property test for interactive topic display

  - **Property 18: Interactive topic display**
  - **Validates: Requirements 7.4**

- [x] 16. Implement topic input and selection

  - Add text input field for manual topic entry
  - Implement autocomplete from detected topics
  - Sync manual input with topic button selection
  - Add placeholder text and help tooltip
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 17. Implement mind map generation UI

  - Add "Generate Mind Map" button with loading states
  - Display animated progress indicator with status messages
  - Call FastAPI /pdf/mindmap endpoint
  - Store generated mind map in session state
  - _Requirements: 7.3_

- [x] 18. Implement interactive mind map visualization

  - Integrate streamlit-agraph for graph rendering
  - Convert mind map JSON to nodes and edges
  - Apply color coding by hierarchy level (purple, blue, green, orange/yellow)
  - Implement zoom and pan controls
  - Add node hover tooltips
  - Make nodes clickable to highlight connections
  - Configure physics and hierarchical layout
  - _Requirements: 7.5_

- [x]* 18.1 Write property test for visualization interactivity

  - **Property 19: Mind map visualization interactivity**
  - **Validates: Requirements 7.5**

- [x] 19. Implement download functionality

  - Add download buttons for JSON and PNG formats
  - Implement JSON download with base64 encoding
  - Generate descriptive filenames with topic name and timestamp
  - Add download confirmation toast messages
  - Style buttons with icons and hover effects
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x]* 19.1 Write property test for download button availability

  - **Property 20: Download button availability**
  - **Validates: Requirements 8.1**

- [x]* 19.2 Write property test for filename format

  - **Property 21: Download filename format**
  - **Validates: Requirements 8.4**

- [x] 20. Implement error handling in UI

  - Display user-friendly error messages with emoji icons
  - Add error state styling (red alerts)
  - Handle API errors gracefully
  - Show specific error messages for different failure types
  - _Requirements: 6.2, 6.4_

- [x] 21. Add loading states and animations

  - Implement custom loading spinners with colors
  - Add progress bars for multi-stage processing
  - Display status messages during processing
  - Add smooth transitions between UI states
  - _Requirements: 7.3_

- [x] 22. Configure deployment settings


  - Create .streamlit/config.toml for Streamlit settings
  - Set up environment variables for API URL
  - Configure CORS in FastAPI for Streamlit origin
  - Add requirements.txt for Streamlit Cloud deployment
  - Create README with deployment instructions
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 23. Final Checkpoint - Ensure all tests pass


  - Ensure all tests pass, ask the user if questions arise.
