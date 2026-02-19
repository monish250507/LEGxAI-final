from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import os
import re
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from config import UPLOAD_DIR

# Try to import aiofiles, but provide fallback
try:
    import aiofiles
    AIOFILES_AVAILABLE = True
except ImportError:
    AIOFILES_AVAILABLE = False
    aiofiles = None
    logging.warning("aiofiles not available - using synchronous file operations")

from services.document_analysis_service import document_analysis_service

# Configure logging
logger = logging.getLogger(__name__)

# Response models for type safety
class ClauseResponse(BaseModel):
    clause_id: str
    text: str
    type: str
    confidence: float
    priority_score: float
    color: str
    rank: int
    explanation: Optional[str] = None

class DocumentStatsResponse(BaseModel):
    total_characters: int
    total_clauses: int
    classified_clauses: int
    ranked_clauses: int

class SummaryResponse(BaseModel):
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    clause_types: list

class UploadResponse(BaseModel):
    status: str
    filename: str
    document_stats: DocumentStatsResponse
    clauses: list[ClauseResponse]
    summary: SummaryResponse

router = APIRouter()

# File validation settings
ALLOWED_EXT = {"pdf", "txt", "docx", "json", "ppt", "pptx", "jpg", "jpeg", "png"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def allowed(filename: str) -> bool:
    """Check if file extension is allowed."""
    if not filename:
        return False
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    if not filename:
        return "unknown_file"
    
    # Remove path separators and special characters
    safe_name = filename.replace(" ", "_").replace("/", "_").replace("\\", "_")
    safe_name = safe_name.replace("..", "_").replace("__", "_")
    
    # Keep only alphanumeric, underscores, and dots
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9_.]', '_', safe_name)
    
    return safe_name

async def save_file_safely(file: UploadFile, upload_dir: str, filename: str) -> str:
    """Safely save uploaded file to upload directory."""
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    try:
        if AIOFILES_AVAILABLE:
            async with aiofiles.open(file_path, 'wb') as buffer:
                content = await file.read()
                await buffer.write(content)
        else:
            # Fallback to synchronous operations
            content = await file.read()
            with open(file_path, 'wb') as buffer:
                buffer.write(content)
        return file_path
    except Exception as e:
        logger.error(f"Failed to save file {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        # Reset file pointer for potential reuse
        await file.seek(0)

@router.post("/upload", response_model=UploadResponse)
async def upload_and_analyze_file(file: UploadFile = File(...), constitution: str = Form(...)):
    """
    Upload file and perform complete clause analysis with constitution context.
    
    Args:
        file: Uploaded file
        constitution: Selected constitution for legal analysis
        
    Returns structured JSON with clause_id, text, type, confidence, priority_score, color, rank
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not allowed(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Sanitize filename
    safe_filename = sanitize_filename(file.filename)
    
    try:
        # Validate file size
        if hasattr(file, 'size') and file.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Save file safely
        file_path = await save_file_safely(file, UPLOAD_DIR, safe_filename)
        logger.info(f"File saved: {file_path}")
        
        # Analyze document using the service
        analysis_result = await document_analysis_service.analyze_document(file, constitution)
        
        # Validate analysis result structure
        if not isinstance(analysis_result, dict):
            raise HTTPException(status_code=500, detail="Invalid analysis result")
        
        required_keys = ['status', 'filename', 'document_stats', 'clauses', 'summary']
        for key in required_keys:
            if key not in analysis_result:
                raise HTTPException(status_code=500, detail=f"Missing required field: {key}")
        
        logger.info(f"Successfully analyzed document: {safe_filename}")
        return analysis_result
        
    except ValueError as e:
        logger.error(f"Document analysis error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing file {safe_filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/upload-simple")
async def upload_file_simple(file: UploadFile = File(...)):
    """
    Simple file upload endpoint without analysis (for backward compatibility).
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not allowed(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    safe_filename = sanitize_filename(file.filename)
    
    try:
        file_path = await save_file_safely(file, UPLOAD_DIR, safe_filename)
        return {"status": "ok", "path": file_path, "filename": safe_filename}
    except Exception as e:
        logger.error(f"Simple upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@router.get("/upload/formats")
def get_supported_formats():
    """Get list of supported file formats."""
    return {
        "supported_formats": document_analysis_service.get_supported_formats(),
        "max_file_size_bytes": MAX_FILE_SIZE,
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024)
    }
