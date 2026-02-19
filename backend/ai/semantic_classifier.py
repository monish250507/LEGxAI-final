"""
Semantic Classifier - Uses embeddings to classify clauses based on semantic similarity.
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.metrics.pairwise import cosine_similarity
from ai.embedding_service import load_model, generate_embeddings

# Configure logging
logger = logging.getLogger(__name__)

class SemanticClassifier:
    """
    Classifier that uses semantic similarity to assign clause types.
    """
    
    def __init__(self):
        self.prototype_vectors = {}
        self._prototypes_loaded = False
    
    def _create_prototype_texts(self) -> Dict[str, str]:
        """
        Create prototype texts for each clause type.
        
        Returns:
            Dict[str, str]: Mapping of clause types to representative texts
        """
        return {
            'termination': [
                "Either party may terminate this agreement upon written notice",
                "This contract may be terminated by either party with 30 days notice",
                "Termination of this agreement requires written consent",
                "The parties agree that termination shall be effective immediately",
                "Upon termination, all obligations cease to exist"
            ],
            'liability': [
                "The parties shall be liable for any damages caused by breach",
                "Limitation of liability clause applies to all claims",
                "Neither party shall be liable for consequential damages",
                "The maximum liability is limited to the contract value",
                "Liability for negligence is excluded under this agreement"
            ],
            'indemnity': [
                "The indemnifying party shall defend and indemnify the other",
                "Indemnification covers all claims, damages, and expenses",
                "The party agrees to indemnify against third-party claims",
                "Full indemnification for any losses or damages incurred",
                "Indemnitor shall hold harmless the indemnified party"
            ],
            'jurisdiction': [
                "This agreement shall be governed by the laws of",
                "Any disputes shall be resolved in the courts of",
                "The exclusive jurisdiction is in the state courts",
                "Governing law and jurisdiction provisions apply",
                "Legal proceedings shall be conducted in the appropriate jurisdiction"
            ],
            'confidentiality': [
                "All information shared shall remain confidential",
                "The receiving party must maintain confidentiality of trade secrets",
                "Confidential information shall not be disclosed to third parties",
                "This confidentiality obligation survives termination",
                "Both parties agree to protect proprietary information"
            ],
            'payment': [
                "Payment shall be made within 30 days of invoice",
                "The buyer shall pay the seller the agreed amount",
                "Payment terms are net 30 days from receipt",
                "All payments shall be made in US dollars",
                "Late payments shall incur interest at the specified rate"
            ],
            'general': [
                "This agreement constitutes the entire understanding",
                "The parties acknowledge they have read and understood",
                "This clause contains general provisions",
                "Miscellaneous terms and conditions apply",
                "General provisions of the contract"
            ]
        }
    
    def load_prototypes(self) -> bool:
        """
        Load and compute prototype vectors for clause types.
        
        Returns:
            bool: True if prototypes loaded successfully, False otherwise
        """
        try:
            if not load_model():
                logger.error("Embedding model not loaded - cannot create prototypes")
                return False
            
            logger.info("Creating semantic prototypes for clause types")
            
            prototype_texts = self._create_prototype_texts()
            
            for clause_type, texts in prototype_texts.items():
                # Create dummy clauses for embedding generation
                dummy_clauses = [{"text": text} for text in texts]
                embeddings = generate_embeddings(dummy_clauses)
                
                if embeddings is not None and len(embeddings) > 0:
                    # Use mean of embeddings as prototype vector
                    prototype_vector = np.mean(embeddings, axis=0)
                    self.prototype_vectors[clause_type] = prototype_vector
                    logger.debug(f"Created prototype for {clause_type}: {prototype_vector.shape}")
                else:
                    logger.error(f"Failed to generate embeddings for {clause_type}")
                    return False
                
                logger.debug(f"Created prototype for {clause_type}: {prototype_vector.shape}")
            
            self._prototypes_loaded = True
            logger.info(f"Loaded {len(self.prototype_vectors)} semantic prototypes")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load prototypes: {e}")
            self._prototypes_loaded = False
            return False
    
    def classify_clauses(self, clauses: List[Dict[str, Any]], embeddings: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """
        Classify clauses based on semantic similarity to prototypes.
        
        Args:
            clauses: List of clause dictionaries
            embeddings: Pre-computed embeddings (optional)
            
        Returns:
            List[Dict[str, Any]]: Updated clauses with type and confidence
        """
        if not self._prototypes_loaded:
            if not self.load_prototypes():
                logger.error("Cannot classify - prototypes not loaded")
                return clauses
        
        try:
            # Generate embeddings if not provided
            if embeddings is None:
                embeddings = generate_embeddings(clauses)
                if embeddings is None:
                    logger.error("Failed to generate embeddings for classification")
                    return clauses
            
            logger.info(f"Classifying {len(clauses)} clauses semantically")
            
            classified_clauses = []
            
            for i, clause in enumerate(clauses):
                if i >= len(embeddings):
                    logger.warning(f"Clause {i} has no corresponding embedding")
                    classified_clauses.append(clause)
                    continue
                
                clause_embedding = embeddings[i].reshape(1, -1)
                
                # Calculate similarity to each prototype
                similarities = {}
                for clause_type, prototype_vector in self.prototype_vectors.items():
                    prototype = prototype_vector.reshape(1, -1)
                    similarity = cosine_similarity(clause_embedding, prototype)[0][0]
                    similarities[clause_type] = similarity
                
                # Find best match
                best_type = max(similarities, key=similarities.get)
                confidence = similarities[best_type]
                
                # Update clause with classification
                updated_clause = clause.copy()
                updated_clause['type'] = best_type
                updated_clause['confidence'] = float(confidence)
                
                classified_clauses.append(updated_clause)
                
                logger.debug(f"Clause {i+1}: {best_type} (confidence: {confidence:.3f})")
            
            logger.info(f"Successfully classified {len(classified_clauses)} clauses")
            return classified_clauses
            
        except Exception as e:
            logger.error(f"Failed to classify clauses: {e}")
            return clauses

# Global service instance
semantic_classifier = SemanticClassifier()

def classify_clauses(clauses: List[Dict[str, Any]], embeddings: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
    """Classify clauses using global semantic classifier."""
    return semantic_classifier.classify_clauses(clauses, embeddings)
