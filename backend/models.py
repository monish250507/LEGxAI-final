# Legal entity extraction and NLP models
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

def extract_entities(text: str):
    """
    Extract legal entities from text using spaCy NER.
    
    Args:
        text (str): Text to extract entities from
        
    Returns:
        list: List of entities with text and label
    """
    if nlp is None:
        return []
    doc = nlp(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

class LegalClause:
    """
    Data model for a legal clause.
    """
    def __init__(self, text: str, clause_type: str = "", section: str = "", importance: float = 0.0):
        self.text = text
        self.clause_type = clause_type
        self.section = section
        self.importance = importance
        self.entities = []
        
    def add_entities(self, entities: list):
        """Add extracted entities to the clause."""
        self.entities = entities
        
    def to_dict(self):
        """Convert clause to dictionary representation."""
        return {
            "text": self.text,
            "type": self.clause_type,
            "section": self.section,
            "importance": self.importance,
            "entities": self.entities
        }

class LegalDocument:
    """
    Data model for a legal document containing multiple clauses.
    """
    def __init__(self, title: str = "", content: str = ""):
        self.title = title
        self.content = content
        self.clauses = []
        self.entities = []
        self.metadata = {}
        
    def add_clause(self, clause: LegalClause):
        """Add a clause to the document."""
        self.clauses.append(clause)
        
    def add_entities(self, entities: list):
        """Add extracted entities to the document."""
        self.entities = entities
        
    def set_metadata(self, metadata: dict):
        """Set document metadata."""
        self.metadata = metadata
        
    def get_clauses_by_type(self, clause_type: str):
        """Get all clauses of a specific type."""
        return [clause for clause in self.clauses if clause.clause_type == clause_type]
        
    def get_top_clauses(self, n: int = 5):
        """Get top N most important clauses."""
        return sorted(self.clauses, key=lambda x: x.importance, reverse=True)[:n]
        
    def to_dict(self):
        """Convert document to dictionary representation."""
        return {
            "title": self.title,
            "content": self.content,
            "clauses": [clause.to_dict() for clause in self.clauses],
            "entities": self.entities,
            "metadata": self.metadata,
            "summary": {
                "total_clauses": len(self.clauses),
                "clause_types": list(set(clause.clause_type for clause in self.clauses))
            }
        }
