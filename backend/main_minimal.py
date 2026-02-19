from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from config import UPLOAD_DIR

# Create FastAPI app
app = FastAPI(
    title="Legal AI API",
    description="AI-powered legal document analysis API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers with minimal dependencies
from routes.health import router as health_router

# Create minimal routers for testing
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

class SummarizeRequest(BaseModel):
    document_text: Optional[str] = None
    text: Optional[str] = None

class QARequest(BaseModel):
    query: str

# Mock services
def summarize_text(text):
    return "Mock summary"

def extract_clauses(text):
    return {"obligations": [], "rights": [], "prohibitions": [], "dates": [], "parties": []}

def answer_query(query, k=5):
    return f"Mock answer to: {query}"

# Create routers
summarize_router = APIRouter()
@summarize_router.post("/summarize")
def summarize(request: SummarizeRequest):
    text = request.document_text or request.text
    if not text:
        raise HTTPException(status_code=400, detail="document_text required")
    
    summary = summarize_text(text)
    clauses = extract_clauses(text)
    return {"summary": summary, "clauses": clauses}

qa_router = APIRouter()
@qa_router.post("/qa")
def qa(request: QARequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="query required")
    
    answer = answer_query(request.query, k=5)
    return {"query": request.query, "answer": answer}

upload_router = APIRouter()
@upload_router.post("/upload")
def upload_file():
    return {"status": "ok", "message": "Mock upload endpoint"}

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(summarize_router, prefix="/api")
app.include_router(qa_router, prefix="/api")
app.include_router(upload_router, prefix="/api")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Legal AI API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
