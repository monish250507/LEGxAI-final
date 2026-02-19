# Upload Endpoint Integration Guide

## Overview

The `/api/upload` endpoint has been enhanced to provide complete clause analysis pipeline for legal documents. It processes PDF files through a 5-step pipeline and returns structured JSON with comprehensive clause information.

## Pipeline Architecture

```
PDF File Upload → Document Processing → Clause Extraction → Clause Classification → Clause Ranking → Structured JSON Response
```

## Endpoint Details

### URL
```
POST /api/upload
```

### Request
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: PDF file upload

### Response Structure
```json
{
  "status": "success",
  "filename": "document.pdf",
  "file_path": "/path/to/uploaded/file.pdf",
  "document_stats": {
    "total_characters": 1250,
    "total_clauses": 8,
    "classified_clauses": 8,
    "ranked_clauses": 8
  },
  "clauses": [
    {
      "clause_id": "clause_001",
      "text": "Either party may terminate this agreement with 30 days written notice.",
      "type": "termination",
      "priority_score": 0.9,
      "color": "red"
    }
  ],
  "summary": {
    "high_priority_count": 3,
    "medium_priority_count": 3,
    "low_priority_count": 2,
    "clause_types": ["termination", "payment", "liability", "general"]
  }
}
```

## Processing Steps

### Step 1: Document Processing
- **Input**: PDF file (UploadFile object)
- **Process**: Extract text using pdfplumber
- **Output**: Cleaned document text
- **Features**: PDF artifact removal, text normalization

### Step 2: Clause Extraction
- **Input**: Document text
- **Process**: Pattern-based clause identification
- **Output**: List of clauses with IDs
- **Features**: Multiple extraction strategies (numbered, lettered, paragraph, section)

### Step 3: Clause Classification
- **Input**: Extracted clauses
- **Process**: Keyword-based type assignment
- **Output**: Clauses with type and confidence
- **Types**: termination, liability, payment, jurisdiction, confidentiality, indemnity, general

### Step 4: Clause Ranking
- **Input**: Classified clauses
- **Process**: Priority-based importance scoring
- **Output**: Ranked clauses with scores and colors
- **Features**: Type priority scores, color coding, relevance scoring

### Step 5: Structured Response
- **Input**: Ranked clauses
- **Process**: JSON response formatting
- **Output**: Complete analysis results
- **Features**: Statistics, summaries, structured clause data

## Clause Fields

### clause_id
- **Format**: `clause_XXX` (3-digit zero-padded)
- **Purpose**: Unique identifier for each clause
- **Example**: `clause_001`, `clause_002`

### text
- **Content**: Full clause text
- **Format**: Cleaned, normalized text
- **Purpose**: Clause content for display and analysis

### type
- **Values**: termination, liability, payment, jurisdiction, confidentiality, indemnity, general
- **Purpose**: Clause categorization
- **Confidence**: Classification confidence score (0-1)

### priority_score
- **Range**: 0.0 - 1.0
- **Type Scores**:
  - termination: 0.9
  - liability: 0.85
  - indemnity: 0.8
  - jurisdiction: 0.75
  - payment: 0.6
  - general: 0.3

### color
- **Red** (> 0.75): High priority clauses
- **Yellow** (> 0.45): Medium priority clauses  
- **Green** (≤ 0.45): Low priority clauses

## Usage Examples

### cURL Example
```bash
curl -X POST \
  -F "file=@contract.pdf" \
  http://localhost:8000/api/upload
```

### Python Example
```python
import requests

# Upload and analyze document
with open('contract.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/upload', files=files)
    result = response.json()

# Process results
if result['status'] == 'success':
    clauses = result['clauses']
    for clause in clauses:
        print(f"{clause['clause_id']}: {clause['type']} ({clause['color']})")
        print(f"  {clause['text'][:80]}...")
```

### JavaScript Example
```javascript
// Upload file and analyze clauses
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/api/upload', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.status === 'success') {
        console.log(`Processed ${data.document_stats.total_clauses} clauses`);
        
        // Display high priority clauses
        const highPriorityClauses = data.clauses.filter(c => c.color === 'red');
        console.log(`High priority clauses: ${highPriorityClauses.length}`);
        
        // Display clause types
        console.log('Clause types:', data.summary.clause_types);
    }
});
```

## Response Processing

### Filtering by Priority
```javascript
// Filter clauses by priority level
const redClauses = clauses.filter(c => c.color === 'red');
const yellowClauses = clauses.filter(c => c.color === 'yellow');
const greenClauses = clauses.filter(c => c.color === 'green');
```

### Filtering by Type
```javascript
// Filter clauses by type
const terminationClauses = clauses.filter(c => c.type === 'termination');
const paymentClauses = clauses.filter(c => c.type === 'payment');
const liabilityClauses = clauses.filter(c => c.type === 'liability');
```

### Sorting Options
```javascript
// Sort by priority score (descending)
const sortedByPriority = [...clauses].sort((a, b) => b.priority_score - a.priority_score);

// Sort by rank
const sortedByRank = [...clauses].sort((a, b) => a.rank - b.rank);
```

## Error Handling

### Common Error Responses
```json
{
  "detail": "No file selected"
}
```

```json
{
  "detail": "File type not allowed"
}
```

```json
{
  "detail": "No text could be extracted from document"
}
```

```json
{
  "detail": "No clauses could be extracted from document"
}
```

### Error Status Codes
- **400**: Bad Request (missing file, wrong type, no text/clauses)
- **500**: Internal Server Error (processing failure)

## Performance Considerations

### Processing Time
- **Small PDF** (< 5 pages): ~2-5 seconds
- **Medium PDF** (5-20 pages): ~5-15 seconds
- **Large PDF** (> 20 pages): ~15-60 seconds

### Memory Usage
- **Clause Extraction**: Low memory usage
- **Text Classification**: Moderate memory usage
- **Clause Ranking**: Higher memory usage due to embeddings
- **Total**: Scales with document size

### Optimization Tips
- **File Size**: Limit uploads to 50MB for optimal performance
- **Concurrent Requests**: Limit to 5 concurrent uploads
- **Caching**: Cache results for repeated document analysis
- **Timeout**: Set 60-second timeout for large documents

## Integration Examples

### Frontend Integration
```javascript
// React component for clause display
function ClauseList({ clauses }) {
  return (
    <div>
      {clauses.map(clause => (
        <div key={clause.clause_id} className={`clause ${clause.color}`}>
          <h4>{clause.type} (Priority: {clause.priority_score})</h4>
          <p>{clause.text}</p>
        </div>
      ))}
    </div>
  );
}
```

### Mobile App Integration
```javascript
// Flutter/Dart example for mobile upload
Future<Map<String, dynamic>> uploadAndAnalyzeDocument(File file) async {
  var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/api/upload'));
  request.files.add(await http.MultipartFile.fromPath('file', file.path));
  
  var response = await request.send();
  var data = jsonDecode(response.body);
  
  if (data['status'] == 'success') {
    return data['clauses'];
  } else {
    throw Exception(data['detail']);
  }
}
```

## Testing

### Test Files
- **Sample Contract**: Multi-page legal agreement
- **Simple Document**: Single page with basic clauses
- **Complex Document**: Multiple clause types and nested structures
- **Edge Cases**: Poor quality PDF, scanned documents

### Test Script
```bash
# Run integration tests
python test_integration_mock.py

# Expected output
✓ All integration tests passed!
✓ Full clause analysis pipeline logic is working correctly.
```

## Monitoring and Logging

### Log Levels
- **INFO**: Processing steps and statistics
- **WARNING**: Non-critical processing issues
- **ERROR**: Processing failures and exceptions

### Key Metrics
- **Processing Time**: Time per document
- **Clause Count**: Average clauses per document
- **Type Distribution**: Most common clause types
- **Error Rate**: Failed processing percentage

### Health Check
```bash
# Check if upload endpoint is working
curl -X GET http://localhost:8000/api/health
```

## Security Considerations

### File Validation
- **File Types**: Only PDF, TXT, DOCX, JSON allowed
- **File Size**: Maximum 50MB limit
- **Filename Sanitization**: Remove special characters
- **Virus Scanning**: Implement for production

### Rate Limiting
- **Requests**: 10 uploads per minute per IP
- **File Size**: 100MB per minute per IP
- **Concurrent**: 5 simultaneous uploads per IP

## Troubleshooting

### Common Issues
1. **"No text extracted"**: Check PDF quality and format
2. **"No clauses found"**: Verify document contains clause patterns
3. **"Classification failed"**: Check clause extractor output
4. **"Ranking failed"**: Verify classifier output format
5. **Timeout**: Increase timeout or reduce file size limit

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check intermediate results
from clause_extractor import extract_clauses
clauses = extract_clauses(text)
print(f"Extracted {len(clauses)} clauses")
```

This integrated upload endpoint provides a complete, production-ready solution for legal document analysis with comprehensive clause extraction, classification, and ranking capabilities.
