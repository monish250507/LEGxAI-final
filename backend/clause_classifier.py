import re
import logging
from typing import List, Dict, Any, Union

# Try to import AI pipeline, but provide fallback
try:
    from services.ai_pipeline import _call_chat
    AI_PIPELINE_AVAILABLE = True
except ImportError:
    AI_PIPELINE_AVAILABLE = False
    def _call_chat(*args, **kwargs):
        return "AI services not available"
    logging.warning("AI pipeline not available - using keyword-only classification")

# Configure logging
logger = logging.getLogger(__name__)

# Define clause type keywords and patterns
CLAUSE_TYPES = {
    'termination': {
        'keywords': [
            'terminate', 'termination', 'end', 'expire', 'expiration', 'cancel', 'cancellation',
            'dissolve', 'dissolution', 'conclude', 'conclusion', 'finish', 'completion',
            'notice period', 'notice', 'effective date', 'term', 'duration'
        ],
        'patterns': [
            r'\bterminate\b',
            r'\btermination\b',
            r'\bexpire\b',
            r'\bcancel\b',
            r'\bnotice\s+period\b',
            r'\bterm\s+of\s+this\s+agreement\b'
        ],
        'weight': 3.0
    },
    'liability': {
        'keywords': [
            'liable', 'liability', 'responsible', 'responsibility', 'accountable',
            'breach', 'violation', 'negligence', 'fault', 'damage', 'loss',
            'compensation', 'reimbursement', 'indemnif', 'hold harmless'
        ],
        'patterns': [
            r'\bliabl\w*\b',
            r'\bresponsib\w*\b',
            r'\bbreach\b',
            r'\bnegligence\b',
            r'\bdamage\b',
            r'\bloss\b'
        ],
        'weight': 2.5
    },
    'payment': {
        'keywords': [
            'pay', 'payment', 'fee', 'cost', 'price', 'invoice', 'billing',
            'compensation', 'remuneration', 'salary', 'wage', 'charge',
            'due', 'overdue', 'late', 'penalty', 'interest', 'currency'
        ],
        'patterns': [
            r'\bpay\w*\b',
            r'\bpayment\b',
            r'\bfee\b',
            r'\bcost\b',
            r'\binvoice\b',
            r'\bdue\s+date\b',
            r'\blate\s+payment\b'
        ],
        'weight': 2.8
    },
    'jurisdiction': {
        'keywords': [
            'jurisdiction', 'govern', 'law', 'legal', 'court', 'arbitration',
            'dispute', 'litigation', 'forum', 'venue', 'state', 'federal',
            'applicable law', 'governing law', 'choice of law'
        ],
        'patterns': [
            r'\bjurisdiction\b',
            r'\bgovern\w*\s+by\b',
            r'\bgoverning\s+law\b',
            r'\bapplicable\s+law\b',
            r'\bcourt\b',
            r'\barbitration\b',
            r'\bdispute\s+resolution\b'
        ],
        'weight': 3.2
    },
    'confidentiality': {
        'keywords': [
            'confidential', 'confidentiality', 'secret', 'proprietary', 'trade secret',
            'non-disclosure', 'disclose', 'reveal', 'share', 'protect',
            'information', 'data', 'sensitive', 'private'
        ],
        'patterns': [
            r'\bconfidential\w*\b',
            r'\bproprietary\b',
            r'\btrade\s+secret\b',
            r'\bnon-disclosure\b',
            r'\bdisclos\w*\b',
            r'\bsensitive\s+information\b'
        ],
        'weight': 3.5
    },
    'indemnity': {
        'keywords': [
            'indemnif', 'indemnity', 'hold harmless', 'defend', 'protect',
            'reimburse', 'compensate', 'cover', 'bear', 'costs', 'expenses',
            'damages', 'claims', 'lawsuits', 'legal action'
        ],
        'patterns': [
            r'\bindemnif\w*\b',
            r'\bhold\s+harmless\b',
            r'\bdefend\s+and\s+indemnif\w*\b',
            r'\breimburse\b',
            r'\bcompensate\b',
            r'\bbear\s+the\s+cost\b'
        ],
        'weight': 3.8
    },
    'general': {
        'keywords': [
            'agree', 'agreement', 'contract', 'understand', 'acknowledge',
            'accept', 'acceptance', 'confirm', 'certify', 'warrant',
            'guarantee', 'promise', 'undertake', 'commit'
        ],
        'patterns': [
            r'\bagree\w*\b',
            r'\bagreement\b',
            r'\bcontract\b',
            r'\bunderstan\w*\b',
            r'\bachnowledg\w*\b',
            r'\bwarrant\w*\b'
        ],
        'weight': 1.0
    }
}

def classify_clause_type(clause_text: str) -> Dict[str, Any]:
    """
    Classify a legal clause using keyword-based detection.
    
    Args:
        clause_text (str): The clause text to classify
        
    Returns:
        dict: Classification result with type and confidence
    """
    if not clause_text or not clause_text.strip():
        return {"type": "general", "confidence": 0.0, "method": "empty"}
    
    # Normalize text for analysis
    text_lower = clause_text.lower()
    
    # Calculate scores for each clause type
    scores = {}
    
    for clause_type, config in CLAUSE_TYPES.items():
        score = 0
        
        # Keyword matching
        keyword_score = 0
        for keyword in config['keywords']:
            # Count occurrences of the keyword
            occurrences = len(re.findall(rf'\b{re.escape(keyword)}\b', text_lower))
            keyword_score += occurrences * config['weight']
        
        # Pattern matching (higher weight)
        pattern_score = 0
        for pattern in config['patterns']:
            matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
            pattern_score += matches * (config['weight'] * 1.5)
        
        # Combined score
        total_score = keyword_score + pattern_score
        scores[clause_type] = total_score
    
    # Find the best match
    if not scores or max(scores.values()) == 0:
        return {"type": "general", "confidence": 0.1, "method": "no_match"}
    
    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]
    
    # Calculate confidence (normalized to 0-1)
    max_possible_score = sum(config['weight'] for config in CLAUSE_TYPES.values()) * 2
    confidence = min(best_score / max_possible_score, 1.0)
    
    # Apply minimum confidence thresholds
    if confidence < 0.1:
        best_type = "general"
        confidence = 0.1
    
    return {
        "type": best_type,
        "confidence": round(confidence, 3),
        "method": "keyword_based",
        "scores": scores
    }

def classify_multiple_clauses(clauses: List[Union[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Classify multiple clauses at once.
    
    Args:
        clauses (List[Union[str, Dict[str, Any]]]): List of clause texts or clause objects
        
    Returns:
        List[Dict[str, Any]]: List of classification results with type field added
    """
    results = []
    
    for clause in clauses:
        if isinstance(clause, dict):
            # Handle clause objects with text field
            clause_text = clause.get('text', '')
            clause_id = clause.get('clause_id', '')
            
            classification = classify_clause_type(clause_text)
            
            # Create result with all original fields plus classification
            result = clause.copy()
            result['type'] = classification['type']
            result['confidence'] = classification['confidence']
            result['classification_method'] = classification['method']
            
            results.append(result)
            
        else:
            # Handle plain text clauses
            clause_text = str(clause)
            classification = classify_clause_type(clause_text)
            
            result = {
                'text': clause_text,
                'type': classification['type'],
                'confidence': classification['confidence'],
                'classification_method': classification['method']
            }
            
            results.append(result)
    
    logger.info(f"Classified {len(results)} clauses")
    return results

def get_clause_type_statistics(clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get statistics about clause type distribution.
    
    Args:
        clauses (List[Dict[str, Any]]): List of classified clauses
        
    Returns:
        Dict[str, Any]: Statistics about clause types
    """
    type_counts = {}
    confidence_sum = {}
    
    for clause in clauses:
        clause_type = clause.get('type', 'general')
        confidence = clause.get('confidence', 0.0)
        
        type_counts[clause_type] = type_counts.get(clause_type, 0) + 1
        confidence_sum[clause_type] = confidence_sum.get(clause_type, 0.0) + confidence
    
    # Calculate averages
    type_stats = {}
    for clause_type in type_counts:
        count = type_counts[clause_type]
        avg_confidence = confidence_sum[clause_type] / count
        
        type_stats[clause_type] = {
            'count': count,
            'percentage': round((count / len(clauses)) * 100, 1),
            'average_confidence': round(avg_confidence, 3)
        }
    
    return {
        'total_clauses': len(clauses),
        'type_distribution': type_stats,
        'most_common': max(type_counts, key=type_counts.get) if type_counts else 'general'
    }

def classify_clause_with_ai(clause_text: str) -> Dict[str, Any]:
    """
    Classify clause using AI for enhanced accuracy.
    
    This function uses AI-based classification as a fallback or for comparison.
    
    Args:
        clause_text (str): The clause text to classify
        
    Returns:
        Dict[str, Any]: AI classification result
    """
    prompt = f"""
    Classify the following legal clause into one of these categories:
    - termination (ending or canceling agreements)
    - liability (legal responsibility or fault)
    - payment (financial obligations or fees)
    - jurisdiction (governing law or legal authority)
    - confidentiality (information protection)
    - indemnity (holding harmless from losses)
    - general (miscellaneous or general terms)
    
    Return a JSON object with 'type' and 'confidence' (0-1) fields.
    
    Clause: {clause_text}
    """
    
    out = _call_chat(prompt, max_tokens=200, temperature=0.1)
    
    try:
        parsed = json.loads(out)
        return parsed
    except Exception:
        # fallback to keyword-based classification
        return classify_clause_type(clause_text)
