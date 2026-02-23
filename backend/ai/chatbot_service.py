"""
Chatbot Service - Interactive Legal Document Analysis

Provides conversational interface for legal document analysis with context awareness
and multi-turn conversation capabilities.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from .generative_service import GenerativeService, generate_full_clause_analysis
from .constitution_matcher import ConstitutionMatcher
from .performance_optimizer import get_performance_optimizer

logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Represents a chat message in the conversation."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ConversationContext:
    """Represents the conversation context."""
    document_text: str
    constitution: str
    clauses: List[Dict[str, Any]]
    session_id: str
    created_at: str
    last_updated: str

class ChatbotService:
    """
    Interactive chatbot service for legal document analysis.
    
    Features:
    - Multi-turn conversation with context awareness
    - Clause-specific analysis
    - Constitution-aware responses
    - Performance optimization with caching
    - Session management
    """
    
    def __init__(self):
        self.generative_service = GenerativeService()
        self.constitution_matcher = ConstitutionMatcher()
        self.performance_optimizer = get_performance_optimizer()
        
        # Conversation storage (in production, use Redis or database)
        self.conversations: Dict[str, Dict[str, Any]] = {}
        self.contexts: Dict[str, ConversationContext] = {}
        
        # Initialize constitution matcher
        if self.constitution_matcher:
            self.constitution_matcher.load_constitutions()
    
    def create_session(self, document_text: str, constitution: str, clauses: List[Dict[str, Any]]) -> str:
        """
        Create a new chat session with document context.
        
        Args:
            document_text: Full document text
            constitution: Selected constitution
            clauses: Analyzed clauses from document
            
        Returns:
            Session ID for the conversation
        """
        import uuid
        session_id = str(uuid.uuid4())
        
        # Store conversation context
        context = ConversationContext(
            document_text=document_text,
            constitution=constitution,
            clauses=clauses,
            session_id=session_id,
            created_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        self.contexts[session_id] = context
        self.conversations[session_id] = {
            'messages': [],
            'metadata': {
                'total_messages': 0,
                'last_activity': datetime.now().isoformat()
            }
        }
        
        logger.info(f"Created chat session: {session_id}")
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Add a message to the conversation.
        
        Args:
            session_id: Session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional metadata
        """
        if session_id not in self.conversations:
            raise ValueError(f"Session {session_id} not found")
        
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            metadata=metadata
        )
        
        self.conversations[session_id]['messages'].append(asdict(message))
        self.conversations[session_id]['metadata']['total_messages'] += 1
        self.conversations[session_id]['metadata']['last_activity'] = datetime.now().isoformat()
        
        # Update context timestamp
        if session_id in self.contexts:
            self.contexts[session_id].last_updated = datetime.now().isoformat()
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """
        Get conversation history for context.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of recent messages
            
        Returns:
            List of recent messages
        """
        if session_id not in self.conversations:
            return []
        
        messages = self.conversations[session_id]['messages']
        recent_messages = messages[-limit:] if len(messages) > limit else messages
        
        return [ChatMessage(**msg) for msg in recent_messages]
    
    def analyze_clause_in_context(self, session_id: str, clause_text: str, question: str) -> Dict[str, Any]:
        """
        Analyze a specific clause within conversation context.
        
        Args:
            session_id: Session identifier
            clause_text: Clause text to analyze
            question: User's specific question about the clause
            
        Returns:
            Comprehensive analysis response
        """
        if session_id not in self.contexts:
            raise ValueError(f"Session {session_id} not found")
        
        context = self.contexts[session_id]
        
        # Find matching clause in document
        matching_clause = None
        for clause in context.clauses:
            if clause_text.lower() in clause.get('text', '').lower():
                matching_clause = clause
                break
        
        if not matching_clause:
            return {
                "error": "Clause not found in document",
                "suggestion": "Please provide a clause that exists in the uploaded document"
            }
        
        # Get conversation history for context
        history = self.get_conversation_history(session_id, limit=5)
        
        # Build context-aware prompt
        context_prompt = self._build_context_prompt(
            context, matching_clause, question, history
        )
        
        # Check cache first
        cache_key = f"{session_id}:{clause_text[:100]}:{question[:100]}"
        cached_response = self.performance_optimizer.get_cached_api_response(
            cache_key, context.constitution, "contextual_analysis"
        )
        
        if cached_response:
            logger.info("Using cached contextual analysis")
            return cached_response
        
        # Generate contextual analysis
        messages = [
            {
                "role": "system",
                "content": "You are an expert legal assistant providing contextual analysis of legal clauses. Consider the conversation history and document context in your response."
            },
            {
                "role": "user",
                "content": context_prompt
            }
        ]
        
        # Use generative service for analysis
        analysis = self.generative_service._call_model(
            self.generative_service.primary_model,
            messages,
            max_tokens=1000,
            timeout=60
        )
        
        if not analysis:
            analysis = self.generative_service._call_model(
                self.generative_service.fallback_model,
                messages,
                max_tokens=1000,
                timeout=60
            )
        
        response = {
            "clause_text": clause_text,
            "question": question,
            "analysis": analysis or "I apologize, but I'm unable to provide analysis at this time.",
            "clause_type": matching_clause.get('type', 'unknown'),
            "risk_level": matching_clause.get('risk_level', 'unknown'),
            "constitution_reference": matching_clause.get('constitution_reference', ''),
            "context": {
                "session_id": session_id,
                "conversation_turn": len(self.conversations[session_id]['messages']) + 1
            }
        }
        
        # Cache the response
        self.performance_optimizer.cache_api_response(
            cache_key, context.constitution, "contextual_analysis", response
        )
        
        return response
    
    def _build_context_prompt(self, context: ConversationContext, clause: Dict, question: str, history: List[ChatMessage]) -> str:
        """
        Build a context-aware prompt for analysis.
        
        Args:
            context: Conversation context
            clause: Clause being analyzed
            question: User's question
            history: Conversation history
            
        Returns:
            Context-aware prompt
        """
        prompt = f"""I'm analyzing a legal document with the following context:

Document Context:
- Constitution: {context.constitution}
- Total clauses analyzed: {len(context.clauses)}

Current Clause:
"{clause.get('text', '')}"
- Type: {clause.get('type', 'unknown')}
- Risk Level: {clause.get('risk_level', 'unknown')}
- Constitution Reference: {clause.get('constitution_reference', 'No reference')}

User's Question: {question}

"""
        
        if history:
            prompt += "Recent Conversation:\n"
            for msg in history[-3:]:  # Last 3 messages for context
                prompt += f"{msg.role}: {msg.content}\n"
            prompt += "\n"
        
        prompt += """Please provide a comprehensive analysis addressing the user's specific question. Consider:
1. The clause's legal implications
2. Constitutional relevance
3. Potential risks and benefits
4. Practical advice based on the conversation context

Be thorough but concise, and directly address the user's question."""
        
        return prompt
    
    def get_document_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get a summary of the document and analysis.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Document summary with key insights
        """
        if session_id not in self.contexts:
            raise ValueError(f"Session {session_id} not found")
        
        context = self.contexts[session_id]
        
        # Analyze document characteristics
        total_clauses = len(context.clauses)
        high_risk_clauses = [c for c in context.clauses if c.get('risk_level') == 'high']
        medium_risk_clauses = [c for c in context.clauses if c.get('risk_level') == 'medium']
        
        # Get clause types distribution
        clause_types = {}
        for clause in context.clauses:
            clause_type = clause.get('type', 'unknown')
            clause_types[clause_type] = clause_types.get(clause_type, 0) + 1
        
        summary = {
            "document_info": {
                "constitution": context.constitution,
                "total_clauses": total_clauses,
                "high_risk_clauses": len(high_risk_clauses),
                "medium_risk_clauses": len(medium_risk_clauses),
                "clause_types": clause_types
            },
            "key_insights": {
                "most_common_clause_type": max(clause_types.items(), key=lambda x: x[1])[0] if clause_types else None,
                "risk_distribution": {
                    "high": len(high_risk_clauses),
                    "medium": len(medium_risk_clauses),
                    "low": total_clauses - len(high_risk_clauses) - len(medium_risk_clauses)
                }
            },
            "session_info": {
                "session_id": session_id,
                "created_at": context.created_at,
                "last_updated": context.last_updated,
                "total_messages": self.conversations[session_id]['metadata']['total_messages']
            }
        }
        
        return summary
    
    def clear_session(self, session_id: str):
        """
        Clear a chat session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
        
        if session_id in self.contexts:
            del self.contexts[session_id]
        
        logger.info(f"Cleared chat session: {session_id}")
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """
        Get session statistics.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session statistics
        """
        if session_id not in self.conversations:
            raise ValueError(f"Session {session_id} not found")
        
        conv_data = self.conversations[session_id]
        context = self.contexts.get(session_id)
        
        stats = {
            "session_id": session_id,
            "total_messages": conv_data['metadata']['total_messages'],
            "last_activity": conv_data['metadata']['last_activity'],
            "document_clauses": len(context.clauses) if context else 0,
            "performance_stats": self.performance_optimizer.get_performance_stats()
        }
        
        return stats

# Global chatbot service instance
chatbot_service = ChatbotService()

def get_chatbot_service() -> ChatbotService:
    """Get the global chatbot service instance."""
    return chatbot_service
