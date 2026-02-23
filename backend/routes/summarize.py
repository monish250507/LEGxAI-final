from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.ai_pipeline import summarize_text
from clause_extractor import extract_clauses

class SummarizeRequest(BaseModel):
    document_text: Optional[str] = None
    text: Optional[str] = None

router = APIRouter()

@router.post("/summarize")
def summarize(request: SummarizeRequest):
    text = request.document_text or request.text
    if not text:
        raise HTTPException(status_code=400, detail="document_text required")
    
    summary = summarize_text(text)
    clauses = extract_clauses(text)
    return {"summary": summary, "clauses": clauses}
