# Minimal version of ai_pipeline for testing without external dependencies
import json

def _call_chat(prompt: str, system: str = "You are an assistant.", max_tokens: int = 512, temperature: float = 0.2):
    """Mock implementation for testing"""
    return "Mock AI response - OpenAI API key not configured"

def summarize_text(document_text: str) -> str:
    """Mock implementation for testing"""
    return "Mock summary of the legal document"

def extract_clauses(document_text: str):
    """Mock implementation for testing"""
    return {
        "obligations": [{"text": "Mock obligation clause", "section": "Section 1"}],
        "rights": [{"text": "Mock right clause", "section": "Section 2"}],
        "prohibitions": [{"text": "Mock prohibition clause", "section": "Section 3"}],
        "dates": [{"text": "Mock date clause", "section": "Section 4"}],
        "parties": [{"text": "Mock party clause", "section": "Section 5"}]
    }

def answer_query(query: str, k: int = 5) -> str:
    """Mock implementation for testing"""
    return f"Mock answer to query: {query}"
