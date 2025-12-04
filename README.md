# PDF Mind Map Generator 🧠

An AI-powered tool for college students to transform PDF documents into interactive, visual mind maps.

## 🚀 Quick Start

**New here?** Read **[START_HERE.md](START_HERE.md)** for complete setup guide!

**Just need AI key?** Read **[QUICK_FIX.md](QUICK_FIX.md)** for 5-minute setup!

## Features

- 📄 Upload PDF documents (up to 80MB)
- 🎯 Automatic topic detection using AI (Llama 3)
- 🗺️ Generate hierarchical mind maps in JSON format
- 🎨 Interactive, colorful web interface
- 📥 Download mind maps as JSON or images
- ⚡ Fast processing with Kiro Blocks architecture

## Tech Stack

- **Backend**: Python, FastAPI, Kiro Blocks
- **AI**: Llama 3 (via Kiro)
- **PDF Processing**: pdfplumber
- **Frontend**: Streamlit
- **Visualization**: streamlit-agraph
- **Testing**: pytest, Hypothesis (property-based testing)

## Project Structure

```
.
├── blocks/              # Kiro blocks for processing
├── pipelines/           # Kiro pipelines
├── api/                 # FastAPI endpoints
├── utils/               # Utility modules
├── tests/               # Test suite
│   ├── unit/           # Unit tests
│   └── property/       # Property-based tests
├── temp/                # Temporary file storage
├── streamlit_app.py     # Streamlit frontend
└── requirements.txt     # Python dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and configure as needed

## Usage

### Quick Start

1. **Run the Backend (FastAPI):**
   ```bash
   python run_backend.py
   ```
   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

2. **Run the Frontend (Streamlit):**
   ```bash
   python run_frontend.py
   ```
   The frontend will be available at `http://localhost:8501`

### Alternative: Manual Start

**Backend:**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
streamlit run streamlit_app.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run property-based tests only
pytest tests/property/

# Run with coverage
pytest --cov=. --cov-report=html
```

## API Endpoints

### POST /pdf/topics
Upload a PDF and get detected topics.

**Request:**
- `file`: PDF file (multipart/form-data)

**Response:**
```json
{
  "topics": ["Topic 1", "Topic 2", ...]
}
```

### POST /pdf/mindmap
Upload a PDF with a topic and generate a mind map.

**Request:**
- `file`: PDF file (multipart/form-data)
- `topic`: Topic string (query parameter)

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

## Development

This project follows spec-driven development with:
- Formal requirements (EARS format)
- Comprehensive design document
- Property-based testing for correctness
- Incremental task-based implementation

See `.kiro/specs/pdf-mindmap-generator/` for full specifications.

## License

MIT License


## ⚠️ IMPORTANT: AI Configuration Required

The app needs an AI API key to work properly. Without it, you'll get generic/mock results.

**Quick Setup (5 minutes):**
1. Get FREE Groq API key from [console.groq.com](https://console.groq.com)
2. Add to Streamlit Cloud Secrets (see `QUICK_FIX.md`)
3. Done! Your app will now analyze PDFs correctly ✅

**See:** `QUICK_FIX.md` for step-by-step instructions

## Deployment to Streamlit Cloud

The app now runs in **standalone mode** - no separate backend needed!

### Steps to Deploy:

1. **Push your code to GitHub**

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Click "New app"**

4. **Configure:**
   - Repository: Your GitHub repo
   - Branch: main (or your branch)
   - Main file path: `streamlit_app.py`

5. **Click "Deploy"**

That's it! Streamlit Cloud will automatically:
- Install dependencies from `requirements.txt`
- Install system packages from `packages.txt`
- Run your app

### Important Files for Deployment:
- `streamlit_app.py` - Main app (standalone version)
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies (poppler-utils for PDF processing)
- `blocks/` - Processing modules
- `utils/` - Utility modules

### Note:
The standalone version (`streamlit_app.py`) runs all processing directly without needing FastAPI. If you want to run with a separate backend locally, use `streamlit_app_api.py` instead.
