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
        
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'\n\s*\n', '\n', text)
        
        return text.strip()
    
    def _extract_pdf_text(self, file) -> str:
        """
        Extract text from PDF files using pdfplumber.
        
        Args:
            file: PDF file object
            
        Returns:
            str: Extracted text content
        """
        try:
            if PDFPLUMBER_AVAILABLE:
                import io
                
                # Read file content
                if hasattr(file, 'read'):
                    content = file.read()
                else:
                    with open(file, 'rb') as f:
                        content = f.read()
                
                # Extract text using pdfplumber
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                
                return self._clean_text(text) if text else ""
            else:
                logger.warning("pdfplumber not available - PDF text extraction limited")
                return "PDF file detected. Text extraction not available without pdfplumber."
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            return ""
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from a text file.
        
        Args:
            file_path (str): Path to text file
            
        Returns:
            str: File content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return self._clean_text(f.read())
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return self._clean_text(f.read())
        except Exception as e:
            logger.error(f"Text file extraction failed: {e}")
            return ""
    
    def _extract_fallback_text(self, file) -> str:
        """
        Fallback text extraction method.
        
        Args:
            file: File object
            
        Returns:
            str: Extracted text or error message
        """
        try:
            if hasattr(file, 'read'):
                content = file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='ignore')
                return self._clean_text(content)
            else:
                return "Unable to extract text from file format."
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
            
            if file_ext == '.pdf':
                return self._extract_pdf_text(file)
            elif file_ext == '.txt':
                return self._extract_text_from_file(file)
            elif file_ext in ['.ppt', '.pptx']:
                return self._extract_ppt_text(file)
            elif file_ext in ['.jpg', '.jpeg', '.png']:
                return self._extract_ocr_text(file)
            else:
                # Try fallback extraction
                return self._extract_fallback_text(file)
        else:
            # Handle UploadFile or file-like object
            file_ext = Path(file.filename).suffix.lower() if hasattr(file, 'filename') else '.pdf'
            
            if file_ext == '.pdf':
                return self._extract_pdf_text(file)
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


# Global instance for backward compatibility
document_processor = DocumentProcessor()

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
