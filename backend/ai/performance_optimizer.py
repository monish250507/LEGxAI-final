"""
Performance Optimizer - Caching and Efficiency Improvements

Provides caching for constitution embeddings, API responses, and other performance optimizations.
"""

import os
import json
import hashlib
import time
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """
    Performance optimization service with caching and efficiency improvements.
    """
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Cache files
        self.embedding_cache_file = self.cache_dir / "constitution_embeddings.json"
        self.api_cache_file = self.cache_dir / "api_responses.json"
        
        # In-memory caches
        self.embedding_cache = {}
        self.api_cache = {}
        self.constitution_cache = {}
        
        # Performance metrics
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_calls = 0
        
        # Load existing caches
        self._load_caches()
    
    def _load_caches(self):
        """Load existing caches from disk."""
        try:
            # Load embedding cache
            if self.embedding_cache_file.exists():
                with open(self.embedding_cache_file, 'r') as f:
                    self.embedding_cache = json.load(f)
                logger.info(f"Loaded {len(self.embedding_cache)} cached embeddings")
            
            # Load API cache
            if self.api_cache_file.exists():
                with open(self.api_cache_file, 'r') as f:
                    self.api_cache = json.load(f)
                logger.info(f"Loaded {len(self.api_cache)} cached API responses")
                
        except Exception as e:
            logger.warning(f"Failed to load caches: {e}")
    
    def _save_caches(self):
        """Save caches to disk."""
        try:
            # Save embedding cache
            with open(self.embedding_cache_file, 'w') as f:
                json.dump(self.embedding_cache, f, indent=2)
            
            # Save API cache
            with open(self.api_cache_file, 'w') as f:
                json.dump(self.api_cache, f, indent=2)
                
        except Exception as e:
            logger.warning(f"Failed to save caches: {e}")
    
    def _generate_cache_key(self, text: str, prefix: str = "") -> str:
        """Generate a cache key for text content."""
        # Use SHA-256 hash for consistent keys
        content = f"{prefix}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get_cached_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get cached embedding for text.
        
        Args:
            text: Text to get embedding for
            
        Returns:
            Cached embedding or None if not found
        """
        cache_key = self._generate_cache_key(text, "embedding")
        
        if cache_key in self.embedding_cache:
            self.cache_hits += 1
            return self.embedding_cache[cache_key]
        
        self.cache_misses += 1
        return None
    
    def cache_embedding(self, text: str, embedding: List[float]):
        """
        Cache embedding for text.
        
        Args:
            text: Text to cache embedding for
            embedding: Embedding to cache
        """
        cache_key = self._generate_cache_key(text, "embedding")
        self.embedding_cache[cache_key] = embedding
        
        # Periodically save to disk
        if len(self.embedding_cache) % 10 == 0:
            self._save_caches()
    
    def get_cached_api_response(self, clause_text: str, constitution: str, clause_type: str) -> Optional[Dict[str, Any]]:
        """
        Get cached API response for clause analysis.
        
        Args:
            clause_text: Clause text
            constitution: Constitution context
            clause_type: Clause type
            
        Returns:
            Cached API response or None if not found
        """
        cache_key = self._generate_cache_key(f"{clause_text}:{constitution}:{clause_type}", "api")
        
        if cache_key in self.api_cache:
            # Check if cache is recent (within 24 hours)
            cache_entry = self.api_cache[cache_key]
            if time.time() - cache_entry.get('timestamp', 0) < 86400:  # 24 hours
                self.cache_hits += 1
                return cache_entry.get('response')
            else:
                # Remove expired cache entry
                del self.api_cache[cache_key]
        
        self.cache_misses += 1
        return None
    
    def cache_api_response(self, clause_text: str, constitution: str, clause_type: str, response: Dict[str, Any]):
        """
        Cache API response for clause analysis.
        
        Args:
            clause_text: Clause text
            constitution: Constitution context
            clause_type: Clause type
            response: API response to cache
        """
        cache_key = self._generate_cache_key(f"{clause_text}:{constitution}:{clause_type}", "api")
        
        self.api_cache[cache_key] = {
            'response': response,
            'timestamp': time.time()
        }
        
        self.api_calls += 1
        
        # Periodically save to disk
        if len(self.api_cache) % 5 == 0:
            self._save_caches()
    
    def get_constitution_embeddings(self, constitution_name: str) -> Optional[Dict[str, Any]]:
        """
        Get cached constitution embeddings.
        
        Args:
            constitution_name: Name of constitution
            
        Returns:
            Cached constitution data or None if not found
        """
        return self.constitution_cache.get(constitution_name)
    
    def cache_constitution_embeddings(self, constitution_name: str, articles: List[Dict], embeddings: List[List[float]]):
        """
        Cache constitution embeddings.
        
        Args:
            constitution_name: Name of constitution
            articles: List of constitution articles
            embeddings: List of embeddings for articles
        """
        self.constitution_cache[constitution_name] = {
            'articles': articles,
            'embeddings': embeddings,
            'timestamp': time.time()
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics.
        
        Returns:
            Dictionary with performance metrics
        """
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate_percent': round(hit_rate, 2),
            'api_calls': self.api_calls,
            'embedding_cache_size': len(self.embedding_cache),
            'api_cache_size': len(self.api_cache),
            'constitution_cache_size': len(self.constitution_cache)
        }
    
    def clear_caches(self):
        """Clear all caches."""
        self.embedding_cache.clear()
        self.api_cache.clear()
        self.constitution_cache.clear()
        
        # Remove cache files
        if self.embedding_cache_file.exists():
            self.embedding_cache_file.unlink()
        if self.api_cache_file.exists():
            self.api_cache_file.unlink()
        
        logger.info("All caches cleared")
    
    def optimize_batch_size(self, items: List[Any], max_batch_size: int = 10) -> List[List[Any]]:
        """
        Optimize batch size for processing.
        
        Args:
            items: List of items to process
            max_batch_size: Maximum batch size
            
        Returns:
            List of batches
        """
        batches = []
        for i in range(0, len(items), max_batch_size):
            batches.append(items[i:i + max_batch_size])
        
        return batches

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

def get_performance_optimizer() -> PerformanceOptimizer:
    """Get the global performance optimizer instance."""
    return performance_optimizer
