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
        Create standardized response structure with strategic intelligence.
        
        Args:
            filename (str): Original filename
            document_text (str): Extracted document text
            extracted_clauses (List[Dict[str, Any]]): Raw extracted clauses
            classified_clauses (List[Dict[str, Any]]): Classified clauses
            standardized_clauses (List[Dict[str, Any]]): Final standardized clauses
            
        Returns:
            Dict[str, Any]: Complete response structure with strategic intelligence
        """
        # Calculate summary statistics
        high_priority_count = len([c for c in standardized_clauses if c['color'] == 'red'])
        medium_priority_count = len([c for c in standardized_clauses if c['color'] == 'yellow'])
        low_priority_count = len([c for c in standardized_clauses if c['color'] == 'green'])
        clause_types = list(set([c['type'] for c in standardized_clauses]))
        
        # Generate strategic intelligence summary
        strategic_summary = self._generate_strategic_summary(standardized_clauses)
        
        response = {
            "status": "success",
            "filename": filename,
            "analysis_method": "semantic" if self.semantic_enabled else "keyword",
            "document_stats": {
                "total_characters": len(document_text),
                "total_clauses": len(extracted_clauses),
                "classified_clauses": len(classified_clauses),
                "ranked_clauses": len(standardized_clauses),
            },
            "clauses": standardized_clauses,
            "strategic_intelligence": strategic_summary,
            "summary": {
                "high_priority_count": high_priority_count,
                "medium_priority_count": medium_priority_count,
                "low_priority_count": low_priority_count,
                "clause_types": clause_types,
            }
        }
        
        return response
    
    def _generate_strategic_summary(self, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate strategic intelligence summary for all clauses.
        
        Args:
            clauses (List[Dict[str, Any]]): Standardized clauses
            
        Returns:
            Dict[str, Any]: Strategic intelligence summary
        """
        if not clauses:
            return {
                "case_summary": "No clauses available for analysis.",
                "case_type": "Unknown",
                "core_legal_issue": "No legal issues identified.",
                "jurisdiction": "Unknown",
                "primary_risk_domain": "None",
                "constitutional_articles_triggered": [],
                "primary_risk_domain": "None",
                "risk_strength_index": 0.0,
                "risk_category": "low",
                "ai_confidence": 0.0,
                "risk_distribution": {"high": 0, "medium": 0, "low": 0},
                "strength_comparison": {"offensive_strength": 0.0, "defensive_strength": 0.0},
                "strategic_recommendations": []
            }
        
        # Calculate risk distribution
        risk_distribution = {"high": 0, "medium": 0, "low": 0}
        for clause in clauses:
            risk_level = clause.get('risk_level', 'unknown')
            if risk_level in risk_distribution:
                risk_distribution[risk_level] += 1
        
        # Calculate risk strength index (0-1 scale)
        high_weight = len([c for c in clauses if c.get('risk_level') == 'high'])
        medium_weight = len([c for c in clauses if c.get('risk_level') == 'medium'])
        low_weight = len([c for c in clauses if c.get('risk_level') == 'low'])
        
        total_clauses = len(clauses)
        if total_clauses == 0:
            risk_strength_index = 0.0
        else:
            # Weighted calculation: High=1.0, Medium=0.5, Low=0.25
            weighted_score = (high_weight * 1.0 + medium_weight * 0.5 + low_weight * 0.25) / total_clauses
            risk_strength_index = min(weighted_score, 1.0)
        
        # Calculate AI confidence based on available data
        ai_confidence = 0.0
        if self.semantic_enabled:
            ai_confidence = 0.85  # High confidence with semantic analysis
        else:
            ai_confidence = 0.65  # Moderate confidence with keyword analysis
        
        # Determine risk category
        if risk_strength_index <= 0.33:
            risk_category = "low"
        elif risk_strength_index <= 0.66:
            risk_category = "moderate"
        else:
            risk_category = "high"
        
        # Generate case summary and analysis
        case_summary, case_type, core_legal_issue, jurisdiction, primary_risk_domain = self._analyze_case_overview(clauses)
        
        # Identify triggered constitutional articles
        constitutional_articles = []
        for clause in clauses:
            ref = clause.get('constitution_reference', '')
            if ref and 'Article' in ref:
                article_num = ref.split('Article')[1].strip().split(':')[0].strip()
                if article_num not in constitutional_articles:
                    constitutional_articles.append(article_num)
        
        # Generate strategic recommendations
        strategic_recommendations = self._generate_strategic_recommendations(clauses, risk_category)
        
        return {
            "case_summary": case_summary,
            "case_type": case_type,
            "core_legal_issue": core_legal_issue,
            "jurisdiction": jurisdiction,
            "primary_risk_domain": primary_risk_domain,
            "constitutional_articles_triggered": constitutional_articles,
            "primary_risk_domain": primary_risk_domain,
            "risk_strength_index": round(risk_strength_index, 2),
            "risk_category": risk_category,
            "ai_confidence": round(ai_confidence, 2),
            "risk_distribution": risk_distribution,
            "strength_comparison": {
                "offensive_strength": round(self._calculate_offensive_strength(clauses), 2),
                "defensive_strength": round(self._calculate_defensive_strength(clauses), 2)
            },
            "strategic_recommendations": strategic_recommendations
        }
    
    def _analyze_case_overview(self, clauses: List[Dict[str, Any]]) -> tuple:
        """
        Analyze case overview based on clause patterns.
        
        Args:
            clauses (List[Dict[str, Any]]): Standardized clauses
            
        Returns:
            tuple: (case_summary, case_type, core_legal_issue, jurisdiction, primary_risk_domain)
        """
        if not clauses:
            return ("No clauses available for analysis", "Unknown", "No legal issues identified.", "Unknown", "None")
        
        # Analyze clause types to determine case characteristics
        clause_types = [c.get('type', 'unknown') for c in clauses]
        
        # Determine case type based on clause patterns
        if 'termination' in clause_types or 'notice' in clause_types:
            case_type = "Employment Termination"
            core_legal_issue = "Termination compliance and notice period requirements"
            primary_risk_domain = "Employment Law"
        elif 'confidentiality' in clause_types or 'proprietary' in clause_types:
            case_type = "Confidentiality & IP Protection"
            core_legal_issue = "Information protection and trade secret compliance"
            primary_risk_domain = "Intellectual Property Law"
        elif 'non-compete' in clause_types or 'non-solicitation' in clause_types:
            case_type = "Restrictive Covenants"
            core_legal_issue = "Enforceability of non-compete and non-solicitation clauses"
            primary_risk_domain = "Contract Law"
        elif 'indemnification' in clause_types:
            case_type = "Risk Allocation"
            core_legal_issue = "Indemnification and liability exposure"
            primary_risk_domain = "Insurance & Liability Law"
        else:
            case_type = "General Contract"
            core_legal_issue = "Standard contractual terms and conditions"
            primary_risk_domain = "Contract Law"
        
        # Generate summary
        high_risk_count = len([c for c in clauses if c.get('risk_level') == 'high'])
        total_clauses = len(clauses)
        
        if high_risk_count > total_clauses * 0.5:
            summary = f"High-risk case with {high_risk_count} of {total_clauses} clauses requiring immediate attention and potential renegotiation."
        elif high_risk_count > 0:
            summary = f"Mixed-risk case with {high_risk_count} high-risk clauses among {total_clauses} total provisions requiring careful review."
        else:
            summary = f"Standard case with {total_clauses} clauses appearing to follow conventional contractual patterns with moderate risk exposure."
        
        jurisdiction = "Multi-jurisdictional (US/International applicable)"
        
        return (summary, case_type, core_legal_issue, jurisdiction, primary_risk_domain)
    
    def _calculate_offensive_strength(self, clauses: List[Dict[str, Any]]) -> float:
        """
        Calculate offensive strength (employer's advantage).
        
        Args:
            clauses (List[Dict[str, Any]]): Standardized clauses
            
        Returns:
            float: Offensive strength score (0-1 scale)
        """
        offensive_factors = []
        
        # Analyze restrictive clauses
        non_compete_count = len([c for c in clauses if c.get('type') == 'non-compete'])
        non_solicitation_count = len([c for c in clauses if c.get('type') == 'non-solicitation'])
        indemnification_count = len([c for c in clauses if c.get('type') == 'indemnification'])
        
        # High offensive strength for restrictive clauses
        if non_compete_count > 0:
            offensive_factors.append(0.3)  # Non-compete restrictions
        if non_solicitation_count > 0:
            offensive_factors.append(0.2)  # Non-solicitation restrictions
        if indemnification_count > 0:
            offensive_factors.append(0.25)  # Indemnification shifts risk to employee
        
        # Analyze termination flexibility
        termination_count = len([c for c in clauses if c.get('type') == 'termination'])
        if termination_count > 0:
            offensive_factors.append(0.15)  # Easy termination
        
        # Calculate base offensive strength
        base_offensive = sum(offensive_factors)
        
        # Cap at 1.0 and normalize by clause count
        return min(base_offensive + (len(clauses) * 0.05), 1.0)
    
    def _calculate_defensive_strength(self, clauses: List[Dict[str, Any]]) -> float:
        """
        Calculate defensive strength (employee's protection).
        
        Args:
            clauses (List[Dict[str, Any]]): Standardized clauses
            
        Returns:
            float: Defensive strength score (0-1 scale)
        """
        defensive_factors = []
        
        # Analyze protective clauses
        benefits_count = len([c for c in clauses if c.get('type') == 'benefits'])
        confidentiality_count = len([c for c in clauses if c.get('type') == 'confidentiality'])
        working_hours_count = len([c for c in clauses if c.get('type') == 'working_hours'])
        
        # High defensive strength for protective clauses
        if benefits_count > 0:
            defensive_factors.append(0.25)  # Benefits protection
        if confidentiality_count > 0:
            defensive_factors.append(0.2)   # Confidentiality limits employer
        if working_hours_count > 0:
            defensive_factors.append(0.15)  # Working hours protection
        
        # Analyze limitation clauses
        limitation_count = len([c for c in clauses if 'limit' in c.get('text', '').lower() or 'restriction' in c.get('text', '').lower()])
        if limitation_count > 0:
            defensive_factors.append(0.1)  # Limitations on employer
        
        # Calculate base defensive strength
        base_defensive = sum(defensive_factors)
        
        # Cap at 1.0 and normalize by clause count
        return min(base_defensive + (len(clauses) * 0.05), 1.0)
    
    def _generate_strategic_recommendations(self, clauses: List[Dict[str, Any]], risk_category: str) -> List[str]:
        """
        Generate strategic recommendations based on risk analysis.
        
        Args:
            clauses (List[Dict[str, Any]]): Standardized clauses
            risk_category (str): Risk category (low/moderate/high)
            
        Returns:
            List[str]: Strategic recommendations
        """
        recommendations = []
        
        # High-risk recommendations
        if risk_category == 'high':
            recommendations.extend([
                "Immediate legal review required before signing",
                "Negotiate removal or modification of high-risk clauses",
                "Document all verbal promises made during negotiations",
                "Consider alternative employment arrangements if terms are unfavorable",
                "Seek professional legal counsel specializing in employment law",
                "Request written clarification of ambiguous terms",
                "Preserve all communications regarding problematic clauses"
            ])
        
        # Moderate-risk recommendations
        elif risk_category == 'moderate':
            recommendations.extend([
                "Legal review recommended for moderate-risk provisions",
                "Request modifications to unclear or unfavorable terms",
                "Negotiate for more balanced risk allocation",
                "Ensure compliance with applicable labor laws",
                "Document any agreed modifications in writing",
                "Consider time limitations on restrictive clauses"
            ])
        
        # Low-risk recommendations
        else:
            recommendations.extend([
                "Standard legal review still advisable",
                "Ensure understanding of all obligations and rights",
                "Maintain copies of all signed agreements",
                "Review for any hidden fees or unusual provisions",
                "Confirm compliance with industry standards"
            ])
        
        # Add specific recommendations based on clause types
        clause_types = [c.get('type', 'unknown') for c in clauses]
        
        if 'termination' in clause_types:
            recommendations.append("Negotiate for longer notice periods and severance provisions")
        if 'non-compete' in clause_types:
            recommendations.append("Challenge geographic scope and duration limitations")
        if 'confidentiality' in clause_types:
            recommendations.append("Define clear boundaries for confidential information")
        if 'indemnification' in clause_types:
            recommendations.append("Negotiate for mutual indemnification and liability caps")
        
        return recommendations
    
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
