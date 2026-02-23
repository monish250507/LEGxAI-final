"""
Chatbot API Routes - Interactive Legal Document Analysis

Provides REST API endpoints for the chatbot service including:
- Session management
- Multi-turn conversation
- Context-aware clause analysis
- Document summaries
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from ai.chatbot_service import get_chatbot_service, ChatbotService

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

# Pydantic models for request/response
class SessionCreateRequest(BaseModel):
    document_text: str
    constitution: str
    clauses: List[Dict[str, Any]]

class SessionCreateResponse(BaseModel):
    session_id: str
    message: str

class MessageRequest(BaseModel):
    session_id: str
    message: str

class MessageResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

class ClauseAnalysisRequest(BaseModel):
    session_id: str
    clause_text: str
    question: str

class ClauseAnalysisResponse(BaseModel):
    clause_text: str
    question: str
    analysis: str
    clause_type: str
    risk_level: str
    constitution_reference: str
    context: Dict[str, Any]

class DocumentSummaryResponse(BaseModel):
    document_info: Dict[str, Any]
    key_insights: Dict[str, Any]
    session_info: Dict[str, Any]

class SessionStatsResponse(BaseModel):
    session_id: str
    total_messages: int
    last_activity: str
    document_clauses: int
    performance_stats: Dict[str, Any]

# Dependency injection
async def get_chatbot() -> ChatbotService:
    """Get chatbot service instance."""
    return get_chatbot_service()

@router.post("/session/create", response_model=SessionCreateResponse)
async def create_session(
    request: SessionCreateRequest,
    chatbot: ChatbotService = Depends(get_chatbot)
):
    """
    Create a new chat session with document context.
    
    Args:
        request: Session creation request with document context
        
    Returns:
        Session ID and confirmation message
    """
    try:
        session_id = chatbot.create_session(
            document_text=request.document_text,
            constitution=request.constitution,
            clauses=request.clauses
        )
        
        logger.info(f"Created chat session: {session_id}")
        
        return SessionCreateResponse(
            session_id=session_id,
            message="Chat session created successfully. You can now start asking questions about your document."
        )
        
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

@router.post("/message", response_model=MessageResponse)
async def send_message(
    request: MessageRequest,
    chatbot: ChatbotService = Depends(get_chatbot)
):
    """
    Send a message in the chat session.
    
    Args:
        request: Message with session ID and content
        
    Returns:
        AI response with session context
    """
    try:
        # Add user message
        chatbot.add_message(request.session_id, "user", request.message)
        
        # Generate response (simple implementation - in production, use more sophisticated logic)
        from datetime import datetime
        
        # For now, provide a simple response
        response_text = f"I understand you're asking about: {request.message}. This is a basic response. In a full implementation, I would provide detailed analysis based on your document context."
        
        # Add assistant response
        chatbot.add_message(request.session_id, "assistant", response_text)
        
        return MessageResponse(
            response=response_text,
            session_id=request.session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to process message: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@router.post("/analyze-clause", response_model=ClauseAnalysisResponse)
async def analyze_clause(
    request: ClauseAnalysisRequest,
    chatbot: ChatbotService = Depends(get_chatbot)
):
    """
    Analyze a specific clause within conversation context.
    
    Args:
        request: Clause analysis request with session context
        
    Returns:
        Comprehensive clause analysis
    """
    try:
        result = chatbot.analyze_clause_in_context(
            session_id=request.session_id,
            clause_text=request.clause_text,
            question=request.question
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return ClauseAnalysisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to analyze clause: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze clause: {str(e)}")

@router.get("/session/{session_id}/summary", response_model=DocumentSummaryResponse)
async def get_document_summary(
    session_id: str,
    chatbot: ChatbotService = Depends(get_chatbot)
):
    """
    Get document summary and analysis insights.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Document summary with key insights
    """
    try:
        summary = chatbot.get_document_summary(session_id)
        return DocumentSummaryResponse(**summary)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get document summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get document summary: {str(e)}")

@router.get("/session/{session_id}/history")
async def get_conversation_history(
    session_id: str,
    limit: int = 10,
    chatbot: ChatbotService = Depends(get_chatbot)
):
    """
    Get conversation history for a session.
    
    Args:
        session_id: Session identifier
        limit: Maximum number of messages to return
        
    Returns:
        List of recent messages
    """
    try:
        history = chatbot.get_conversation_history(session_id, limit)
        
        return {
            "session_id": session_id,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "metadata": msg.metadata
                }
                for msg in history
            ],
            "total_messages": len(history)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get conversation history: {str(e)}")

@router.get("/session/{session_id}/stats", response_model=SessionStatsResponse)
async def get_session_stats(
    session_id: str,
    chatbot: ChatbotService = Depends(get_chatbot)
):
    """
    Get session statistics and performance metrics.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Session statistics
    """
    try:
        stats = chatbot.get_session_stats(session_id)
        return SessionStatsResponse(**stats)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get session stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get session stats: {str(e)}")

@router.delete("/session/{session_id}")
async def clear_session(
    session_id: str,
    chatbot: ChatbotService = Depends(get_chatbot)
):
    """
    Clear a chat session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Confirmation message
    """
    try:
        chatbot.clear_session(session_id)
        
        return {
            "message": f"Session {session_id} cleared successfully",
            "session_id": session_id
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to clear session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear session: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for chatbot service."""
    return {
        "status": "healthy",
        "service": "chatbot",
        "timestamp": "2024-01-01T00:00:00Z"
    }
