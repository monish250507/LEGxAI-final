import re
import json
import logging
from typing import List, Dict, Any

# Try to import AI pipeline, but provide fallback
try:
    from services.ai_pipeline import _call_chat
    AI_PIPELINE_AVAILABLE = True
except ImportError:
    AI_PIPELINE_AVAILABLE = False
    def _call_chat(*args, **kwargs):
        return "AI services not available - using pattern-based extraction only"
    logging.warning("AI pipeline not available - using pattern-based extraction only")

# Configure logging
logger = logging.getLogger(__name__)

def extract_clauses(document_text: str) -> List[Dict[str, str]]:
    """
    Extract clauses from legal document text using pattern-based detection.
    
    Args:
        document_text (str): The legal document text to analyze
        
    Returns:
        List[Dict[str, str]]: List of clauses with clause_id and text
    """
    if not document_text or not document_text.strip():
        return []
    
    # Clean the text first
    cleaned_text = _clean_document_text(document_text)
    
    # Split into potential clauses using multiple strategies
    clauses = _extract_clauses_by_patterns(cleaned_text)
    
    # Filter and validate clauses
    valid_clauses = _filter_valid_clauses(clauses)
    
    # Generate clause IDs
    for i, clause in enumerate(valid_clauses, 1):
        clause['clause_id'] = f"clause_{i:03d}"
    
    logger.info(f"Extracted {len(valid_clauses)} clauses from document")
    return valid_clauses

def _clean_document_text(text: str) -> str:
    """
    Clean document text for better clause extraction.
    
    Args:
        text (str): Raw document text
        
    Returns:
        str: Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Preserve paragraph breaks
    text = re.sub(r'\s*\n\s*', '\n', text)
    
    # Remove page numbers and headers
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*Page\s+\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Clean up extra spaces
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()

def _extract_clauses_by_patterns(text: str) -> List[Dict[str, str]]:
    """
    Extract clauses using various patterns and strategies.
    
    Args:
        text (str): Cleaned document text
        
    Returns:
        List[Dict[str, str]]: List of raw clauses
    """
    clauses = []
    
    # Strategy 1: Numbered clauses (1., 2., 3., etc.)
    numbered_clauses = _extract_numbered_clauses(text)
    clauses.extend(numbered_clauses)
    
    # Strategy 2: Lettered clauses (a., b., c., etc.)
    lettered_clauses = _extract_lettered_clauses(text)
    clauses.extend(lettered_clauses)
    
    # Strategy 3: Paragraph-based clauses
    if not clauses or len(clauses) < 3:
        paragraph_clauses = _extract_paragraph_clauses(text)
        clauses.extend(paragraph_clauses)
    
    # Strategy 4: Legal section patterns
    section_clauses = _extract_section_clauses(text)
    clauses.extend(section_clauses)
    
    # Remove duplicates while preserving order
    seen_texts = set()
    unique_clauses = []
    for clause in clauses:
        if clause['text'] not in seen_texts:
            seen_texts.add(clause['text'])
            unique_clauses.append(clause)
    
    return unique_clauses

def _extract_numbered_clauses(text: str) -> List[Dict[str, str]]:
    """
    Extract numbered clauses using regex patterns.
    
    Args:
        text (str): Document text
        
    Returns:
        List[Dict[str, str]]: List of numbered clauses
    """
    clauses = []
    
    # Pattern for numbered clauses: 1., 2., 3., etc.
    pattern = r'(?m)^(?:\s*(\d+)\.\s+)(.+?)(?=\s*\d+\.\s+|$)'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    for match in matches:
        clause_text = match.group(2).strip()
        if len(clause_text) > 20:  # Filter very short matches
            clauses.append({
                'text': clause_text,
                'type': 'numbered',
                'number': int(match.group(1))
            })
    
    # Pattern for numbered clauses with parentheses: (1), (2), (3), etc.
    pattern_paren = r'(?m)^(?:\s*\((\d+)\)\s+)(.+?)(?=\s*\(\d+\)\s+|$)'
    matches_paren = re.finditer(pattern_paren, text, re.DOTALL)
    
    for match in matches_paren:
        clause_text = match.group(2).strip()
        if len(clause_text) > 20:
            clauses.append({
                'text': clause_text,
                'type': 'numbered_paren',
                'number': int(match.group(1))
            })
    
    return clauses

def _extract_lettered_clauses(text: str) -> List[Dict[str, str]]:
    """
    Extract lettered clauses using regex patterns.
    
    Args:
        text (str): Document text
        
    Returns:
        List[Dict[str, str]]: List of lettered clauses
    """
    clauses = []
    
    # Pattern for lettered clauses: a., b., c., etc.
    pattern = r'(?m)^(?:\s*([a-zA-Z])\.\s+)(.+?)(?=\s*[a-zA-Z]\.\s+|$)'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    for match in matches:
        clause_text = match.group(2).strip()
        if len(clause_text) > 15:  # Filter very short matches
            clauses.append({
                'text': clause_text,
                'type': 'lettered',
                'letter': match.group(1)
            })
    
    return clauses

def _extract_paragraph_clauses(text: str) -> List[Dict[str, str]]:
    """
    Extract clauses based on paragraph breaks.
    
    Args:
        text (str): Document text
        
    Returns:
        List[Dict[str, str]]: List of paragraph-based clauses
    """
    clauses = []
    
    # Split by double newlines (paragraph breaks)
    paragraphs = re.split(r'\n\s*\n', text)
    
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        
        # Filter paragraphs that are likely clauses
        if len(paragraph) > 30 and _is_likely_clause(paragraph):
            clauses.append({
                'text': paragraph,
                'type': 'paragraph',
                'paragraph_number': i + 1
            })
    
    return clauses

def _extract_section_clauses(text: str) -> List[Dict[str, str]]:
    """
    Extract clauses based on legal section patterns.
    
    Args:
        text (str): Document text
        
    Returns:
        List[Dict[str, str]]: List of section-based clauses
    """
    clauses = []
    
    # Pattern for sections: Section 1, Article 2, etc.
    section_patterns = [
        r'(?m)^(?:\s*(?:Section|Article|Clause)\s+(\d+(?:\.\d+)*)\.?\s*:?\s*)(.+?)(?=\s*(?:Section|Article|Clause)\s+\d+|$)',
        r'(?m)^(?:\s*(\d+(?:\.\d+)*)\.\s*)(.+?)(?=\s*\d+(?:\.\d+)*\.\s+|$)'
    ]
    
    for pattern in section_patterns:
        matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            clause_text = match.group(2).strip()
            if len(clause_text) > 20:
                clauses.append({
                    'text': clause_text,
                    'type': 'section',
                    'section': match.group(1)
                })
    
    return clauses

def _is_likely_clause(text: str) -> bool:
    """
    Determine if a text segment is likely a legal clause.
    
    Args:
        text (str): Text segment to evaluate
        
    Returns:
        bool: True if likely a clause
    """
    # Keywords that indicate legal clauses
    legal_keywords = [
        'shall', 'must', 'will', 'agree', 'obligation', 'liable', 'responsible',
        'prohibited', 'forbidden', 'restricted', 'required', 'mandatory',
        'entitled', 'right', 'permission', 'authorized', 'permitted',
        'terminate', 'expiration', 'duration', 'period', 'term',
        'party', 'parties', 'agreement', 'contract', 'legal', 'law'
    ]
    
    text_lower = text.lower()
    
    # Check for legal keywords
    keyword_count = sum(1 for keyword in legal_keywords if keyword in text_lower)
    
    # Check for sentence structure indicators
    has_subject_verb = bool(re.search(r'\b\w+\s+\w+(?:s|ed|ing)\b', text_lower))
    
    # Minimum length and keyword requirements
    is_long_enough = len(text) > 30
    has_keywords = keyword_count >= 1
    
    return is_long_enough and (has_keywords or has_subject_verb)

def _filter_valid_clauses(clauses: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Filter and validate extracted clauses.
    
    Args:
        clauses (List[Dict[str, str]]): Raw clauses
        
    Returns:
        List[Dict[str, str]]: Filtered valid clauses
    """
    valid_clauses = []
    
    for clause in clauses:
        text = clause['text'].strip()
        
        # Basic validation
        if len(text) < 10:
            continue
            
        if len(text) > 2000:  # Very long clauses might be multiple clauses
            # Try to split long clauses
            sub_clauses = _split_long_clause(text)
            for sub_clause in sub_clauses:
                if _is_likely_clause(sub_clause):
                    valid_clauses.append({'text': sub_clause, 'type': 'split'})
        elif _is_likely_clause(text):
            valid_clauses.append({'text': text, 'type': clause.get('type', 'unknown')})
    
    return valid_clauses

def _split_long_clause(text: str) -> List[str]:
    """
    Split very long clauses into smaller, more manageable chunks.
    
    Args:
        text (str): Long clause text
        
    Returns:
        List[str]: Split clause parts
    """
    # Split by sentence boundaries
    sentences = re.split(r'[.!?]+\s+', text)
    
    # Group sentences into reasonable chunks
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        if len(current_chunk + sentence) < 500:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def extract_clauses_with_ai(document_text: str) -> Dict[str, Any]:
    """
    Extract clauses using AI for enhanced accuracy.
    
    This function uses the original AI-based extraction for comparison
    or when pattern-based extraction is insufficient.
    
    Args:
        document_text (str): The legal document text to analyze
        
    Returns:
        Dict[str, Any]: AI-extracted clauses categorized by type
    """
    prompt = (
        "Extract key clauses from the legal text. Return a JSON object with fields: obligations, rights, prohibitions, dates, parties. "
        "Each field should be a list of objects with 'text' and optional 'section' if available.\n\n"
        f"Text:\n{document_text}"
    )
    
    out = _call_chat(prompt, max_tokens=700, temperature=0.1)
    
    # Try to parse JSON if LLM returned JSON
    try:
        parsed = json.loads(out)
        return parsed
    except Exception:
        # fallback: return raw text
        return {"extraction": out}
