# Design Document: PDF Mind Map Generator

## Overview

The PDF Mind Map Generator is a Python-based application that transforms PDF documents into structured mind maps using AI. The system follows a pipeline architecture using Kiro Blocks, where each block performs a specific transformation on the data. The application accepts a PDF file and a user-specified topic, extracts text content, filters it based on the topic, and generates a hierarchical JSON mind map that can be visualized.

The core workflow consists of:
1. PDF upload and validation
2. Text extraction using pdfplumber
3. Topic detection or topic-based filtering using Llama 3
4. Mind map generation in JSON format
5. Response delivery through FastAPI endpoints

## Architecture

### High-Level Architecture

```
┌─────────────┐
│   Client    │
│ (Frontend)  │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────────────────────┐
│         FastAPI Layer               │
│  ┌─────────────┐  ┌──────────────┐ │
│  │ /pdf/topics │  │ /pdf/mindmap │ │
│  └─────────────┘  └──────────────┘ │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│      Kiro Pipeline Layer            │
│  ┌──────────────┐ ┌──────────────┐ │
│  │pdf_to_topics │ │topic_to_     │ │
│  │              │ │mindmap       │ │
│  └──────────────┘ └──────────────┘ │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│       Kiro Blocks Layer             │
│  ┌──────────┐  ┌──────────────┐    │
│  │extract_  │  │detect_topics │    │
│  │pdf       │  └──────────────┘    │
│  └──────────┘  ┌──────────────┐    │
│  ┌──────────┐  │filter_topic_ │    │
│  │generate_ │  │text          │    │
│  │mindmap   │  └──────────────┘    │
│  └──────────┘                       │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│      External Dependencies          │
│  ┌──────────┐  ┌──────────────┐    │
│  │pdfplumber│  │Llama 3 (Kiro)│    │
│  └──────────┘  └──────────────┘    │
└─────────────────────────────────────┘
```

### Component Interaction Flow

**Flow 1: Topic Detection**
```
User → FastAPI (/pdf/topics) → pdf_to_topics pipeline → 
  extract_pdf block → detect_topics block → Response (JSON list)
```

**Flow 2: Mind Map Generation**
```
User → FastAPI (/pdf/mindmap) → topic_to_mindmap pipeline → 
  extract_pdf block → filter_topic_text block → 
  generate_mindmap block → Response (JSON mind map)
```

## Components and Interfaces

### 1. Kiro Blocks

#### Block: extract_pdf
**Purpose:** Extract text content from PDF files using pdfplumber

**Input:**
```python
{
  "file_path": str  # Path to the PDF file
}
```

**Output:**
```python
{
  "raw_text": str  # Extracted text content from all pages
}
```

**Behavior:**
- Opens PDF file using pdfplumber
- Iterates through all pages
- Extracts text from each page
- Concatenates text with newlines between pages
- Handles pages with no extractable text gracefully
- Raises exception if PDF is corrupted or unreadable

---

#### Block: detect_topics
**Purpose:** Analyze PDF text and extract prominent topics using AI

**Input:**
```python
{
  "raw_text": str  # Raw text from PDF (truncated to ~6000 chars)
}
```

**Output:**
```python
{
  "topics": list[str]  # List of detected topics
}
```

**Behavior:**
- Truncates input text to prevent token overflow
- Constructs prompt for Llama 3 to extract topics
- Parses AI response as JSON list
- Returns at least top 10 topics if available
- Handles AI parsing errors

---

#### Block: filter_topic_text
**Purpose:** Filter PDF text to extract only content relevant to specified topic

**Input:**
```python
{
  "raw_text": str,  # Full text from PDF
  "topic": str      # User-specified topic
}
```

**Output:**
```python
{
  "topic_text": str  # Filtered text related to the topic
}
```

**Behavior:**
- Constructs prompt asking AI to extract topic-related content
- Limits input text to 10000 tokens maximum
- Preserves structure and context of filtered content
- Returns empty string if topic not found
- Validates minimum content length (50 chars)

---

#### Block: generate_mindmap
**Purpose:** Generate hierarchical mind map JSON from filtered text

**Input:**
```python
{
  "topic_text": str  # Filtered text content
}
```

**Output:**
```python
{
  "mindmap": dict  # JSON mind map structure
}
```

**Expected Mind Map Schema:**
```python
{
  "topic": str,           # Main topic/root node
  "nodes": [
    {
      "id": int,          # Unique node identifier
      "parent": int,      # Parent node ID (0 for root children)
      "text": str         # Node content
    }
  ]
}
```

**Behavior:**
- Constructs detailed prompt with expected JSON format
- Calls Llama 3 to generate structured mind map
- Parses and validates JSON response
- Ensures all parent references are valid
- Supports minimum 4 levels of hierarchy
- Retries once on failure

### 2. Kiro Pipelines

#### Pipeline: pdf_to_topics
**Purpose:** Extract and detect topics from a PDF file

**Input:**
```python
file_path: str  # Path to uploaded PDF
```

**Output:**
```python
{
  "topics": list[str]  # List of detected topics
}
```

**Flow:**
1. Call extract_pdf(file_path)
2. Call detect_topics(raw_text)
3. Return topics list

---

#### Pipeline: topic_to_mindmap
**Purpose:** Generate mind map for a specific topic from PDF

**Input:**
```python
file_path: str,  # Path to uploaded PDF
topic: str       # User-specified topic
```

**Output:**
```python
{
  "mindmap": dict  # JSON mind map structure
}
```

**Flow:**
1. Call extract_pdf(file_path)
2. Call filter_topic_text(raw_text, topic)
3. Call generate_mindmap(topic_text)
4. Return mind map JSON

### 3. FastAPI Endpoints

#### Endpoint: POST /pdf/topics
**Purpose:** Upload PDF and get list of detected topics

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: 
  - file: UploadFile (PDF file)

**Response:**
```json
{
  "topics": ["Topic 1", "Topic 2", ...]
}
```

**Status Codes:**
- 200: Success
- 400: Invalid file or validation error
- 413: File too large (>50MB)
- 500: Processing error

---

#### Endpoint: POST /pdf/mindmap
**Purpose:** Upload PDF with topic and generate mind map

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - file: UploadFile (PDF file)
  - topic: str (query parameter or form field)

**Response:**
```json
{
  "mindmap": {
    "topic": "Main Topic",
    "nodes": [
      {"id": 1, "parent": 0, "text": "Subtopic 1"},
      {"id": 2, "parent": 1, "text": "Detail 1"}
    ]
  }
}
```

**Status Codes:**
- 200: Success
- 400: Invalid input or validation error
- 404: Topic not found in PDF
- 413: File too large
- 500: Processing error
- 504: Timeout (>60 seconds)

### 4. File Management

**Temporary File Handling:**
- Uploaded files stored in `temp/` directory
- Filename format: `{original_filename}`
- Files cleaned up after processing (5 minute TTL)
- Directory created if not exists

## Data Models

### PDF Upload Model
```python
class PDFUpload:
    file: UploadFile
    max_size: int = 80 * 1024 * 1024  # 80MB
    allowed_types: list[str] = ["application/pdf"]
```

### Topic Request Model
```python
class TopicRequest:
    file: UploadFile
    topic: str
    max_topic_length: int = 200
```

### Mind Map Node Model
```python
class MindMapNode:
    id: int
    parent: int
    text: str
```

### Mind Map Model
```python
class MindMap:
    topic: str
    nodes: list[MindMapNode]
```

### Error Response Model
```python
class ErrorResponse:
    error: str
    message: str
    details: Optional[dict] = None
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: PDF format validation
*For any* uploaded file, the system should accept it if and only if it is a valid PDF format, rejecting all other file types with an appropriate error message.
**Validates: Requirements 1.2, 1.3**

### Property 2: Successful upload confirmation
*For any* valid PDF file under 80MB, uploading it should result in the file being stored temporarily and a confirmation with a unique identifier being returned.
**Validates: Requirements 1.5**

### Property 3: Whitespace topic rejection
*For any* string composed entirely of whitespace characters (spaces, tabs, newlines), submitting it as a topic should be rejected with a validation error.
**Validates: Requirements 2.2**

### Property 4: Topic truncation
*For any* topic string exceeding 200 characters, the system should truncate it to exactly 200 characters before processing.
**Validates: Requirements 2.3**

### Property 5: Topic detection returns results
*For any* PDF with extractable text content, the topic detection should return a non-empty list of topics.
**Validates: Requirements 2.4**

### Property 6: Minimum topic count
*For any* PDF document with sufficient content (more than 1000 words), the system should return at least 10 detected topics.
**Validates: Requirements 2.5**

### Property 7: Topic filtering relevance
*For any* PDF text and specified topic, the filtered content should only contain text segments that are semantically related to that topic.
**Validates: Requirements 3.1**

### Property 8: Filtered content minimum length
*For any* successful filtering operation where content is found, the returned filtered text should contain at least 50 characters.
**Validates: Requirements 3.4**

### Property 9: Input text truncation
*For any* text input to the filtering operation, if it exceeds 10000 tokens, the system should truncate it before processing.
**Validates: Requirements 3.5**

### Property 10: Mind map structure validity
*For any* generated mind map, it should contain a root topic string and a non-empty list of nodes, where each node has an id, parent, and text field.
**Validates: Requirements 4.1, 4.5**

### Property 11: Mind map referential integrity
*For any* generated mind map, all parent references in nodes should point to valid node IDs that exist in the same mind map, or be 0 for root-level nodes.
**Validates: Requirements 4.3**

### Property 12: Mind map hierarchy depth
*For any* mind map generated from content with sufficient complexity, the system should support at least 4 levels of hierarchy (root + 3 levels of children).
**Validates: Requirements 4.4**

### Property 13: AI response validation
*For any* AI-generated output (topics, filtered text, or mind map), the system should validate the response format and structure before returning it to the user, rejecting malformed responses.
**Validates: Requirements 5.3, 5.5**

### Property 14: AI retry on failure
*For any* AI operation that fails, the system should automatically retry the request exactly once before returning an error to the user.
**Validates: Requirements 5.4**

### Property 15: Error message safety
*For any* error that occurs during processing, the returned error message should not contain internal implementation details, stack traces, or file system paths.
**Validates: Requirements 6.2, 6.4**

### Property 16: Temporary file cleanup on error
*For any* processing operation that fails after creating temporary files, those temporary files should be removed from the file system.
**Validates: Requirements 6.3**

### Property 17: First error precedence
*For any* pipeline execution where multiple errors occur, the system should return the first critical error encountered and halt further processing.
**Validates: Requirements 6.5**

### Property 18: Interactive topic display
*For any* list of detected topics, the UI should render them as interactive, clickable elements that allow topic selection.
**Validates: Requirements 7.4**

### Property 19: Mind map visualization interactivity
*For any* generated mind map, the visualization should support zoom and pan operations, allowing users to navigate the entire structure.
**Validates: Requirements 7.5**

### Property 20: Download button availability
*For any* successfully generated mind map, the UI should display download buttons for both JSON and image formats.
**Validates: Requirements 8.1**

### Property 21: Download filename format
*For any* mind map download, the generated filename should include the topic name and a timestamp in a descriptive format.
**Validates: Requirements 8.4**

### Property 22: Temporary file cleanup after completion
*For any* temporary file created during processing, it should be deleted from the file system within 5 minutes of processing completion.
**Validates: Requirements 9.4**

## Error Handling

### Error Categories

**1. Validation Errors (400)**
- Invalid file format (non-PDF)
- Empty or whitespace-only topic
- Missing required parameters
- Malformed request data

**2. Client Errors (413, 404)**
- File size exceeds 80MB limit
- Topic not found in PDF content
- No extractable text in PDF

**3. Server Errors (500)**
- PDF corruption or read failure
- AI processing failure (after retry)
- JSON parsing failure
- Unexpected exceptions

**4. Timeout Errors (504)**
- Processing exceeds 60 second limit
- AI response timeout

### Error Handling Strategy

**Validation Layer:**
- Validate all inputs before processing
- Return clear, actionable error messages
- Use Pydantic models for request validation

**Processing Layer:**
- Wrap all block operations in try-except
- Log errors with context (timestamp, input summary)
- Clean up resources on failure
- Retry AI operations once on failure

**Response Layer:**
- Map exceptions to appropriate HTTP status codes
- Sanitize error messages (no internal details)
- Include error type and user-friendly message
- Log full error details server-side

### Error Response Format

```json
{
  "error": "ValidationError",
  "message": "Topic cannot be empty or contain only whitespace",
  "details": {
    "field": "topic",
    "provided_value": "   "
  }
}
```

## Testing Strategy

The testing strategy employs both unit testing and property-based testing to ensure comprehensive coverage of the system's correctness properties.

### Unit Testing Approach

Unit tests will verify specific examples, integration points, and edge cases:

**PDF Upload Tests:**
- Test successful upload with valid PDF
- Test rejection of non-PDF files
- Test file size limit enforcement (80MB boundary)
- Test temporary file creation and storage

**Topic Detection Tests:**
- Test topic extraction from sample PDF
- Test handling of PDFs with no text
- Test topic list format and structure

**Topic Filtering Tests:**
- Test filtering with known topic in sample PDF
- Test handling of non-existent topics
- Test preservation of context in filtered text

**Mind Map Generation Tests:**
- Test mind map structure with sample input
- Test JSON schema compliance
- Test node relationship integrity

**Error Handling Tests:**
- Test error responses for various failure scenarios
- Test cleanup of temporary files on errors
- Test error message sanitization

### Property-Based Testing Approach

Property-based tests will verify universal properties across all inputs using **Hypothesis** (Python's leading property-based testing library).

**Configuration:**
- Each property test will run a minimum of 100 iterations
- Tests will use Hypothesis strategies to generate diverse inputs
- Each test will be tagged with a comment referencing the design document property

**Property Test Requirements:**
- Each correctness property MUST be implemented by a SINGLE property-based test
- Each test MUST be tagged with: `# Feature: pdf-mindmap-generator, Property {number}: {property_text}`
- Tests MUST validate the universal quantification ("for any") specified in each property

**Property Test Coverage:**

1. **Input Validation Properties (Properties 1, 3, 4):**
   - Generate random files of various types
   - Generate random topic strings (valid, whitespace, long)
   - Verify validation behavior across all inputs

2. **Processing Properties (Properties 5-9):**
   - Generate random PDF content
   - Generate random topics
   - Verify filtering and detection behavior

3. **Output Structure Properties (Properties 10-12):**
   - Generate random mind map structures
   - Verify schema compliance
   - Verify referential integrity
   - Verify hierarchy depth

4. **Reliability Properties (Properties 13-18):**
   - Simulate AI failures
   - Simulate file system errors
   - Verify retry logic
   - Verify cleanup behavior
   - Verify error message safety

**Test Organization:**
```
tests/
├── unit/
│   ├── test_blocks.py
│   ├── test_pipelines.py
│   ├── test_api.py
│   └── test_file_handling.py
└── property/
    ├── test_validation_properties.py
    ├── test_processing_properties.py
    ├── test_output_properties.py
    └── test_reliability_properties.py
```

### Integration Testing

Integration tests will verify end-to-end workflows:
- Complete PDF upload → topic detection flow
- Complete PDF upload → mind map generation flow
- API endpoint integration with pipelines
- File cleanup after processing

### Test Data

**Sample PDFs:**
- Small PDF (1-2 pages) with clear topics
- Medium PDF (10-20 pages) with multiple sections
- Large PDF (50+ pages) for performance testing
- PDF with special characters and formatting
- Corrupted PDF for error handling

**Generated Test Data:**
- Random valid PDFs using reportlab or similar
- Random text content with known topics
- Random topic strings of various lengths
- Random mind map structures for validation

## Deployment Considerations

### Environment Setup

**Required Dependencies:**
```
python >= 3.9
fastapi
uvicorn
pdfplumber
kiro
hypothesis (for property testing)
pytest
```

### Configuration

**Environment Variables:**
- `TEMP_DIR`: Directory for temporary file storage (default: `./temp`)
- `MAX_FILE_SIZE`: Maximum PDF file size in bytes (default: 83886080 = 80MB)
- `AI_TIMEOUT`: Timeout for AI operations in seconds (default: 60)
- `FILE_CLEANUP_INTERVAL`: Interval for cleaning old temp files in seconds (default: 300 = 5 minutes)

### Streamlit Deployment

The application will be deployed on Streamlit Cloud with an interactive, colorful, and user-friendly interface.

**Frontend (Streamlit) - UI Design:**

**Color Scheme:**
- Primary: Vibrant blues and purples (#4A90E2, #7B68EE)
- Secondary: Warm oranges and greens (#FF6B6B, #51CF66)
- Background: Clean white with subtle gradients
- Accent: Bright yellows for highlights (#FFD93D)

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│  🧠 PDF Mind Map Generator              │
│  [Colorful header with gradient]        │
├─────────────────────────────────────────┤
│                                         │
│  📄 Upload Your PDF                     │
│  ┌─────────────────────────────────┐   │
│  │  Drag & Drop or Click to Upload │   │
│  │  [Interactive upload area]       │   │
│  └─────────────────────────────────┘   │
│                                         │
│  🎯 Choose Your Topic                   │
│  ┌─────────────────────────────────┐   │
│  │  Enter topic or select below... │   │
│  └─────────────────────────────────┘   │
│                                         │
│  💡 Detected Topics (clickable)         │
│  [Topic 1] [Topic 2] [Topic 3] ...     │
│  [Colorful, interactive buttons]        │
│                                         │
│  [Generate Mind Map Button - Large]    │
│                                         │
├─────────────────────────────────────────┤
│  🗺️ Your Mind Map                       │
│  ┌─────────────────────────────────┐   │
│  │                                 │   │
│  │  [Interactive visualization]    │   │
│  │  - Zoomable                     │   │
│  │  - Pannable                     │   │
│  │  - Colorful nodes               │   │
│  │  - Animated connections         │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [📥 Download JSON] [📥 Download PNG]  │
│                                         │
└─────────────────────────────────────────┘
```

**Interactive Components:**

1. **File Upload Area:**
   - Drag-and-drop zone with hover effects
   - Color changes on file hover (blue glow)
   - Success animation when file is uploaded
   - File name and size display with icon

2. **Topic Selection:**
   - Text input with autocomplete
   - Detected topics as colorful, clickable pills/badges
   - Each topic button has unique color from palette
   - Hover effects with scale animation
   - Selected topic highlights with border

3. **Loading States:**
   - Animated spinner with custom colors
   - Progress bar showing processing stages
   - Status messages: "Extracting text...", "Analyzing topics...", "Generating mind map..."
   - Smooth transitions between states

4. **Mind Map Visualization:**
   - Use streamlit-agraph or pyvis for interactive graphs
   - Nodes colored by hierarchy level:
     - Level 0 (root): Purple
     - Level 1: Blue
     - Level 2: Green
     - Level 3+: Orange/Yellow gradient
   - Node size based on importance/content length
   - Smooth edges with curved lines
   - Zoom controls (+ / - buttons)
   - Pan by dragging
   - Click nodes to highlight connections
   - Tooltip on hover showing full text

5. **Download Buttons:**
   - Two prominent buttons side-by-side
   - Icon + text labels
   - Hover effects with color shift
   - Download confirmation toast message
   - Filename format: `{topic_name}_mindmap_{timestamp}.{ext}`

**Backend Integration:**
- Streamlit app calls FastAPI endpoints via requests
- FastAPI runs as separate service (can be embedded for simple deployment)
- Temporary files stored in Streamlit's temp directory
- Session state management for uploaded files and generated mind maps

**Deployment Configuration:**
```python
# streamlit_app.py
import streamlit as st
import requests
from streamlit_agraph import agraph, Node, Edge, Config
import json
from datetime import datetime
import base64

# Custom CSS for colorful, interactive UI
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .stButton>button { 
        background: linear-gradient(90deg, #4A90E2 0%, #7B68EE 100%);
        color: white;
        border-radius: 20px;
        padding: 10px 30px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: scale(1.05); }
    .topic-pill {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 20px;
        background: #FF6B6B;
        color: white;
        cursor: pointer;
        transition: all 0.3s;
    }
    .topic-pill:hover { transform: scale(1.1); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
</style>
""", unsafe_allow_html=True)

# FastAPI backend URL
API_URL = "http://localhost:8000"  # or deployed URL

# App title with emoji
st.title("🧠 PDF Mind Map Generator")
st.markdown("### Transform your PDFs into beautiful, interactive mind maps!")

# File upload with custom styling
uploaded_file = st.file_uploader(
    "📄 Upload Your PDF",
    type="pdf",
    help="Upload a PDF document to analyze"
)

if uploaded_file:
    # Show file info
    st.success(f"✅ Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
    
    # Detect topics button
    if st.button("🔍 Detect Topics", key="detect"):
        with st.spinner("🔄 Analyzing your PDF..."):
            # Call API
            files = {"file": uploaded_file}
            response = requests.post(f"{API_URL}/pdf/topics", files=files)
            if response.ok:
                topics = response.json()["topics"]
                st.session_state.topics = topics
    
    # Display detected topics as interactive buttons
    if "topics" in st.session_state:
        st.markdown("### 💡 Detected Topics (click to select)")
        cols = st.columns(3)
        for idx, topic in enumerate(st.session_state.topics):
            with cols[idx % 3]:
                if st.button(topic, key=f"topic_{idx}"):
                    st.session_state.selected_topic = topic
    
    # Topic input
    topic = st.text_input(
        "🎯 Or Enter Your Topic",
        value=st.session_state.get("selected_topic", ""),
        placeholder="e.g., Machine Learning, Photosynthesis..."
    )
    
    # Generate mind map
    if topic and st.button("🚀 Generate Mind Map", key="generate"):
        with st.spinner("🎨 Creating your mind map..."):
            files = {"file": uploaded_file}
            data = {"topic": topic}
            response = requests.post(f"{API_URL}/pdf/mindmap", files=files, params=data)
            if response.ok:
                mindmap = response.json()["mindmap"]
                st.session_state.mindmap = mindmap
                st.session_state.topic_name = topic
    
    # Display mind map
    if "mindmap" in st.session_state:
        st.markdown("### 🗺️ Your Interactive Mind Map")
        
        # Convert to graph format
        mindmap = st.session_state.mindmap
        nodes = []
        edges = []
        colors = ["#7B68EE", "#4A90E2", "#51CF66", "#FFD93D", "#FF6B6B"]
        
        # Create nodes with colors based on level
        for node in mindmap["nodes"]:
            level = 0  # Calculate level from parent chain
            color = colors[min(level, len(colors)-1)]
            nodes.append(Node(
                id=node["id"],
                label=node["text"],
                size=25,
                color=color
            ))
            if node["parent"] != 0:
                edges.append(Edge(source=node["parent"], target=node["id"]))
        
        # Display interactive graph
        config = Config(
            width=800,
            height=600,
            directed=True,
            physics=True,
            hierarchical=True
        )
        agraph(nodes=nodes, edges=edges, config=config)
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            # JSON download
            json_str = json.dumps(mindmap, indent=2)
            b64 = base64.b64encode(json_str.encode()).decode()
            filename = f"{st.session_state.topic_name}_mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            href = f'<a href="data:application/json;base64,{b64}" download="{filename}">📥 Download JSON</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            # PNG download (would need additional library for graph to image)
            st.button("📥 Download PNG", help="Export as image")

# Error handling
if "error" in st.session_state:
    st.error(f"❌ {st.session_state.error}")
```

### Performance Optimization

**Caching:**
- Cache extracted PDF text for repeated requests
- Cache detected topics for same PDF

**Async Processing:**
- Use FastAPI's async capabilities for I/O operations
- Process multiple PDFs concurrently

**Resource Management:**
- Implement file cleanup background task
- Limit concurrent AI requests
- Set memory limits for PDF processing

## Security Considerations

**File Upload Security:**
- Validate file type and size before processing
- Sanitize filenames to prevent path traversal
- Store uploads in isolated temporary directory
- Implement rate limiting on upload endpoints

**Input Sanitization:**
- Validate and sanitize topic strings
- Prevent injection attacks in AI prompts
- Limit input text size to prevent DoS

**Error Information Disclosure:**
- Never expose internal paths or stack traces
- Log sensitive errors server-side only
- Return generic error messages to clients

**Resource Limits:**
- Enforce file size limits (50MB)
- Enforce processing timeouts (60 seconds)
- Limit concurrent requests per client
- Clean up temporary files regularly
