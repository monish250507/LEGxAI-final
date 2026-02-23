import os
import io
import re
import logging
from typing import Union, BinaryIO
from pathlib import Path

# Try to import pdfplumber, but provide fallback
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    pdfplumber = None
    logging.warning("pdfplumber not available - PDF processing will be limited")

# Try to import OCR libraries
try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    OCR_AVAILABLE = True
except ImportError as e:
    OCR_AVAILABLE = False
    pytesseract = None
    Image = None
    cv2 = None
    np = None
    logging.warning(f"OCR libraries not available: {e}")

# Try to import textract for fallback
try:
    import textract
    TEXTRACT_AVAILABLE = True
except ImportError:
    TEXTRACT_AVAILABLE = False
    textract = None
    logging.warning("textract not available - fallback text extraction will be limited")

from fastapi import UploadFile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Main class for processing legal documents end-to-end.
    Handles text extraction, clause extraction, classification, and ranking.
    """
    
    def __init__(self):
        self.supported_formats = {'.pdf', '.txt', '.docx', '.doc', '.ppt', '.pptx', '.jpg', '.jpeg', '.png'}
    
    def _extract_ocr_text(self, file) -> str:
        """
        Extract text from images using Tesseract OCR.
        
        Args:
            file: Image file object
            
        Returns:
            str: Extracted text content
        """
        try:
            if OCR_AVAILABLE:
                # Read file content
                if hasattr(file, 'read'):
                    content = file.read()
                else:
                    with open(file, 'rb') as f:
                        content = f.read()
                
                # Open image with PIL
                image = Image.open(io.BytesIO(content))
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Preprocess image for better OCR
                img_array = np.array(image)
                
                # Convert to grayscale
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                
                # Apply threshold to get better OCR results
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                # Perform OCR
                text = pytesseract.image_to_string(thresh, lang='eng')
                
                return self._clean_text(text) if text else ""
            else:
                logger.warning("OCR libraries not available - image text extraction limited")
                return "Image file detected. OCR text extraction not available without Tesseract."
        except Exception as e:
            logger.error(f"OCR text extraction failed: {e}")
            return ""
    
    def _extract_ppt_text(self, file) -> str:
        """
        Extract text from PowerPoint files using textract.
        
        Args:
            file: PPT file object
            
        Returns:
            str: Extracted text content
        """
        try:
            if TEXTRACT_AVAILABLE:
                import io
                
                # Read file content
                if hasattr(file, 'read'):
                    content = file.read()
                else:
                    with open(file, 'rb') as f:
                        content = f.read()
                
                # Use textract for PPT files
                text = textract.process(io.BytesIO(content))
                return self._clean_text(text) if text else ""
            else:
                logger.warning("textract not available - PPT text extraction limited")
                return "PowerPoint file detected. Text extraction not available without textract."
        except Exception as e:
            logger.error(f"PPT text extraction failed: {e}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common PDF artifacts
        text = re.sub(r'\f+', ' ', text)  # Form feeds
        text = re.sub(r'\x0c', ' ', text)  # Form feed character
        
        # Fix common OCR issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between words
        
        # Remove non-printable characters except newlines and tabs
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Normalize quotes and dashes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('–', '-').replace('—', '--')
        
        # Strip and return
        return text.strip()
    
    def _extract_pdf_text(self, file: Union[str, BinaryIO, UploadFile]) -> str:
        """
        Extract text from PDF file using pdfplumber.
        
        Args:
            file: File path, file-like object, or UploadFile
            
        Returns:
            str: Extracted text
        """
        try:
            # Handle different file input types
            if isinstance(file, str):
                # File path
                with open(file, 'rb') as f:
                    pdf_content = f.read()
                pdf_stream = io.BytesIO(pdf_content)
            elif isinstance(file, UploadFile):
                # FastAPI UploadFile
                pdf_content = file.file.read()
                file.file.seek(0)  # Reset file pointer
                pdf_stream = io.BytesIO(pdf_content)
            else:
                # File-like object
                if hasattr(file, 'seek'):
                    file.seek(0)
                pdf_stream = file
            
            text_parts = []
            
            with pdfplumber.open(pdf_stream) as pdf:
                total_pages = len(pdf.pages)
                logger.info(f"Processing PDF with {total_pages} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        # Extract text with layout preservation
                        page_text = page.extract_text(x_tolerance=1, y_tolerance=1)
                        
                        if page_text:
                            # Clean page text
                            cleaned_text = self._clean_text(page_text)
                            if cleaned_text:
                                text_parts.append(cleaned_text)
                                
                        logger.debug(f"Processed page {page_num}/{total_pages}")
                        
                    except Exception as e:
                        logger.warning(f"Error processing page {page_num}: {e}")
                        continue
            
            # Combine all pages with proper spacing
            full_text = '\n\n'.join(text_parts)
            
            # Final cleanup
            full_text = self._clean_text(full_text)
            
            logger.info(f"Extracted {len(full_text)} characters from PDF")
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_fallback_text(self, file: Union[str, BinaryIO, UploadFile]) -> str:
        """
        Fallback text extraction using textract for non-PDF files.
        
        Args:
            file: File path, file-like object, or UploadFile
            
        Returns:
            str: Extracted text
        """
        try:
            if isinstance(file, str):
                # File path - use original textract method
                text = textract.process(file).decode("utf-8", errors="ignore")
            elif isinstance(file, UploadFile):
                # FastAPI UploadFile - save temporarily
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
                    file.file.seek(0)
                    tmp_file.write(file.file.read())
                    tmp_file_path = tmp_file.name
                
                try:
                    text = textract.process(tmp_file_path).decode("utf-8", errors="ignore")
                finally:
                    os.unlink(tmp_file_path)  # Clean up temp file
            else:
                # File-like object - save temporarily
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    if hasattr(file, 'seek'):
                        file.seek(0)
                    tmp_file.write(file.read())
                    tmp_file_path = tmp_file.name
                
                try:
                    text = textract.process(tmp_file_path).decode("utf-8", errors="ignore")
                finally:
                    os.unlink(tmp_file_path)  # Clean up temp file
            
            return self._clean_text(text)
            
        except Exception as e:
            logger.error(f"Fallback text extraction failed: {e}")
            return ""
    
    def extract_text(self, file: Union[str, BinaryIO, UploadFile]) -> str:
        """
        Extract text from various file formats.
        
        Args:
            file (Union[str, BinaryIO, UploadFile]): Path to document file, file-like object, or UploadFile
            
        Returns:
            str: Extracted text content
        """
        if isinstance(file, str):
            # File path
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")
            
            file_ext = Path(file).suffix.lower()
            
            if file_ext not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: {self.supported_formats}")
            elif file_ext == '.txt':
                # Read text content directly
                if hasattr(file, 'read'):
                    content = file.read()
                    if isinstance(content, bytes):
                        content = content.decode('utf-8', errors='ignore')
                    return self._clean_text(content)
                else:
                    # Fallback for file-like objects
                    return self._extract_fallback_text(file)
            elif file_ext in ['.ppt', '.pptx']:
                return self._extract_ppt_text(file)
            elif file_ext in ['.jpg', '.jpeg', '.png']:
                return self._extract_ocr_text(file)
            else:
                # Try fallback extraction
                return self._extract_fallback_text(file)
    
    def process_document(self, file: Union[str, BinaryIO, UploadFile] = None, document_text: str = None):
        """
        Process a legal document completely.
        
        Args:
            file: Path to document file, file-like object, or UploadFile (optional)
            document_text (str): Document text directly (optional)
            
        Returns:
            dict: Complete processing results
        """
        if not file and not document_text:
            raise ValueError("Either file or document_text must be provided")
        
        # Extract text if file provided
        if file:
            if isinstance(file, str):
                text = self.extract_text_from_file(file)
            else:
                # Handle UploadFile or file-like object
                file_ext = Path(file.filename).suffix.lower() if hasattr(file, 'filename') else '.pdf'
                if file_ext == '.pdf':
                    text = self._extract_pdf_text(file)
                else:
                    text = self._extract_fallback_text(file)
        else:
            text = document_text
        
        if not text.strip():
            return {"error": "No text could be extracted from the document"}
        
        # Extract clauses
        clauses_data = extract_clauses(text)
        
        # Flatten clauses for processing
        all_clauses = []
        for category, clause_list in clauses_data.items():
            if isinstance(clause_list, list):
                for clause in clause_list:
                    if isinstance(clause, dict):
                        clause['category'] = category
                        all_clauses.append(clause)
                    else:
                        all_clauses.append({'text': clause, 'category': category})
        
        # Classify clauses
        classified_clauses = classify_multiple_clauses(all_clauses)
        
        # Rank clauses by importance
        ranked_clauses = rank_clauses_by_importance(classified_clauses)
        
        # Extract entities
        entities = extract_entities(text)
        
        return {
            "document_text": text,
            "extracted_clauses": clauses_data,
            "classified_clauses": classified_clauses,
            "ranked_clauses": ranked_clauses,
            "entities": entities,
            "summary": {
                "total_clauses": len(all_clauses),
                "categories": list(clauses_data.keys()),
                "top_clauses": ranked_clauses[:5]
            }
        }
    
    def process_query_on_document(self, file: Union[str, BinaryIO, UploadFile] = None, document_text: str = None, query: str = ""):
        """
        Process a document with a specific query focus.
        
        Args:
            file: Path to document file, file-like object, or UploadFile (optional)
            document_text (str): Document text directly (optional)
            query (str): Query to focus the analysis on
            
        Returns:
            dict: Processing results with query-relevant ranking
        """
        if not file and not document_text:
            raise ValueError("Either file or document_text must be provided")
        
        # Extract text if file provided
        if file:
            if isinstance(file, str):
                text = self.extract_text_from_file(file)
            else:
                # Handle UploadFile or file-like object
                file_ext = Path(file.filename).suffix.lower() if hasattr(file, 'filename') else '.pdf'
                if file_ext == '.pdf':
                    text = self._extract_pdf_text(file)
                else:
                    text = self._extract_fallback_text(file)
        else:
            text = document_text
        
        # Extract clauses
        clauses_data = extract_clauses(text)
        
        # Flatten clauses
        all_clauses = []
        for category, clause_list in clauses_data.items():
            if isinstance(clause_list, list):
                for clause in clause_list:
                    if isinstance(clause, dict):
                        clause['category'] = category
                        all_clauses.append(clause)
                    else:
                        all_clauses.append({'text': clause, 'category': category})
        
        # Classify clauses
        classified_clauses = classify_multiple_clauses(all_clauses)
        
        # Rank clauses by relevance to query
        ranked_clauses = rank_clauses_by_importance(classified_clauses, query)
        
        return {
            "query": query,
            "relevant_clauses": ranked_clauses[:10],
            "total_clauses_found": len(all_clauses),
            "top_relevant": ranked_clauses[:3]
        }


def extract_text(file) -> str:
    """
    Simple text extraction function for document processing pipeline.
    
    Args:
        file: File path, file-like object, or UploadFile
        
    Returns:
        str: Extracted text content
    """
    processor = DocumentProcessor()
    return processor.extract_text(file)
