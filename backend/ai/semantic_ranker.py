"""
Semantic Ranker - Assigns priority scores and ranks clauses based on semantic classification.
"""

import logging
from typing import List, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

class SemanticRanker:
    """
    Ranker that assigns priority scores and colors based on semantic clause types.
    """
    
    def __init__(self):
        # Priority score mapping for clause types
        self.priority_scores = {
            'termination': 0.9,
            'liability': 0.85,
            'indemnity': 0.85,
            'jurisdiction': 0.7,
            'confidentiality': 0.75,
            'payment': 0.6,
            'general': 0.3
        }
        
        # Color mapping based on priority
        self.color_mapping = {
            'high': 'red',      # 0.8 - 1.0
            'medium': 'yellow', # 0.5 - 0.8
            'low': 'green'      # 0.0 - 0.5
        }
    
    def _get_color_from_priority(self, priority_score: float) -> str:
        """
        Get color based on priority score.
        
        Args:
            priority_score: Priority score between 0 and 1
            
        Returns:
            str: Color ('red', 'yellow', or 'green')
        """
        if priority_score >= 0.8:
            return self.color_mapping['high']
        elif priority_score >= 0.5:
            return self.color_mapping['medium']
        else:
            return self.color_mapping['low']
    
    def rank_clauses(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank clauses based on their semantic classification.
        
        Args:
            clauses: List of clause dictionaries with 'type' field
            
        Returns:
            List[Dict[str, Any]]: Ranked clauses with priority_score, color, and rank
        """
        try:
            logger.info(f"Ranking {len(clauses)} clauses semantically")
            
            ranked_clauses = []
            
            for clause in clauses:
                clause_type = clause.get('type', 'general')
                confidence = clause.get('confidence', 0.0)
                
                # Get priority score for clause type
                base_priority = self.priority_scores.get(clause_type, 0.3)
                
                # Adjust priority based on confidence
                # Higher confidence boosts priority slightly
                adjusted_priority = base_priority * (0.7 + 0.3 * confidence)
                
                # Ensure priority stays within bounds
                adjusted_priority = max(0.0, min(1.0, adjusted_priority))
                
                # Get color based on priority
                color = self._get_color_from_priority(adjusted_priority)
                
                # Update clause with ranking information
                ranked_clause = clause.copy()
                ranked_clause['priority_score'] = float(adjusted_priority)
                ranked_clause['color'] = color
                
                ranked_clauses.append(ranked_clause)
                
                logger.debug(f"Clause {clause.get('clause_id', 'unknown')}: {clause_type} -> priority {adjusted_priority:.3f} ({color})")
            
            # Sort clauses by priority score (descending)
            ranked_clauses.sort(key=lambda x: x['priority_score'], reverse=True)
            
            # Assign ranks
            for rank, clause in enumerate(ranked_clauses, 1):
                clause['rank'] = rank
            
            logger.info(f"Successfully ranked {len(ranked_clauses)} clauses")
            return ranked_clauses
            
        except Exception as e:
            logger.error(f"Failed to rank clauses: {e}")
            # Return original clauses with default ranking
            for i, clause in enumerate(clauses):
                clause['priority_score'] = 0.3
                clause['color'] = 'green'
                clause['rank'] = i + 1
            return clauses
    
    def get_priority_mapping(self) -> Dict[str, float]:
        """
        Get the priority score mapping for all clause types.
        
        Returns:
            Dict[str, float]: Mapping of clause types to priority scores
        """
        return self.priority_scores.copy()
    
    def get_color_mapping(self) -> Dict[str, str]:
        """
        Get the color mapping for priority levels.
        
        Returns:
            Dict[str, str]: Mapping of priority levels to colors
        """
        return self.color_mapping.copy()

# Global service instance
semantic_ranker = SemanticRanker()

def rank_clauses(clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rank clauses using global semantic ranker."""
    return semantic_ranker.rank_clauses(clauses)
