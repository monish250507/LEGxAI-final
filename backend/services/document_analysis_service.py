"""
Document Analysis Service - Orchestrates the complete clause analysis pipeline.
"""

import logging
from typing import List, Dict, Any, Optional
from fastapi import UploadFile
from document_processor import extract_text
from clause_extractor import extract_clauses
from clause_classifier import classify_multiple_clauses
from clause_ranker import rank_clauses_by_importance
from database import save_analysis_result

# Try to import semantic components
try:
    from ai.embedding_service import load_model, generate_embeddings
    from ai.semantic_classifier import semantic_classifier, classify_clauses as semantic_classify
    from ai.semantic_ranker import semantic_ranker, rank_clauses as semantic_rank
    from ai.generative_service import generate_clause_explanation, generate_full_clause_analysis
    from ai.constitution_matcher import ConstitutionMatcher
    SEMANTIC_AVAILABLE = True
except ImportError as e:
    SEMANTIC_AVAILABLE = False
    generate_embeddings = None
    semantic_classifier = None
    semantic_ranker = None
    semantic_classify = None
    semantic_rank = None
    generate_clause_explanation = None
    generate_full_clause_analysis = None
    ConstitutionMatcher = None
    logging.warning(f"Semantic components not available: {e}")

# Configure logging
logger = logging.getLogger(__name__)

class DocumentAnalysisService:
    """
    Service class that orchestrates the complete document analysis pipeline.
    
    Pipeline Flow (with semantic enhancement):
    UploadFile → document_processor.process_document() → 
    clause_extractor.extract_clauses() → 
    [semantic embeddings → semantic_classifier → semantic_ranker] OR 
    [keyword_classifier → keyword_ranker] (fallback) → 
    structured JSON response
    """
    
    def __init__(self):
        self.supported_formats = {'.pdf', '.txt', '.docx', '.json'}
        self.semantic_enabled = False
        self.constitution_matcher = None
        
        # Initialize semantic components if available
        if SEMANTIC_AVAILABLE:
            self._initialize_semantic_components()
    
    def _initialize_semantic_components(self) -> bool:
        """
        Initialize semantic components for enhanced analysis.
        
        Returns:
            bool: True if semantic components initialized successfully
        """
        try:
            logger.info("Initializing semantic components...")
            
            # Load embedding model
            if load_model and load_model():
                logger.info("Embedding model loaded successfully")
                
                # Load semantic classifier prototypes
                if semantic_classifier and semantic_classifier.load_prototypes():
                    logger.info("Semantic classifier prototypes loaded")
                    self.semantic_enabled = True
                    
                    # Initialize constitution matcher
                    if ConstitutionMatcher:
                        self.constitution_matcher = ConstitutionMatcher()
                        if self.constitution_matcher.load_constitutions():
                            logger.info("Constitution matcher loaded successfully")
                        else:
                            logger.warning("Failed to load constitution matcher")
                    
                    return True
                else:
                    logger.warning("Failed to load semantic classifier prototypes")
            else:
                logger.warning("Failed to load embedding model")
                
        except Exception as e:
            logger.error(f"Failed to initialize semantic components: {e}")
        
        self.semantic_enabled = False
        return False
    
    async def analyze_document(self, file: UploadFile, constitution: str = "US Constitution") -> Dict[str, Any]:
        """
        Analyze uploaded document through complete pipeline.
        
        Args:
            file (UploadFile): Uploaded file object
            constitution (str): Selected constitution for legal context
            
        Returns:
            Dict[str, Any]: Complete analysis result with standardized structure
            
        Raises:
            ValueError: For invalid input or processing failures
        """
        try:
            # Step 1: Process document and extract text
            logger.info(f"Starting document analysis for: {file.filename}")
            
            # Reset file pointer to ensure we can read it
            await file.seek(0)
            
            # Read file content for text files
            if file.filename and file.filename.lower().endswith('.txt'):
                content = await file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='ignore')
                document_text = content
            else:
                # Use extract_text for other files
                document_text = extract_text(file)
            
            if not document_text or not document_text.strip():
                raise ValueError("No text could be extracted from document")
            
            logger.info(f"Extracted {len(document_text)} characters from document")
            
            # Step 2: Extract clauses
            logger.info("Extracting clauses from document")
            extracted_clauses = extract_clauses(document_text)
            
            if not extracted_clauses:
                raise ValueError("No clauses could be extracted from document")
            
            logger.info(f"Extracted {len(extracted_clauses)} clauses")
            
            # Step 3: Classify and rank clauses (semantic or fallback)
            logger.info("Classifying and ranking clauses")
            
            if self.semantic_enabled:
                logger.info("Using semantic analysis pipeline")
                
                # Generate embeddings
                logger.info("Generating embeddings for clauses")
                embeddings = generate_embeddings(extracted_clauses)
                
                if embeddings is not None:
                    # Semantic classification
                    logger.info("Classifying clauses semantically")
                    classified_clauses = semantic_classify(extracted_clauses, embeddings)
                    
                    # Semantic ranking
                    logger.info("Ranking clauses semantically")
                    ranked_clauses = semantic_rank(classified_clauses)
                    
                    logger.info(f"Semantic analysis completed: {len(ranked_clauses)} clauses")
                else:
                    logger.warning("Failed to generate embeddings, falling back to keyword analysis")
                    classified_clauses = classify_multiple_clauses(extracted_clauses)
                    ranked_clauses = rank_clauses_by_importance(classified_clauses)
            else:
                logger.info("Using keyword-based analysis pipeline (fallback)")
                # Fallback to original keyword-based pipeline
                classified_clauses = classify_multiple_clauses(extracted_clauses)
                ranked_clauses = rank_clauses_by_importance(classified_clauses)
            
            if not ranked_clauses:
                raise ValueError("Failed to rank clauses")
            
            logger.info(f"Processed {len(ranked_clauses)} clauses")
            
            # Step 4: Constitution matching and comprehensive analysis
            if self.constitution_matcher and generate_full_clause_analysis:
                logger.info("Performing constitution matching and comprehensive analysis")
                
                for clause in ranked_clauses:
                    try:
                        # Find relevant constitution article
                        matched_article = None
                        if self.constitution_matcher:
                            # Try to match with the specified constitution
                            constitution_name = constitution.replace(' Constitution', '')
                            matches = self.constitution_matcher.match_constitution_sections(
                                clause["text"], 
                                constitution_name, 
                                top_k=1
                            )
                            if matches:
                                matched_article = matches[0]
                        
                        # Generate comprehensive analysis
                        analysis = generate_full_clause_analysis(
                            clause["text"],
                            constitution,
                            clause["type"],
                            matched_article
                        )
                        
                        # Add comprehensive analysis to clause
                        clause["explanation"] = analysis.get("explanation", "No explanation available.")
                        clause["offensive_analysis"] = analysis.get("offensive_analysis", "No offensive analysis available.")
                        clause["defensive_analysis"] = analysis.get("defensive_analysis", "No defensive analysis available.")
                        clause["constitution_reference"] = analysis.get("constitution_reference", "")
                        clause["risk_level"] = analysis.get("risk_level", "unknown")
                        
                    except Exception as e:
                        logger.warning(f"Failed to generate comprehensive analysis for clause: {e}")
                        clause["explanation"] = "AI explanation unavailable."
                        clause["offensive_analysis"] = "Unavailable"
                        clause["defensive_analysis"] = "Unavailable"
                        clause["constitution_reference"] = ""
                        clause["risk_level"] = "unknown"
            
            # Fallback to simple explanation if comprehensive analysis not available
            elif generate_clause_explanation:
                logger.info("Generating simple explanations for clauses")
                
                for clause in ranked_clauses:
                    try:
                        explanation = generate_clause_explanation(
                            clause["text"],
                            constitution,
                            clause["type"]
                        )
                        clause["explanation"] = explanation
                        clause["offensive_analysis"] = "Unavailable"
                        clause["defensive_analysis"] = "Unavailable"
                        clause["constitution_reference"] = ""
                        clause["risk_level"] = "unknown"
                    except Exception as e:
                        logger.warning(f"Failed to generate explanation for clause: {e}")
                        clause["explanation"] = "AI explanation unavailable."
                        clause["offensive_analysis"] = "Unavailable"
                        clause["defensive_analysis"] = "Unavailable"
                        clause["constitution_reference"] = ""
                        clause["risk_level"] = "unknown"
            
            # Step 5: Standardize clause structure
            standardized_clauses = self._standardize_clause_structure(ranked_clauses)
            
            # Step 6: Create response structure
            response = self._create_response_structure(
                file.filename, 
                document_text, 
                extracted_clauses, 
                classified_clauses, 
                standardized_clauses
            )
            
            # Step 7: Save to database (optional)
            try:
                import os
                from config import UPLOAD_DIR
                file_path = os.path.join(UPLOAD_DIR, file.filename or "unknown")
                save_analysis_result(file.filename or "unknown", file_path, standardized_clauses)
                logger.info("Analysis result saved to database")
            except Exception as e:
                logger.warning(f"Failed to save to database: {e}")
            
            logger.info(f"Successfully analyzed document: {file.filename}")
            return response
            
        except Exception as e:
            logger.error(f"Document analysis failed: {str(e)}")
            raise ValueError(f"Document analysis failed: {str(e)}")
    
    def _standardize_clause_structure(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Standardize clause structure to match required format.
        
        Args:
            clauses (List[Dict[str, Any]]): Raw clauses from ranking
            
        Returns:
            List[Dict[str, Any]]: Standardized clauses
        """
        standardized = []
        
        for clause in clauses:
            standardized_clause = {
                "clause_id": clause.get('clause_id', ''),
                "text": clause.get('text', ''),
                "type": clause.get('type', 'general'),
                "confidence": float(clause.get('confidence', 0.0)),
                "priority_score": float(clause.get('priority_score', 0.0)),
                "color": clause.get('color', 'green'),
                "rank": int(clause.get('rank', 0)),
                "explanation": clause.get('explanation', None),
                "offensive_analysis": clause.get('offensive_analysis', None),
                "defensive_analysis": clause.get('defensive_analysis', None),
                "constitution_reference": clause.get('constitution_reference', ''),
                "risk_level": clause.get('risk_level', 'unknown')
            }
            standardized.append(standardized_clause)
        
        return standardized
    
    def _create_response_structure(
        self, 
        filename: str, 
        document_text: str, 
        extracted_clauses: List[Dict[str, Any]], 
        classified_clauses: List[Dict[str, Any]], 
        standardized_clauses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create standardized response structure.
        
        Args:
            filename (str): Original filename
            document_text (str): Extracted document text
            extracted_clauses (List[Dict[str, Any]]): Raw extracted clauses
            classified_clauses (List[Dict[str, Any]]): Classified clauses
            standardized_clauses (List[Dict[str, Any]]): Final standardized clauses
            
        Returns:
            Dict[str, Any]: Complete response structure
        """
        # Calculate summary statistics
        high_priority_count = len([c for c in standardized_clauses if c['color'] == 'red'])
        medium_priority_count = len([c for c in standardized_clauses if c['color'] == 'yellow'])
        low_priority_count = len([c for c in standardized_clauses if c['color'] == 'green'])
        clause_types = list(set([c['type'] for c in standardized_clauses]))
        
        response = {
            "status": "success",
            "filename": filename,
            "analysis_method": "semantic" if self.semantic_enabled else "keyword",
            "document_stats": {
                "total_characters": len(document_text),
                "total_clauses": len(extracted_clauses),
                "classified_clauses": len(classified_clauses),
                "ranked_clauses": len(standardized_clauses)
            },
            "clauses": standardized_clauses,
            "summary": {
                "high_priority_count": high_priority_count,
                "medium_priority_count": medium_priority_count,
                "low_priority_count": low_priority_count,
                "clause_types": clause_types
            }
        }
        
        return response
    
    def validate_file_format(self, filename: str) -> bool:
        """
        Validate if file format is supported.
        
        Args:
            filename (str): Filename to validate
            
        Returns:
            bool: True if format is supported
        """
        if not filename:
            return False
        
        file_ext = '.' + filename.lower().split('.')[-1] if '.' in filename else ''
        return file_ext in self.supported_formats
    
    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.
        
        Returns:
            List[str]: Supported file extensions
        """
        return list(self.supported_formats)
    
    def is_semantic_enabled(self) -> bool:
        """
        Check if semantic analysis is enabled.
        
        Returns:
            bool: True if semantic analysis is available and enabled
        """
        return self.semantic_enabled
    
    def get_analysis_status(self) -> Dict[str, Any]:
        """
        Get the current analysis status and capabilities.
        
        Returns:
            Dict[str, Any]: Status information
        """
        return {
            "semantic_available": SEMANTIC_AVAILABLE,
            "semantic_enabled": self.semantic_enabled,
            "analysis_method": "semantic" if self.semantic_enabled else "keyword",
            "model_loaded": embedding_service.is_model_loaded() if embedding_service else False
        }

# Global service instance
document_analysis_service = DocumentAnalysisService()
