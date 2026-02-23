"""
Constitution Matcher - Constitution-Aware Semantic Matching

This module provides constitution-aware semantic matching for legal clauses,
enabling the system to identify relevant constitution articles based on
semantic similarity.
"""

import os
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
import logging
from performance_optimizer import get_performance_optimizer

logger = logging.getLogger(__name__)

class ConstitutionMatcher:
    """
    Constitution-aware semantic matcher for legal clauses.
    """
    
    def __init__(self, embedding_service=None):
        """
        Initialize the constitution matcher.
        
        Args:
            embedding_service: Embedding service for generating embeddings
        """
        self.embedding_service = embedding_service
        self.constitutions = {}
        self.constitution_embeddings = {}
        self.data_dir = 'data'
        self.performance_optimizer = get_performance_optimizer()
        
        # Import embedding service if not provided
        if not self.embedding_service:
            import embedding_service
            self.embedding_service = embedding_service
        
    def load_constitutions(self) -> bool:
        """
        Load all constitution JSON files and generate embeddings.
        
        Returns:
            bool: True if loading successful
        """
        try:
            constitution_files = [
                'COI.json',
                'China_2018.json', 
                'Japan_1946.json',
                'Russia_2014.json'
            ]
            
            for filename in constitution_files:
                filepath = os.path.join(self.data_dir, filename)
                if os.path.exists(filepath):
                    # Check if already cached
                    constitution_name = filename.replace('.json', '')
                    cached_data = self.performance_optimizer.get_constitution_embeddings(constitution_name)
                    
                    if cached_data:
                        # Load from cache
                        self.constitutions[constitution_name] = cached_data['articles']
                        self.constitution_embeddings[constitution_name] = {
                            'articles': cached_data['articles'],
                            'embeddings': cached_data['embeddings']
                        }
                        logger.info(f"Loaded {constitution_name} constitution from cache")
                    else:
                        # Load from file and generate embeddings
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Extract constitution name from filename
                        constitution_name = filename.replace('.json', '')
                        self.constitutions[constitution_name] = data
                        
                        # Generate embeddings for this constitution
                        self._generate_constitution_embeddings(constitution_name, data)
                        
                        # Cache the results
                        if constitution_name in self.constitution_embeddings:
                            cache_data = self.constitution_embeddings[constitution_name]
                            self.performance_optimizer.cache_constitution_embeddings(
                                constitution_name,
                                cache_data['articles'],
                                cache_data['embeddings']
                            )
                        
                        logger.info(f"Loaded {constitution_name} constitution")
                else:
                    logger.warning(f"Constitution file not found: {filename}")
            
            logger.info(f"Loaded {len(self.constitutions)} constitutions")
            return True
            
        except Exception as e:
            logger.error(f"Error loading constitutions: {e}")
            return False
    
    def _generate_constitution_embeddings(self, constitution_name: str, data: dict) -> None:
        """
        Generate embeddings for constitution articles/sections.
        
        Args:
            constitution_name: Name of the constitution
            data: Constitution data
        """
        try:
            articles = []
            
            # Handle different constitution formats
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                # Nested array format (like COI.json)
                for article in data[0]:
                    if isinstance(article, dict):
                        article_text = self._extract_article_text(article)
                        if article_text:
                            articles.append({
                                'article_number': article.get('ArtNo', 'Unknown'),
                                'title': article.get('Name', 'Unknown'),
                                'text': article_text
                            })
            
            elif 'document' in data and 'section' in data['document']:
                # Document format (like China_2018.json)
                for section in data['document']['section']:
                    section_text = self._extract_section_text(section)
                    if section_text:
                        articles.append({
                            'article_number': section.get('metadata', {}).get('identifier', 'Unknown'),
                            'title': section.get('content', 'Unknown')[:100],
                            'text': section_text
                        })
            
            # Generate embeddings using the embedding service
            if articles:
                article_texts = [article['text'] for article in articles]
                
                # Create clause-like objects for embedding service
                clause_objects = [{'text': text} for text in article_texts]
                embeddings = self.embedding_service.generate_embeddings(clause_objects)
                
                # Store embeddings
                self.constitution_embeddings[constitution_name] = {
                    'articles': articles,
                    'embeddings': embeddings
                }
                
                logger.info(f"Generated embeddings for {len(articles)} articles in {constitution_name}")
            
        except Exception as e:
            logger.error(f"Error generating embeddings for {constitution_name}: {e}")
    
    def _extract_article_text(self, article: dict) -> str:
        """Extract text from article dictionary."""
        text_parts = []
        
        # Try different field names
        for field in ['ArtDesc', 'description', 'text', 'content']:
            if field in article and article[field]:
                text_parts.append(str(article[field]))
        
        # Check for clauses
        if 'Clauses' in article and isinstance(article['Clauses'], list):
            for clause in article['Clauses']:
                if isinstance(clause, dict) and 'ClauseDesc' in clause:
                    text_parts.append(str(clause['ClauseDesc']))
        
        return ' '.join(text_parts).strip()
    
    def _extract_section_text(self, section: dict) -> str:
        """Extract text from section dictionary."""
        text_parts = []
        
        if 'content' in section:
            if isinstance(section['content'], str):
                text_parts.append(section['content'])
            elif isinstance(section['content'], list):
                for content_item in section['content']:
                    if isinstance(content_item, dict) and 'content' in content_item:
                        text_parts.append(str(content_item['content']))
                    elif isinstance(content_item, str):
                        text_parts.append(content_item)
        
        return ' '.join(text_parts).strip()
    
    def match_constitution_sections(self, clause_text: str, constitution_name: str, top_k: int = 3) -> List[Dict]:
        """
        Match clause text against constitution sections.
        
        Args:
            clause_text: Text of the legal clause
            constitution_name: Name of constitution to search
            top_k: Number of top matches to return
            
        Returns:
            List of matching constitution sections with similarity scores
        """
        try:
            if constitution_name not in self.constitution_embeddings:
                logger.warning(f"Constitution not loaded: {constitution_name}")
                return []
            
            constitution_data = self.constitution_embeddings[constitution_name]
            articles = constitution_data['articles']
            embeddings = constitution_data['embeddings']
            
            if len(embeddings) == 0:
                logger.warning(f"No embeddings available for {constitution_name}")
                return []
            
            # Generate embedding for the clause text
            clause_objects = [{'text': clause_text}]
            clause_embedding = self.embedding_service.generate_embeddings(clause_objects)
            
            if len(clause_embedding) == 0:
                logger.warning("Failed to generate embedding for clause text")
                return []
            
            # Calculate cosine similarity
            similarities = cosine_similarity(clause_embedding, embeddings)[0]
            
            # Get top matches
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            matches = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    article = articles[idx]
                    matches.append({
                        'constitution': constitution_name,
                        'article_number': article['article_number'],
                        'title': article['title'],
                        'text': article['text'],
                        'similarity_score': float(similarities[idx])
                    })
            
            logger.info(f"Found {len(matches)} matches for {constitution_name}")
            return matches
            
        except Exception as e:
            logger.error(f"Error matching constitution sections: {e}")
            return []
    
    def get_best_match(self, clause_text: str, constitution_name: str) -> Optional[Dict]:
        """
        Get the best matching constitution section.
        
        Args:
            clause_text: Text of the legal clause
            constitution_name: Name of constitution to search
            
        Returns:
            Best matching section or None
        """
        matches = self.match_constitution_sections(clause_text, constitution_name, top_k=1)
        return matches[0] if matches else None
    
    def search_all_constitutions(self, clause_text: str, top_k: int = 2) -> Dict[str, List[Dict]]:
        """
        Search clause text against all loaded constitutions.
        
        Args:
            clause_text: Text of the legal clause
            top_k: Number of top matches per constitution
            
        Returns:
            Dictionary mapping constitution names to their matches
        """
        results = {}
        
        for constitution_name in self.constitutions:
            matches = self.match_constitution_sections(clause_text, constitution_name, top_k)
            if matches:
                results[constitution_name] = matches
        
        return results
