"""
FastAPI application for PDF Mind Map Generator.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import os

from pipelines.pdf_to_topics import pdf_to_topics
from pipelines.topic_to_mindmap import topic_to_mindmap
from utils.validation import validate_file_upload, validate_topic
from utils.file_manager import save_uploaded_file, cleanup_file, cleanup_old_files
from utils.error_handler import create_error_response, log_error, ValidationError


# Create FastAPI app
app = FastAPI(
    title="PDF Mind Map Generator",
    description="AI-powered tool to transform PDF documents into interactive mind maps",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Run cleanup on startup."""
    cleanup_old_files()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PDF Mind Map Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/pdf/topics": "POST - Upload PDF and get detected topics",
            "/pdf/mindmap": "POST - Upload PDF with topic and generate mind map"
        }
    }


@app.post("/pdf/topics")
async def get_topics(file: UploadFile = File(...)):
    """
    Upload PDF and get list of detected topics.
    
    Args:
        file: PDF file to analyze
        
    Returns:
        JSON with list of detected topics
    """
    file_path = None
    
    try:
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file upload
        is_valid, error_message = validate_file_upload(file.filename, file_size)
        if not is_valid:
            raise ValidationError(error_message, {"field": "file", "filename": file.filename})
        
        # Save uploaded file
        file_path = save_uploaded_file(file_content, file.filename)
        
        # Run pipeline
        result = pdf_to_topics(file_path)
        
        # Cleanup file
        cleanup_file(file_path)
        
        return result
        
    except ValidationError as e:
        log_error(e, {"endpoint": "/pdf/topics", "filename": file.filename})
        if file_path:
            cleanup_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(e)
        )
    except Exception as e:
        log_error(e, {"endpoint": "/pdf/topics", "filename": file.filename})
        if file_path:
            cleanup_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(e)
        )


@app.post("/pdf/mindmap")
async def get_mindmap(
    file: UploadFile = File(...),
    topic: str = Form(...)
):
    """
    Upload PDF with topic and generate mind map.
    
    Args:
        file: PDF file to analyze
        topic: Topic to generate mind map for
        
    Returns:
        JSON with mind map structure
    """
    file_path = None
    
    try:
        # Validate topic
        is_valid, processed_topic, error_message = validate_topic(topic)
        if not is_valid:
            raise ValidationError(error_message, {"field": "topic", "provided_value": topic})
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file upload
        is_valid, error_message = validate_file_upload(file.filename, file_size)
        if not is_valid:
            raise ValidationError(error_message, {"field": "file", "filename": file.filename})
        
        # Save uploaded file
        file_path = save_uploaded_file(file_content, file.filename)
        
        # Run pipeline
        result = topic_to_mindmap(file_path, processed_topic)
        
        # Cleanup file
        cleanup_file(file_path)
        
        return result
        
    except ValidationError as e:
        log_error(e, {"endpoint": "/pdf/mindmap", "filename": file.filename, "topic": topic})
        if file_path:
            cleanup_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_error_response(e)
        )
    except ValueError as e:
        # Topic not found in PDF
        log_error(e, {"endpoint": "/pdf/mindmap", "filename": file.filename, "topic": topic})
        if file_path:
            cleanup_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response(e)
        )
    except Exception as e:
        log_error(e, {"endpoint": "/pdf/mindmap", "filename": file.filename, "topic": topic})
        if file_path:
            cleanup_file(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_error_response(e)
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
