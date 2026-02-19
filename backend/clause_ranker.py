import json
import logging
from typing import List, Dict, Any, Union

# Try to import optional dependencies
try:
    from services.ai_pipeline import _call_chat
    AI_PIPELINE_AVAILABLE = True
except ImportError:
    AI_PIPELINE_AVAILABLE = False
    def _call_chat(*args, **kwargs):
        return "AI services not available"
    logging.warning("AI pipeline not available - using fallback behavior")

try:
    from services.embeddings import encode_texts
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    def encode_texts(texts):
        import numpy as np
        return np.random.rand(len(texts), 384)
    logging.warning("Embeddings not available - using random vectors")

try:
    import numpy as np
except ImportError:
    np = None
    logging.error("NumPy not available - ranking will be limited")
    raise ImportError("NumPy is required for clause ranking")

# Configure logging
logger = logging.getLogger(__name__)

# Define clause type priority scores
CLAUSE_PRIORITY_SCORES = {
    'termination': 0.9,
    'liability': 0.85,
    'indemnity': 0.8,
    'jurisdiction': 0.75,
    'payment': 0.6,
    'general': 0.3
}

# Define color coding based on priority scores
def get_priority_color(priority_score: float) -> str:
    """
    Get color based on priority score.
    
    Args:
        priority_score (float): Priority score (0-1)
        
    Returns:
        str: Color name ('red', 'yellow', 'green')
    """
    if priority_score > 0.75:
        return 'red'
    elif priority_score > 0.45:
        return 'yellow'
    else:
        return 'green'

def rank_clauses_by_importance(clauses: List[Dict[str, Any]], query: str = "") -> List[Dict[str, Any]]:
    """
    Rank clauses by importance based on type priority and optional query relevance.
    
    Args:
        clauses (List[Dict[str, Any]]): List of clause dictionaries with 'type' field
        query (str): Optional query to rank by relevance
        
    Returns:
        List[Dict[str, Any]]: Ranked clauses with priority_score and color
    """
    if not clauses:
        return []
    
    # Extract texts for encoding
    texts = []
    for clause in clauses:
        if isinstance(clause, dict):
            texts.append(clause.get('text', ''))
        else:
            texts.append(str(clause))
    
    # Get embeddings for semantic similarity
    try:
        embeddings = encode_texts(texts)
    except Exception as e:
        logger.warning(f"Failed to encode texts: {e}")
        embeddings = np.random.rand(len(texts), 384)  # Fallback random embeddings
    
    # If query provided, calculate relevance scores
    if query:
        try:
            query_embedding = encode_texts([query])[0]
            relevance_scores = np.dot(embeddings, query_embedding)
        except Exception as e:
            logger.warning(f"Failed to encode query: {e}")
            relevance_scores = np.ones(len(texts))
    else:
        relevance_scores = np.ones(len(texts))
    
    # Rank clauses
    ranked_clauses = []
    
    for i, clause in enumerate(clauses):
        # Get clause type and priority score
        clause_type = 'general'  # default
        if isinstance(clause, dict):
            clause_type = clause.get('type', 'general')
        
        priority_score = CLAUSE_PRIORITY_SCORES.get(clause_type, 0.3)
        
        # Calculate relevance score (normalized)
        relevance_score = float(relevance_scores[i])
        max_relevance = np.max(relevance_scores) if np.max(relevance_scores) > 0 else 1
        normalized_relevance = relevance_score / max_relevance if max_relevance > 0 else 0
        
        # Calculate combined score (70% priority, 30% relevance)
        combined_score = (priority_score * 0.7) + (normalized_relevance * 0.3)
        
        # Get color based on priority score
        color = get_priority_color(priority_score)
        
        # Create ranked clause object
        ranked_clause = clause.copy() if isinstance(clause, dict) else {'text': str(clause)}
        
        ranked_clause.update({
            'priority_score': round(priority_score, 3),
            'relevance_score': round(normalized_relevance, 3),
            'combined_score': round(combined_score, 3),
            'color': color,
            'rank': 0  # Will be set after sorting
        })
        
        ranked_clauses.append(ranked_clause)
    
    # Sort by combined score (descending)
    ranked_clauses.sort(key=lambda x: x['combined_score'], reverse=True)
    
    # Assign ranks
    for i, clause in enumerate(ranked_clauses):
        clause['rank'] = i + 1
    
    logger.info(f"Ranked {len(ranked_clauses)} clauses by importance")
    return ranked_clauses

def get_top_clauses(clauses: List[Dict[str, Any]], top_n: int = 5, query: str = "") -> List[Dict[str, Any]]:
    """
    Get the top N most important clauses.
    
    Args:
        clauses (List[Dict[str, Any]]): List of clauses to rank
        top_n (int): Number of top clauses to return
        query (str): Optional query for relevance ranking
        
    Returns:
        List[Dict[str, Any]]: Top N ranked clauses
    """
    ranked = rank_clauses_by_importance(clauses, query)
    return ranked[:top_n]

def get_clause_priority_statistics(clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get statistics about clause priority distribution.
    
    Args:
        clauses (List[Dict[str, Any]]): List of ranked clauses
        
    Returns:
        Dict[str, Any]: Statistics about clause priorities
    """
    if not clauses:
        return {'total_clauses': 0, 'priority_distribution': {}}
    
    # Count clauses by priority level
    priority_counts = {'red': 0, 'yellow': 0, 'green': 0}
    type_counts = {}
    
    for clause in clauses:
        color = clause.get('color', 'green')
        clause_type = clause.get('type', 'general')
        
        priority_counts[color] = priority_counts.get(color, 0) + 1
        type_counts[clause_type] = type_counts.get(clause_type, 0) + 1
    
    # Calculate percentages
    total = len(clauses)
    priority_percentages = {
        color: round((count / total) * 100, 1) 
        for color, count in priority_counts.items()
    }
    
    return {
        'total_clauses': total,
        'priority_distribution': {
            'counts': priority_counts,
            'percentages': priority_percentages
        },
        'type_distribution': type_counts,
        'highest_priority': max(priority_counts, key=priority_counts.get) if priority_counts else 'green'
    }

def rank_clauses_by_type_priority(clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Simple ranking based only on clause type priority (no query relevance).
    
    Args:
        clauses (List[Dict[str, Any]]): List of clauses with 'type' field
        
    Returns:
        List[Dict[str, Any]]: Clauses ranked by type priority
    """
    ranked_clauses = []
    
    for clause in clauses:
        clause_type = clause.get('type', 'general')
        priority_score = CLAUSE_PRIORITY_SCORES.get(clause_type, 0.3)
        color = get_priority_color(priority_score)
        
        ranked_clause = clause.copy()
        ranked_clause.update({
            'priority_score': round(priority_score, 3),
            'color': color,
            'rank': 0  # Will be set after sorting
        })
        
        ranked_clauses.append(ranked_clause)
    
    # Sort by priority score (descending)
    ranked_clauses.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # Assign ranks
    for i, clause in enumerate(ranked_clauses):
        clause['rank'] = i + 1
    
    return ranked_clauses

def rank_clauses_with_ai(clauses: List[Dict[str, Any]], query: str = "") -> List[Dict[str, Any]]:
    """
    Rank clauses using AI for enhanced importance assessment.
    
    This function uses AI-based ranking as an alternative to priority-based ranking.
    
    Args:
        clauses (List[Dict[str, Any]]): List of clauses to rank
        query (str): Optional query for relevance ranking
        
    Returns:
        List[Dict[str, Any]]: AI-ranked clauses
    """
    texts = []
    for clause in clauses:
        if isinstance(clause, dict):
            texts.append(clause.get('text', ''))
        else:
            texts.append(str(clause))
    
    prompt = f"""
    Analyze the following legal clauses and rank them by importance (1-10, where 10 is most important).
    Consider factors like:
    - Financial obligations and payment terms
    - Legal compliance requirements
    - Critical deadlines and termination clauses
    - Risk exposure and liability
    - Core business terms and conditions
    
    Return a JSON array with objects containing 'index' and 'importance_score' fields.
    
    Clauses:
    {json.dumps([{'index': i, 'text': text} for i, text in enumerate(texts)], indent=2)}
    """
    
    out = _call_chat(prompt, max_tokens=1000, temperature=0.1)
    
    try:
        ai_scores = json.loads(out)
        # Create importance score mapping
        importance_map = {item['index']: item.get('importance_score', 5) for item in ai_scores}
    except Exception:
        # Fallback: use priority scores
        importance_map = {}
        for i, clause in enumerate(clauses):
            clause_type = clause.get('type', 'general')
            importance_map[i] = CLAUSE_PRIORITY_SCORES.get(clause_type, 0.3) * 10
    
    # Apply AI scores to clauses
    ranked_clauses = []
    for i, clause in enumerate(clauses):
        importance = importance_map.get(i, 5)
        priority_score = importance / 10.0  # Normalize to 0-1
        color = get_priority_color(priority_score)
        
        ranked_clause = clause.copy()
        ranked_clause.update({
            'priority_score': round(priority_score, 3),
            'importance_score': importance,
            'color': color,
            'rank': 0,
            'ranking_method': 'ai_enhanced'
        })
        
        ranked_clauses.append(ranked_clause)
    
    # Sort by importance score (descending)
    ranked_clauses.sort(key=lambda x: x['importance_score'], reverse=True)
    
    # Assign ranks
    for i, clause in enumerate(ranked_clauses):
        clause['rank'] = i + 1
    
    return ranked_clauses
