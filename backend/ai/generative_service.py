"""
Generative Service - Multi-Model AI Reasoning with OpenRouter

Supports Claude 3.5 Sonnet (primary) and Llama 3.1 70B (fallback)
Provides comprehensive legal analysis with offensive/defensive perspectives
"""

import logging
import requests
import json
import os
from typing import Optional, Dict, Any
from enum import Enum
from performance_optimizer import get_performance_optimizer

# Configure logging
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

class GenerativeService:
    """
    Multi-model generative service for comprehensive legal clause analysis.
    
    Primary model: anthropic/claude-3.5-sonnet
    Fallback model: meta-llama/llama-3.1-70b-instruct
    """
    
    def __init__(self):
        # Load API key from environment
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Model configuration
        self.primary_model = "anthropic/claude-3.5-sonnet"
        self.fallback_model = "meta-llama/llama-3.1-70b-instruct"
        
        # API availability
        self.api_available = bool(self.api_key)
        self.api_validated = False
        
        # Performance optimizer
        self.performance_optimizer = get_performance_optimizer()
        
        if not self.api_available:
            logger.warning("OPENROUTER_API_KEY not found. Generative AI will use fallback mode.")
        else:
            logger.info("OpenRouter API key loaded. Validating connection...")
            self.validate_openrouter_connection()
    
    def validate_openrouter_connection(self) -> bool:
        """
        Validate OpenRouter API connectivity with lightweight test.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Lightweight test with smaller model
            payload = {
                "model": "meta-llama/llama-3.1-8b-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": "Test response - say 'API working' if you receive this"
                    }
                ],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.info("OpenRouter API key validated successfully.")
                self.api_validated = True
                return True
            else:
                logger.error(f"OpenRouter API key invalid: {response.status_code}")
                self.api_validated = False
                return False
                
        except Exception as e:
            logger.error(f"OpenRouter API validation failed: {e}")
            self.api_validated = False
            return False
    
    def _call_model(self, model: str, messages: list, max_tokens: int = 500, timeout: int = 30) -> Optional[str]:
        """
        Call a specific model with fallback handling.
        """
        if not self.api_available or not self.api_validated:
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.2
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                return content if content else None
            else:
                logger.warning(f"Model {model} failed with status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.warning(f"Model {model} request timed out")
            return None
        except Exception as e:
            logger.warning(f"Model {model} request failed: {e}")
            return None
    
    def _assess_risk_level(self, analysis_text: str) -> RiskLevel:
        """
        Assess risk level from analysis text.
        """
        text_lower = analysis_text.lower()
        
        high_risk_keywords = ['illegal', 'unconstitutional', 'void', 'invalid', 'prohibited', 'breach', 'violation']
        medium_risk_keywords = ['risk', 'potential', 'may', 'could', 'subject to', 'conditional']
        low_risk_keywords = ['standard', 'compliant', 'legal', 'valid', 'proper', 'acceptable']
        
        if any(keyword in text_lower for keyword in high_risk_keywords):
            return RiskLevel.HIGH
        elif any(keyword in text_lower for keyword in medium_risk_keywords):
            return RiskLevel.MEDIUM
        elif any(keyword in text_lower for keyword in low_risk_keywords):
            return RiskLevel.LOW
        else:
            return RiskLevel.UNKNOWN
    
    def generate_full_clause_analysis(self, 
                                    clause_text: str, 
                                    constitution: str, 
                                    clause_type: str, 
                                    matched_article: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate comprehensive clause analysis with multiple perspectives.
        """
        
        # Check cache first
        cached_response = self.performance_optimizer.get_cached_api_response(
            clause_text, constitution, clause_type
        )
        
        if cached_response:
            logger.info("Using cached comprehensive analysis")
            return cached_response
        
        # Build constitution context
        constitution_context = f"Constitution: {constitution}"
        
        if matched_article:
            constitution_context += f"\nRelevant Article: {matched_article.get('article_number', 'N/A')}"
            constitution_context += f"\nArticle Title: {matched_article.get('title', 'N/A')}"
            constitution_context += f"\nSimilarity: {matched_article.get('similarity_score', 0):.3f}"
        
        # Create comprehensive analysis prompt
        analysis_prompt = f"""As an expert constitutional lawyer, provide a comprehensive analysis of this legal clause.

{constitution_context}

Clause Type: {clause_type}

Clause Text:
{clause_text}

Provide analysis in these four sections:

1. EXPLANATION: Plain English explanation of what this clause means and its legal implications.

2. OFFENSIVE ANALYSIS: How could someone use this clause to their advantage? What strategic benefits does it provide?

3. DEFENSIVE ANALYSIS: How could someone challenge or defend against this clause? What are the potential vulnerabilities?

4. RISK ASSESSMENT: What is the overall risk level (HIGH/MEDIUM/LOW) and why?"""
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert constitutional lawyer providing comprehensive legal analysis. Be thorough, strategic, and practical."
            },
            {
                "role": "user",
                "content": analysis_prompt
            }
        ]
        
        # Try primary model first
        logger.info(f"Requesting comprehensive analysis from {self.primary_model}")
        analysis = self._call_model(self.primary_model, messages, max_tokens=800, timeout=45)
        
        # Fallback to secondary model if primary fails
        if not analysis:
            logger.info(f"Primary model failed, trying fallback {self.fallback_model}")
            analysis = self._call_model(self.fallback_model, messages, max_tokens=800, timeout=45)
        
        # Parse analysis into structured components
        structured_analysis = self._parse_analysis(analysis, matched_article)
        
        # Cache the result
        self.performance_optimizer.cache_api_response(
            clause_text, constitution, clause_type, structured_analysis
        )
        
        return structured_analysis
    
    def _parse_analysis(self, analysis: Optional[str], matched_article: Optional[Dict]) -> Dict[str, Any]:
        """
        Parse analysis text into structured components.
        """
        if not analysis:
            return {
                "explanation": "Generative AI unavailable. Semantic analysis only.",
                "offensive_analysis": "Unavailable",
                "defensive_analysis": "Unavailable",
                "constitution_reference": matched_article.get('text', '')[:200] + '...' if matched_article else '',
                "risk_level": RiskLevel.UNKNOWN.value
            }
        
        # Parse sections
        sections = {
            "explanation": "",
            "offensive_analysis": "", 
            "defensive_analysis": "",
            "risk_assessment": ""
        }
        
        current_section = None
        lines = analysis.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if any(keyword in line.upper() for keyword in ['EXPLANATION:', '1. EXPLANATION']):
                current_section = 'explanation'
                continue
            elif any(keyword in line.upper() for keyword in ['OFFENSIVE:', '2. OFFENSIVE']):
                current_section = 'offensive_analysis'
                continue
            elif any(keyword in line.upper() for keyword in ['DEFENSIVE:', '3. DEFENSIVE']):
                current_section = 'defensive_analysis'
                continue
            elif any(keyword in line.upper() for keyword in ['RISK:', '4. RISK']):
                current_section = 'risk_assessment'
                continue
            
            # Add content to current section
            if current_section and current_section in sections:
                sections[current_section] += line + ' '
        
        # Clean up sections
        for key in sections:
            sections[key] = sections[key].strip()
        
        # Assess risk level
        risk_level = self._assess_risk_level(sections.get('risk_assessment', ''))
        
        # Build constitution reference
        constitution_ref = ""
        if matched_article:
            constitution_ref = f"Article {matched_article.get('article_number', 'N/A')}: {matched_article.get('title', 'N/A')}"
        
        return {
            "explanation": sections.get('explanation', 'No explanation provided.'),
            "offensive_analysis": sections.get('offensive_analysis', 'No offensive analysis provided.'),
            "defensive_analysis": sections.get('defensive_analysis', 'No defensive analysis provided.'),
            "constitution_reference": constitution_ref,
            "risk_level": risk_level.value
        }
    
    def generate_clause_explanation(self, clause_text: str, constitution: str, clause_type: str) -> str:
        """
        Legacy method for backward compatibility.
        """
        analysis = self.generate_full_clause_analysis(clause_text, constitution, clause_type)
        return analysis.get('explanation', 'AI explanation unavailable.')

# Global service instance
generative_service = GenerativeService()

def generate_clause_explanation(clause_text: str, constitution: str, clause_type: str) -> str:
    """
    Generate explanation for a clause using global generative service.
    """
    return generative_service.generate_clause_explanation(clause_text, constitution, clause_type)

def generate_full_clause_analysis(clause_text: str, 
                                constitution: str, 
                                clause_type: str, 
                                matched_article: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Generate comprehensive clause analysis using global generative service.
    """
    return generative_service.generate_full_clause_analysis(clause_text, constitution, clause_type, matched_article)
