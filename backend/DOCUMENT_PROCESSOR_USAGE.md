# Document Processor Usage Guide

## Overview

The `document_processor.py` module provides production-ready PDF text extraction and document processing capabilities using `pdfplumber`.

## Key Features

- **PDF Text Extraction**: High-quality text extraction using pdfplumber
- **Text Cleaning**: Automatic cleanup of PDF artifacts and formatting issues
- **Multiple Input Types**: Supports file paths, file-like objects, and FastAPI UploadFile
- **Error Handling**: Comprehensive error handling and logging
- **Production Ready**: Robust implementation with proper resource management

## Usage

### Simple PDF Text Extraction

```python
from document_processor import process_document

# Extract text from PDF file path
text = process_document("path/to/document.pdf")
print(text)

# Extract text from file-like object
with open("document.pdf", "rb") as f:
    text = process_document(f)
    print(text)
```

### FastAPI Integration

```python
from fastapi import FastAPI, UploadFile, File
from document_processor import process_document

app = FastAPI()

@app.post("/extract-text")
async def extract_pdf_text(file: UploadFile = File(...)):
    try:
        text = process_document(file)
        return {"text": text, "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}
```

### Full Document Processing

```python
from document_processor import DocumentProcessor

processor = DocumentProcessor()

# Process with file path
result = processor.process_document("document.pdf")

# Process with UploadFile
result = processor.process_document(upload_file)

# Process with direct text
result = processor.process_document(document_text="Legal text here...")

# Result includes:
# - document_text: Cleaned text
# - extracted_clauses: AI-extracted clauses
# - classified_clauses: Classified by type
# - ranked_clauses: Ranked by importance
# - entities: Named entities
# - summary: Processing summary
```

## Text Cleaning Features

The processor automatically cleans extracted text by:

- Removing excessive whitespace
- Eliminating PDF artifacts (form feeds, control characters)
- Fixing common OCR issues
- Normalizing quotes and dashes
- Removing non-printable characters

## Error Handling

The processor provides detailed error messages:

```python
try:
    text = process_document("document.pdf")
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Processing error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Supported Formats

- **PDF**: Primary format using pdfplumber
- **TXT**: Text files
- **DOCX/DOC**: Using textract fallback

## Logging

The processor uses Python logging for debugging:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Will log processing information
text = process_document("document.pdf")
```

## Performance Considerations

- PDF processing is memory-efficient for large files
- Temporary files are automatically cleaned up
- File pointers are properly managed
- Page-by-page processing with error recovery

## Dependencies

- `pdfplumber`: PDF text extraction
- `fastapi`: For UploadFile support (optional)
- `pathlib`: File path handling
- `io`: File stream management

## Installation

```bash
pip install pdfplumber fastapi python-multipart
```

## Testing

Run the basic structure test:

```bash
python test_basic_structure.py
```

Run the full test suite (requires all dependencies):

```bash
python test_document_processor.py
```
