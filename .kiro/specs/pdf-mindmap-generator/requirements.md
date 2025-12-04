# Requirements Document

## Introduction

The PDF Mind Map Generator is an AI-powered tool designed for college students to transform PDF documents into visual mind maps. The system accepts a PDF file and a user-specified topic, processes the content using AI, and generates a structured mind map in JSON format that can be visualized. The tool leverages Python, FastAPI, Kiro Blocks, pdfplumber, Llama 3, and provides both API and web interfaces for accessibility.

## Glossary

- **System**: The PDF Mind Map Generator application
- **User**: A college student interacting with the application
- **PDF Document**: A Portable Document Format file containing educational content
- **Topic**: A specific subject or heading within the PDF that the user wants to explore
- **Mind Map**: A hierarchical visual representation of information with a central topic and related subtopics
- **Kiro Block**: A reusable processing unit in the Kiro framework decorated with @block
- **Pipeline**: A sequence of Kiro blocks that process data through multiple stages
- **Raw Text**: Unprocessed text content extracted from a PDF document
- **Filtered Text**: Text content that has been filtered to include only information relevant to a specified topic
- **JSON Mind Map**: A structured JSON representation of a mind map with nodes and relationships
- **API Endpoint**: A FastAPI route that accepts HTTP requests and returns responses
- **Frontend Interface**: A web-based user interface built with Flask or Streamlit

## Requirements

### Requirement 1

**User Story:** As a college student, I want to upload a PDF document, so that I can extract and visualize information from my study materials.

#### Acceptance Criteria

1. WHEN a user uploads a PDF file through the API endpoint, THEN the System SHALL accept the file and store it temporarily
2. WHEN a PDF file is received, THEN the System SHALL validate that the file is a valid PDF format
3. WHEN an invalid file is uploaded, THEN the System SHALL return an error message indicating the file type is not supported
4. WHEN a PDF file exceeds 80MB, THEN the System SHALL reject the upload and return a file size error message
5. WHEN a PDF upload is successful, THEN the System SHALL return a confirmation with a unique identifier

### Requirement 2

**User Story:** As a college student, I want to specify a topic from my PDF, so that I can focus on specific content areas.

#### Acceptance Criteria

1. WHEN a user provides a topic string, THEN the System SHALL accept topics containing alphanumeric characters and common punctuation
2. WHEN a topic string is empty or contains only whitespace, THEN the System SHALL reject the request and return a validation error
3. WHEN a topic exceeds 200 characters, THEN the System SHALL truncate it to 200 characters and proceed with processing
4. WHEN a user requests available topics, THEN the System SHALL analyze the PDF and return a list of detected topics
5. WHEN the System detects topics, THEN the System SHALL return at least the top 10 most prominent topics from the document

### Requirement 3

**User Story:** As a college student, I want the AI to filter PDF content by my chosen topic, so that I only see relevant information.

#### Acceptance Criteria

1. WHEN the System receives raw text and a topic, THEN the System SHALL use AI to extract only content related to that topic
2. WHEN filtered text is generated, THEN the System SHALL preserve the logical structure and context of the content
3. WHEN a topic is not found in the PDF, THEN the System SHALL return an empty result with a message indicating no relevant content was found
4. WHEN filtering is complete, THEN the System SHALL return the filtered text with a minimum of 50 characters if content exists
5. WHEN the AI processes the filtering request, THEN the System SHALL limit the input text to 10000 tokens to prevent timeout

### Requirement 4

**User Story:** As a college student, I want the AI to generate a mind map from filtered content, so that I can visualize the information hierarchically.

#### Acceptance Criteria

1. WHEN the System receives filtered text, THEN the System SHALL generate a JSON mind map with a root topic and child nodes
2. WHEN a mind map is generated, THEN the System SHALL include node IDs, parent references, and text labels for each node
3. WHEN the mind map JSON is created, THEN the System SHALL ensure all parent references point to valid node IDs
4. WHEN a mind map contains multiple levels, THEN the System SHALL support at least 4 levels of hierarchy
5. WHEN the AI generates the mind map, THEN the System SHALL return valid JSON that conforms to the specified schema

### Requirement 5

**User Story:** As a college student, I want the system to use Llama 3 for AI processing, so that I get high-quality and accurate results.

#### Acceptance Criteria

1. WHEN the System performs AI operations, THEN the System SHALL use Llama 3 model through the Kiro llm function
2. WHEN AI prompts are constructed, THEN the System SHALL include clear instructions and expected output format
3. WHEN the AI returns a response, THEN the System SHALL validate the response format before returning to the user
4. WHEN AI processing fails, THEN the System SHALL retry the request once before returning an error
5. WHEN the AI generates JSON output, THEN the System SHALL parse and validate the JSON structure

### Requirement 6

**User Story:** As a college student, I want the system to handle errors gracefully, so that I understand what went wrong and can take corrective action.

#### Acceptance Criteria

1. WHEN any processing error occurs, THEN the System SHALL log the error with timestamp and context details
2. WHEN a user-facing error occurs, THEN the System SHALL return a clear error message without exposing internal details
3. WHEN file operations fail, THEN the System SHALL clean up temporary files and return appropriate error messages
4. WHEN the System encounters an unexpected error, THEN the System SHALL return a generic error message and log full details
5. WHEN multiple errors occur in a pipeline, THEN the System SHALL return the first critical error encountered

### Requirement 7

**User Story:** As a college student, I want an interactive and colorful web interface, so that I can easily use the tool and enjoy the experience.

#### Acceptance Criteria

1. WHEN a user accesses the web interface, THEN the System SHALL display a clean and colorful design with intuitive navigation
2. WHEN a user uploads a PDF, THEN the System SHALL display an interactive file upload area with visual feedback
3. WHEN processing is in progress, THEN the System SHALL display an animated loading indicator with progress information
4. WHEN topics are detected, THEN the System SHALL display them as interactive, clickable buttons or cards with color coding
5. WHEN a mind map is generated, THEN the System SHALL display it as an interactive, zoomable, and pannable visualization with colorful nodes

### Requirement 8

**User Story:** As a college student, I want to download the generated mind map, so that I can save it for offline study or share it with classmates.

#### Acceptance Criteria

1. WHEN a mind map is successfully generated, THEN the System SHALL display a download button prominently
2. WHEN a user clicks the download button, THEN the System SHALL offer download options for JSON format
3. WHEN a user clicks the download button, THEN the System SHALL offer download options for PNG or SVG image format
4. WHEN a download is initiated, THEN the System SHALL generate the file with a descriptive filename including the topic name
5. WHEN a download completes, THEN the System SHALL provide visual confirmation to the user

### Requirement 9

**User Story:** As a college student, I want the system to process my requests efficiently, so that I can quickly generate mind maps without long wait times.

#### Acceptance Criteria

1. WHEN a PDF is uploaded, THEN the System SHALL begin processing within 2 seconds
2. WHEN text extraction occurs, THEN the System SHALL process at least 10 pages per second
3. WHEN AI operations are performed, THEN the System SHALL use streaming or chunking for large texts
4. WHEN temporary files are created, THEN the System SHALL delete them within 5 minutes of processing completion
5. WHEN concurrent requests are received, THEN the System SHALL handle at least 5 simultaneous requests without degradation
