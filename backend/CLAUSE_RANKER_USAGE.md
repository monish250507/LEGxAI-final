# Clause Ranker Usage Guide

## Overview

The `clause_ranker.py` module provides intelligent ranking of legal clauses based on type priority and optional query relevance, with color coding for visual prioritization.

## Priority Scoring System

The ranker assigns priority scores based on clause type importance:

| Clause Type | Priority Score | Color | Description |
|-------------|----------------|--------|-------------|
| termination | 0.9 | 🔴 Red | Contract ending, cancellation clauses |
| liability | 0.85 | 🔴 Red | Legal responsibility, fault clauses |
| indemnity | 0.8 | 🔴 Red | Hold harmless, compensation clauses |
| jurisdiction | 0.75 | 🟡 Yellow | Governing law, court clauses |
| payment | 0.6 | 🟡 Yellow | Financial obligations, fee clauses |
| general | 0.3 | 🟢 Green | Miscellaneous or general terms |

### Color Coding Rules

- **Red (score > 0.75)**: High priority clauses requiring immediate attention
- **Yellow (score > 0.45)**: Medium priority clauses important for review
- **Green (score ≤ 0.45)**: Low priority clauses for general reference

## Usage

### Basic Clause Ranking

```python
from clause_ranker import rank_clauses_by_importance

# Example clauses with types
clauses = [
    {"clause_id": "clause_001", "text": "Either party may terminate this agreement.", "type": "termination"},
    {"clause_id": "clause_002", "text": "Payment shall be made within 30 days.", "type": "payment"},
    {"clause_id": "clause_003", "text": "The contractor shall indemnify the client.", "type": "indemnity"},
    {"clause_id": "clause_004", "text": "General terms and conditions apply.", "type": "general"}
]

# Rank clauses by importance
ranked_clauses = rank_clauses_by_importance(clauses)

# Display results
for clause in ranked_clauses:
    print(f"Rank {clause['rank']}: {clause['type']} ({clause['color']}) - Score: {clause['priority_score']}")
    print(f"  Text: {clause['text'][:60]}...")
```

**Output:**
```
Rank 1: termination (red) - Score: 0.9
  Text: Either party may terminate this agreement...
Rank 2: indemnity (red) - Score: 0.8
  Text: The contractor shall indemnify the client...
Rank 3: payment (yellow) - Score: 0.6
  Text: Payment shall be made within 30 days...
Rank 4: general (green) - Score: 0.3
  Text: General terms and conditions apply...
```

### Query-Based Ranking

```python
from clause_ranker import rank_clauses_by_importance

# Rank clauses with query relevance
query = "payment obligations"
ranked_clauses = rank_clauses_by_importance(clauses, query=query)

for clause in ranked_clauses:
    print(f"{clause['type']}: Priority {clause['priority_score']}, Relevance {clause['relevance_score']}")
```

### Get Top Clauses

```python
from clause_ranker import get_top_clauses

# Get top 3 most important clauses
top_clauses = get_top_clauses(clauses, top_n=3)

print(f"Top {len(top_clauses)} clauses:")
for i, clause in enumerate(top_clauses, 1):
    print(f"{i}. {clause['type']} ({clause['color']}) - {clause['text'][:50]}...")
```

### Priority-Only Ranking

```python
from clause_ranker import rank_clauses_by_type_priority

# Rank only by type priority (no query relevance)
ranked = rank_clauses_by_type_priority(clauses)

for clause in ranked:
    print(f"{clause['type']}: {clause['priority_score']} ({clause['color']})")
```

## Return Format

Each ranked clause includes:

```python
{
    "clause_id": "clause_001",           # Original clause identifier
    "text": "Either party may terminate...", # Clause text content
    "type": "termination",               # Clause type from classifier
    "priority_score": 0.9,              # Type-based priority score
    "relevance_score": 0.75,           # Query relevance score (0-1)
    "combined_score": 0.88,             # Combined ranking score
    "color": "red",                     # Visual priority color
    "rank": 1                           # Final rank (1 = highest)
}
```

## Advanced Features

### Statistics and Analysis

```python
from clause_ranker import get_clause_priority_statistics

# Get distribution statistics
stats = get_clause_priority_statistics(ranked_clauses)

print(f"Total clauses: {stats['total_clauses']}")
print(f"Highest priority: {stats['highest_priority']}")

# Priority distribution
dist = stats['priority_distribution']
print(f"Red clauses: {dist['counts']['red']} ({dist['percentages']['red']}%)")
print(f"Yellow clauses: {dist['counts']['yellow']} ({dist['percentages']['yellow']}%)")
print(f"Green clauses: {dist['counts']['green']} ({dist['percentages']['green']}%)")

# Type distribution
for type_name, count in stats['type_distribution'].items():
    print(f"{type_name}: {count} clauses")
```

### AI-Enhanced Ranking

```python
from clause_ranker import rank_clauses_with_ai

# Use AI for enhanced importance assessment
ai_ranked = rank_clauses_with_ai(clauses, query="critical deadlines")

for clause in ai_ranked:
    print(f"AI Score: {clause['importance_score']} ({clause['ranking_method']})")
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from clause_ranker import rank_clauses_by_importance
from pydantic import BaseModel

class RankingRequest(BaseModel):
    clauses: List[dict]
    query: str = ""

app = FastAPI()

@app.post("/rank-clauses")
def rank_clauses_endpoint(request: RankingRequest):
    try:
        ranked = rank_clauses_by_importance(request.clauses, request.query)
        return {"ranked_clauses": ranked, "total": len(ranked)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Complete Document Processing Pipeline

```python
from clause_extractor import extract_clauses
from clause_classifier import classify_multiple_clauses
from clause_ranker import rank_clauses_by_importance

# Complete processing pipeline
document_text = "Legal document text..."

# 1. Extract clauses
extracted = extract_clauses(document_text)

# 2. Classify clauses
classified = classify_multiple_clauses(extracted)

# 3. Rank clauses
ranked = rank_clauses_by_importance(classified)

# 4. Get statistics
stats = get_clause_priority_statistics(ranked)

print(f"Processed {len(extracted)} clauses")
print(f"Priority distribution: {stats['priority_distribution']}")
```

### Frontend Integration

```javascript
// Example JavaScript integration
function displayRankedClauses(clauses) {
    const redClauses = clauses.filter(c => c.color === 'red');
    const yellowClauses = clauses.filter(c => c.color === 'yellow');
    const greenClauses = clauses.filter(c => c.color === 'green');
    
    return {
        highPriority: redClauses,
        mediumPriority: yellowClauses,
        lowPriority: greenClauses,
        all: clauses
    };
}
```

## Performance Considerations

### Ranking Algorithm

1. **Priority Score (70%)**: Type-based importance from predefined scores
2. **Relevance Score (30%)**: Query-based semantic similarity
3. **Combined Score**: Weighted combination for final ranking
4. **Color Assignment**: Visual coding based on priority thresholds

### Optimization Tips

- **Batch Processing**: Rank multiple clauses at once for efficiency
- **Query Caching**: Cache query embeddings for repeated queries
- **Priority Filtering**: Filter by minimum priority score for large documents
- **Color Pre-filtering**: Use color coding for quick visual scanning

## Customization

### Adjusting Priority Scores

```python
# Modify CLAUSE_PRIORITY_SCORES in clause_ranker.py
CLAUSE_PRIORITY_SCORES = {
    'termination': 0.95,  # Increase termination importance
    'payment': 0.7,       # Increase payment importance
    'custom_type': 0.5     # Add custom clause type
}
```

### Custom Color Thresholds

```python
# Modify get_priority_color function
def get_priority_color(priority_score: float) -> str:
    if priority_score > 0.8:      # Higher threshold for red
        return 'red'
    elif priority_score > 0.4:    # Lower threshold for yellow
        return 'yellow'
    else:
        return 'green'
```

### Adding New Clause Types

```python
# Extend the priority scores dictionary
CLAUSE_PRIORITY_SCORES['intellectual_property'] = 0.65

# Add corresponding color logic if needed
```

## Testing

Run the ranking tests:

```bash
python test_clause_ranker.py
```

## Best Practices

1. **Consistent Input**: Ensure clauses have 'type' field from classifier
2. **Query Optimization**: Use specific, relevant queries for better ranking
3. **Color Utilization**: Leverage color coding for quick visual assessment
4. **Score Thresholds**: Apply minimum score filters for large documents
5. **Performance Monitoring**: Track ranking accuracy and user feedback
6. **Domain Customization**: Adjust priority scores for specific legal areas

## Troubleshooting

### Low Ranking Quality
- Verify clause types are correctly classified
- Adjust priority scores for your domain
- Use AI-enhanced ranking for complex cases

### Performance Issues
- Reduce embedding dimensionality for large documents
- Implement caching for repeated queries
- Use priority-only ranking for faster processing

### Color Coding Issues
- Check priority score thresholds
- Verify color assignment logic
- Ensure consistent color mapping across frontend

## Use Cases

### Contract Review
- **Red clauses**: Critical terms requiring legal review
- **Yellow clauses**: Important business terms
- **Green clauses**: Standard boilerplate language

### Risk Assessment
- **High priority**: Liability, termination, indemnity clauses
- **Medium priority**: Payment, jurisdiction clauses
- **Low priority**: General terms and definitions

### Document Summarization
- Focus on red and yellow clauses for executive summary
- Use green clauses for detailed reference
- Provide priority-based filtering options
