# Clause Extractor Usage Guide

## Overview

The `clause_extractor.py` module provides robust clause extraction from legal documents using multiple pattern-based strategies and intelligent filtering.

## Key Features

- **Multiple Extraction Strategies**: Numbered, lettered, paragraph, and section-based detection
- **Intelligent Text Cleaning**: Removes artifacts and normalizes text
- **Legal Keyword Detection**: Identifies likely legal clauses using keyword analysis
- **Robust Validation**: Filters and validates extracted clauses
- **Automatic ID Generation**: Generates unique clause IDs
- **Duplicate Removal**: Eliminates duplicate clauses while preserving order

## Usage

### Basic Clause Extraction

```python
from clause_extractor import extract_clauses

# Extract clauses from document text
document_text = """
1. The parties shall maintain confidentiality of all proprietary information.
2. This agreement shall be governed by the laws of California.
3. Either party may terminate this contract with 30 days written notice.

The client agrees to pay all fees within 15 days of invoice.
The service provider will deliver all work according to the specifications.
"""

clauses = extract_clauses(document_text)

# Process results
for clause in clauses:
    print(f"{clause['clause_id']}: {clause['text']}")
```

**Output:**
```
clause_001: The parties shall maintain confidentiality of all proprietary information.
clause_002: This agreement shall be governed by the laws of California.
clause_003: Either party may terminate this contract with 30 days written notice.
clause_004: The client agrees to pay all fees within 15 days of invoice.
clause_005: The service provider will deliver all work according to the specifications.
```

### Return Format

Each clause is returned as a dictionary with:

```python
{
    "clause_id": "clause_001",  # Unique identifier
    "text": "The clause text",   # Extracted clause content
    "type": "numbered",         # Detection method (optional)
    # ... other metadata fields
}
```

## Extraction Strategies

### 1. Numbered Clauses
Detects clauses numbered as:
- `1. First clause`
- `2. Second clause`
- `(1) Parenthesized clause`
- `(2) Another parenthesized clause`

### 2. Lettered Clauses
Detects clauses lettered as:
- `a. First item`
- `b. Second item`
- `A. Capital letter item`

### 3. Paragraph Clauses
Analyzes paragraphs and identifies those likely to be legal clauses based on:
- Legal keywords (shall, must, agree, etc.)
- Sentence structure
- Minimum length requirements

### 4. Section Clauses
Detects formal section markers:
- `Section 1.1: Contract Formation`
- `Article 2: Obligations`
- `Clause 3: Termination`

## Text Cleaning Features

The extractor automatically cleans text by:

- Removing excessive whitespace
- Eliminating page numbers and headers
- Preserving paragraph breaks
- Normalizing formatting
- Removing PDF artifacts

## Legal Keywords

The system uses legal keywords to identify likely clauses:

**Obligation Keywords**: shall, must, will, agree, obligation, liable, responsible
**Prohibition Keywords**: prohibited, forbidden, restricted, required, mandatory
**Right Keywords**: entitled, right, permission, authorized, permitted
**Temporal Keywords**: terminate, expiration, duration, period, term
**Party Keywords**: party, parties, agreement, contract, legal, law

## Validation and Filtering

### Minimum Requirements
- **Length**: At least 10 characters
- **Content**: Contains legal keywords or proper sentence structure
- **Quality**: Passes clause likelihood scoring

### Long Clause Handling
Clauses over 2000 characters are automatically split into smaller, more manageable chunks while preserving context.

### Duplicate Removal
Identical clauses are removed while preserving the original order of appearance.

## Advanced Usage

### AI-Enhanced Extraction

For enhanced accuracy, you can use AI-based extraction:

```python
from clause_extractor import extract_clauses_with_ai

# Get AI-categorized clauses
ai_result = extract_clauses_with_ai(document_text)

# Returns categorized clauses
# {
#     "obligations": [...],
#     "rights": [...],
#     "prohibitions": [...],
#     "dates": [...],
#     "parties": [...]
# }
```

### Custom Processing

```python
from clause_extractor import _clean_document_text, _extract_clauses_by_patterns

# Clean text manually
cleaned_text = _clean_document_text(raw_text)

# Extract raw clauses
raw_clauses = _extract_clauses_by_patterns(cleaned_text)
```

## Error Handling

```python
from clause_extractor import extract_clauses

try:
    clauses = extract_clauses(document_text)
    print(f"Extracted {len(clauses)} clauses")
except Exception as e:
    print(f"Extraction failed: {e}")
```

## Performance Considerations

- **Memory Efficient**: Processes large documents in chunks
- **Regex Optimized**: Uses compiled regex patterns for performance
- **Early Filtering**: Applies quick filters before expensive operations
- **Duplicate Detection**: Efficient hash-based duplicate removal

## Testing

Run the pattern tests:

```bash
python test_clause_patterns.py
```

Run the full test suite (requires all dependencies):

```bash
python test_clause_extractor.py
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from clause_extractor import extract_clauses
from pydantic import BaseModel

class DocumentRequest(BaseModel):
    text: str

app = FastAPI()

@app.post("/extract-clauses")
def extract_document_clauses(request: DocumentRequest):
    try:
        clauses = extract_clauses(request.text)
        return {"clauses": clauses, "count": len(clauses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Document Processor Integration

```python
from document_processor import DocumentProcessor
from clause_extractor import extract_clauses

# Extract text first
processor = DocumentProcessor()
text = processor.extract_text_from_file("document.pdf")

# Then extract clauses
clauses = extract_clauses(text)
```

## Configuration

The extractor uses sensible defaults, but you can modify behavior by:

1. **Adjusting keyword lists** in `_is_likely_clause()`
2. **Modifying regex patterns** in extraction functions
3. **Changing validation criteria** in `_filter_valid_clauses()`
4. **Tuning length thresholds** for different document types

## Best Practices

1. **Preprocess documents**: Use clean, machine-readable text when possible
2. **Validate input**: Ensure text is not empty or malformed
3. **Handle edge cases**: Account for different document formats
4. **Monitor performance**: Large documents may require additional processing time
5. **Review results**: Always validate extracted clauses for your specific use case
