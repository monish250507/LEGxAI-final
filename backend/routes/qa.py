from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_pipeline import answer_query

class QARequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/qa")
def qa(request: QARequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="query required")
    
    answer = answer_query(request.query, k=5)
    return {"query": request.query, "answer": answer}
