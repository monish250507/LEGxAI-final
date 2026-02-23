# Clause Classifier Usage Guide

## Overview

The `clause_classifier.py` module provides keyword-based classification of legal clauses into specific categories with confidence scoring.

## Supported Clause Types

The classifier detects the following clause types:

- **termination**: Contract ending, cancellation, expiration clauses
- **liability**: Legal responsibility, fault, damage clauses
- **payment**: Financial obligations, fees, invoicing clauses
- **jurisdiction**: Governing law, court, arbitration clauses
- **confidentiality**: Information protection, non-disclosure clauses
- **indemnity**: Hold harmless, reimbursement, compensation clauses
- **general**: Miscellaneous or general agreement terms

## Usage

### Single Clause Classification

```python
from clause_classifier import classify_clause_type

# Classify a single clause
clause_text = "Either party may terminate this agreement with 30 days written notice."
result = classify_clause_type(clause_text)

print(f"Type: {result['type']}")
print(f"Confidence: {result['confidence']}")
print(f"Method: {result['method']}")

# Output:
# Type: termination
# Confidence: 0.856
# Method: keyword_based
```

### Multiple Clause Classification

```python
from clause_classifier import classify_multiple_clauses

# Classify multiple clauses at once
clauses = [
    "The client shall pay all fees within 15 days.",
    "Both parties shall maintain confidentiality.",
    "This agreement is governed by California law.",
    "The contractor shall indemnify the client."
]

results = classify_multiple_clauses(clauses)

for result in results:
    print(f"{result['type']}: {result['text'][:50]}...")
```

**Output:**
```
payment: The client shall pay all fees within 15 days...
confidentiality: Both parties shall maintain confidentiality...
jurisdiction: This agreement is governed by California law...
indemnity: The contractor shall indemnify the client...
```

### Classification with Existing Clause Objects

```python
# Works with clause objects that have additional fields
clauses_with_metadata = [
    {
        "clause_id": "clause_001",
        "text": "Payment shall be made within 30 days.",
        "section": "Section 4"
    },
    {
        "clause_id": "clause_002", 
        "text": "This agreement terminates on December 31, 2024.",
        "section": "Section 7"
    }
]

results = classify_multiple_clauses(clauses_with_metadata)

# Results preserve original fields and add classification
for result in results:
    print(f"{result['clause_id']}: {result['type']} (confidence: {result['confidence']})")
```

## Return Format

Each classification result includes:

```python
{
    "type": "payment",                    # Detected clause type
    "confidence": 0.847,                 # Confidence score (0-1)
    "method": "keyword_based",             # Classification method used
    "scores": {                           # All type scores (debug info)
        "payment": 2.8,
        "general": 1.0,
        "termination": 0.0,
        # ... other types
    }
}
```

## Classification Algorithm

### Keyword-Based Detection

The classifier uses comprehensive keyword lists for each clause type:

**Termination Keywords:**
- terminate, termination, end, expire, expiration
- cancel, cancellation, dissolve, dissolution
- notice period, effective date, term, duration

**Payment Keywords:**
- pay, payment, fee, cost, price, invoice
- compensation, remuneration, due, overdue, late
- penalty, interest, currency

**Liability Keywords:**
- liable, liability, responsible, responsibility
- breach, violation, negligence, fault, damage
- loss, compensation, reimbursement

**Jurisdiction Keywords:**
- jurisdiction, govern, law, legal, court
- arbitration, dispute, litigation, forum
- venue, state, federal, applicable law

**Confidentiality Keywords:**
- confidential, confidentiality, secret, proprietary
- trade secret, non-disclosure, disclose, reveal
- protect, information, data, sensitive

**Indemnity Keywords:**
- indemnif, indemnity, hold harmless, defend
- reimburse, compensate, cover, bear costs
- damages, claims, lawsuits, legal action

### Scoring System

1. **Keyword Matching**: Each keyword occurrence adds points based on type weight
2. **Pattern Matching**: Regex patterns add 1.5x weight for better matches
3. **Confidence Calculation**: Normalized to 0-1 range
4. **Minimum Thresholds**: Applied to ensure minimum confidence levels

### Type Weights

- **indemnity**: 3.8 (highest specificity)
- **confidentiality**: 3.5
- **jurisdiction**: 3.2
- **termination**: 3.0
- **payment**: 2.8
- **liability**: 2.5
- **general**: 1.0 (lowest specificity)

## Advanced Features

### Statistics and Analysis

```python
from clause_classifier import get_clause_type_statistics

# Get distribution statistics
clauses = [
    {"type": "payment", "confidence": 0.8},
    {"type": "termination", "confidence": 0.9},
    {"type": "payment", "confidence": 0.7}
]

stats = get_clause_type_statistics(clauses)

print(f"Total clauses: {stats['total_clauses']}")
print(f"Most common type: {stats['most_common']}")

for type_name, type_stats in stats['type_distribution'].items():
    print(f"{type_name}: {type_stats['count']} ({type_stats['percentage']}%)")
```

### AI-Enhanced Classification

For improved accuracy, use AI-based classification:

```python
from clause_classifier import classify_clause_with_ai

result = classify_clause_with_ai("Complex legal clause text...")
# Falls back to keyword-based if AI fails
```

## Error Handling

```python
from clause_classifier import classify_clause_type

try:
    result = classify_clause_type(clause_text)
    if result['confidence'] > 0.5:
        print(f"High confidence classification: {result['type']}")
    else:
        print(f"Low confidence classification: {result['type']}")
except Exception as e:
    print(f"Classification failed: {e}")
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from clause_classifier import classify_multiple_clauses
from pydantic import BaseModel

class ClassificationRequest(BaseModel):
    clauses: List[str]

app = FastAPI()

@app.post("/classify-clauses")
def classify_document_clauses(request: ClassificationRequest):
    try:
        results = classify_multiple_clauses(request.clauses)
        return {"classifications": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Document Processor Integration

```python
from clause_extractor import extract_clauses
from clause_classifier import classify_multiple_clauses

# Extract then classify
document_text = "Legal document text..."
extracted_clauses = extract_clauses(document_text)
classified_clauses = classify_multiple_clauses(extracted_clauses)

# Now each clause has type field
for clause in classified_clauses:
    print(f"{clause['clause_id']}: {clause['type']}")
```

## Performance Considerations

- **Speed**: Keyword-based classification is very fast (~1ms per clause)
- **Memory**: Low memory usage with efficient regex patterns
- **Accuracy**: High accuracy for common legal clause patterns
- **Scalability**: Handles thousands of clauses efficiently

## Customization

### Adding New Clause Types

```python
# Extend CLAUSE_TYPES in clause_classifier.py
CLAUSE_TYPES['intellectual_property'] = {
    'keywords': ['intellectual property', 'IP', 'copyright', 'patent', 'trademark'],
    'patterns': [r'\bintellectual\s+property\b', r'\bIP\b'],
    'weight': 3.0
}
```

### Adjusting Weights

```python
# Modify type weights for your domain
CLAUSE_TYPES['payment']['weight'] = 3.5  # Increase payment detection sensitivity
```

### Custom Patterns

```python
# Add domain-specific patterns
CLAUSE_TYPES['jurisdiction']['patterns'].extend([
    r'\bEU\s+law\b',
    r'\binternational\s+court\b'
])
```

## Testing

Run the classification tests:

```bash
python test_clause_classifier.py
```

## Best Practices

1. **Preprocess Text**: Clean and normalize text before classification
2. **Handle Edge Cases**: Account for empty or malformed input
3. **Use Confidence Thresholds**: Filter low-confidence classifications
4. **Combine Methods**: Use keyword-based as primary, AI as fallback
5. **Monitor Performance**: Track classification accuracy for your domain
6. **Customize for Domain**: Adjust keywords and weights for specific legal areas

## Troubleshooting

### Low Confidence Scores
- Check if clause text is too short or generic
- Verify relevant keywords are present
- Consider customizing keyword lists for your domain

### Misclassifications
- Review the scoring system and weights
- Add domain-specific keywords
- Use AI-enhanced classification for complex cases

### Performance Issues
- Pre-compile regex patterns if processing large volumes
- Consider batch processing for multiple clauses
- Cache results for repeated classifications
