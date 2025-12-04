# Quick Start Guide

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -c "import fastapi, streamlit, pdfplumber; print('All dependencies installed!')"
   ```

## Running the Application

### Option 1: Using Helper Scripts (Recommended)

1. **Start the Backend (Terminal 1):**
   ```bash
   python run_backend.py
   ```
   Wait for the message: "Application startup complete"

2. **Start the Frontend (Terminal 2):**
   ```bash
   python run_frontend.py
   ```
   Your browser should open automatically to `http://localhost:8501`

### Option 2: Manual Start

1. **Backend:**
   ```bash
   uvicorn api.main:app --reload
   ```

2. **Frontend:**
   ```bash
   streamlit run streamlit_app.py
   ```

## Using the Application

1. **Upload a PDF:**
   - Click "Choose a PDF file" or drag and drop
   - Maximum file size: 80MB

2. **Detect Topics:**
   - Click "🔍 Detect Topics" to automatically find topics in your PDF
   - Or manually enter a topic in the text field

3. **Generate Mind Map:**
   - Select a detected topic or enter your own
   - Click "🚀 Generate Mind Map"
   - Wait for the AI to process (usually 5-15 seconds)

4. **Download:**
   - Click "📥 Download JSON" to save your mind map

## Troubleshooting

### Backend won't start
- Check if port 8000 is already in use
- Try: `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)

### Frontend won't start
- Check if port 8501 is already in use
- Try: `netstat -ano | findstr :8501` (Windows) or `lsof -i :8501` (Mac/Linux)

### "Module not found" errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### API connection errors
- Make sure the backend is running first
- Check that API_URL in `.env` matches your backend address

## Testing

Run the test suite:
```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Property-based tests only
pytest tests/property/

# With coverage
pytest --cov=. --cov-report=html
```

## Next Steps

- Check out the [full README](README.md) for more details
- View API documentation at `http://localhost:8000/docs`
- Explore the spec files in `.kiro/specs/pdf-mindmap-generator/`
