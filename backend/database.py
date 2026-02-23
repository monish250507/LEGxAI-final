import os
import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from tqdm import tqdm
from config import KB_DIR, DB_DIR, KB_SQLITE, FAISS_INDEX, ID_MAP

# Try to import optional dependencies
try:
    from services.embeddings import encode_texts, save_faiss_index, save_id_map
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logging.warning("Embeddings not available - some database features will be limited")

try:
    import numpy as np
except ImportError:
    np = None
    logging.warning("NumPy not available - some database features will be limited")

class LegalDatabase:
    """
    Database handler for legal documents and clauses.
    """
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or KB_SQLITE
        self.conn = None
        self._ensure_db_exists()
        
    def _ensure_db_exists(self):
        """Ensure database and directories exist."""
        os.makedirs(DB_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            self._create_database()
    
    def _create_database(self):
        """Create the database schema."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE clauses (
                id INTEGER PRIMARY KEY,
                country TEXT,
                section_path TEXT,
                text TEXT,
                metadata TEXT,
                clause_type TEXT,
                importance_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT,
                file_path TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE document_clauses (
                id INTEGER PRIMARY KEY,
                document_id INTEGER,
                clause_id INTEGER,
                FOREIGN KEY (document_id) REFERENCES documents (id),
                FOREIGN KEY (clause_id) REFERENCES clauses (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def connect(self):
        """Establish database connection."""
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def insert_document(self, title: str, content: str, file_path: str = "", metadata: dict = None):
        """Insert a new document into the database."""
        conn = self.connect()
        cur = conn.cursor()
        
        metadata_json = json.dumps(metadata or {})
        cur.execute("""
            INSERT INTO documents (title, content, file_path, metadata)
            VALUES (?, ?, ?, ?)
        """, (title, content, file_path, metadata_json))
        
        doc_id = cur.lastrowid
        conn.commit()
        return doc_id
    
    def insert_clause(self, text: str, clause_type: str = "", country: str = "", 
                     section_path: str = "", metadata: dict = None, importance_score: float = 0.0):
        """Insert a new clause into the database."""
        conn = self.connect()
        cur = conn.cursor()
        
        metadata_json = json.dumps(metadata or {})
        cur.execute("""
            INSERT INTO clauses (text, clause_type, country, section_path, metadata, importance_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (text, clause_type, country, section_path, metadata_json, importance_score))
        
        clause_id = cur.lastrowid
        conn.commit()
        return clause_id
    
    def link_document_clause(self, document_id: int, clause_id: int):
        """Link a clause to a document."""
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO document_clauses (document_id, clause_id)
            VALUES (?, ?)
        """, (document_id, clause_id))
        
        conn.commit()
    
    def get_clauses_by_type(self, clause_type: str, limit: int = 100):
        """Get clauses of a specific type."""
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, text, clause_type, country, section_path, metadata, importance_score
            FROM clauses
            WHERE clause_type = ?
            ORDER BY importance_score DESC
            LIMIT ?
        """, (clause_type, limit))
        
        results = []
        for row in cur.fetchall():
            results.append({
                'id': row[0],
                'text': row[1],
                'clause_type': row[2],
                'country': row[3],
                'section_path': row[4],
                'metadata': json.loads(row[5]) if row[5] else {},
                'importance_score': row[6]
            })
        
        return results
    
    def search_clauses(self, query: str, limit: int = 50):
        """Search clauses by text content."""
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, text, clause_type, country, section_path, metadata, importance_score
            FROM clauses
            WHERE text LIKE ?
            ORDER BY importance_score DESC
            LIMIT ?
        """, (f"%{query}%", limit))
        
        results = []
        for row in cur.fetchall():
            results.append({
                'id': row[0],
                'text': row[1],
                'clause_type': row[2],
                'country': row[3],
                'section_path': row[4],
                'metadata': json.loads(row[5]) if row[5] else {},
                'importance_score': row[6]
            })
        
        return results
    
    def get_document_clauses(self, document_id: int):
        """Get all clauses for a specific document."""
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT c.id, c.text, c.clause_type, c.country, c.section_path, c.metadata, c.importance_score
            FROM clauses c
            JOIN document_clauses dc ON c.id = dc.clause_id
            WHERE dc.document_id = ?
            ORDER BY c.importance_score DESC
        """, (document_id,))
        
        results = []
        for row in cur.fetchall():
            results.append({
                'id': row[0],
                'text': row[1],
                'clause_type': row[2],
                'country': row[3],
                'section_path': row[4],
                'metadata': json.loads(row[5]) if row[5] else {},
                'importance_score': row[6]
            })
        
        return results

def build_database():
    """
    Build the legal database from knowledge base files.
    """
    # Remove existing DB/index if any
    if os.path.exists(KB_SQLITE):
        os.remove(KB_SQLITE)
    
    db = LegalDatabase()
    conn = db.connect()
    cur = conn.cursor()
    
    texts = []
    id_map = {}
    pos = 0
    
    for fname in os.listdir(KB_DIR):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(KB_DIR, fname)
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        
        # Expected format: { "clauses": [ { "section": "...", "text": "...", "meta": {...} }, ... ] }
        for clause in tqdm(data.get("clauses", []), desc=fname):
            section = clause.get("section", "")
            text = clause.get("text", "")
            metadata = clause.get("meta", {})
            
            cur.execute("""
                INSERT INTO clauses (country, section_path, text, metadata)
                VALUES (?, ?, ?, ?)
            """, (metadata.get("country", ""), section, text, json.dumps(metadata)))
            
            rowid = cur.lastrowid
            if text:
                texts.append(text)
                id_map[str(pos)] = rowid
                pos += 1
    
    conn.commit()
    conn.close()
    
    # Build FAISS index if texts exist
    if texts:
        embs = encode_texts(texts)
        save_faiss_index(embs, path=FAISS_INDEX)
        save_id_map(id_map, path=ID_MAP)
    
    print("Database build complete.")

# New functions for analysis result storage
def save_analysis_result(filename: str, file_path: str, clauses: List[Dict[str, Any]]) -> int:
    """Save analysis result to database."""
    try:
        db = LegalDatabase()
        conn = db.connect()
        cursor = conn.cursor()
        
        # Create analysis_results table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT,
                total_characters INTEGER,
                total_clauses INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create analysis_clauses table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_clauses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER,
                clause_id TEXT NOT NULL,
                text TEXT NOT NULL,
                clause_type TEXT,
                confidence REAL,
                priority_score REAL,
                color TEXT,
                rank INTEGER,
                FOREIGN KEY (analysis_id) REFERENCES analysis_results (id)
            )
        """)
        
        # Insert analysis result
        cursor.execute("""
            INSERT INTO analysis_results (filename, file_path, total_characters, total_clauses)
            VALUES (?, ?, ?, ?)
        """, (
            filename, 
            file_path, 
            sum(len(c.get('text', '')) for c in clauses), 
            len(clauses)
        ))
        
        analysis_id = cursor.lastrowid
        
        # Insert clauses
        for clause in clauses:
            cursor.execute("""
                INSERT INTO analysis_clauses (analysis_id, clause_id, text, clause_type, confidence, priority_score, color, rank)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis_id,
                clause.get('clause_id', ''),
                clause.get('text', ''),
                clause.get('type', ''),
                clause.get('confidence', 0.0),
                clause.get('priority_score', 0.0),
                clause.get('color', 'green'),
                clause.get('rank', 0)
            ))
        
        conn.commit()
        conn.close()
        
        logging.info(f"Saved analysis result for {filename}")
        return analysis_id
        
    except Exception as e:
        logging.error(f"Failed to save analysis result: {e}")
        raise

def get_analysis_history(limit: int = 10) -> List[Dict[str, Any]]:
    """Get analysis history."""
    try:
        db = LegalDatabase()
        conn = db.connect()
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT,
                total_characters INTEGER,
                total_clauses INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            SELECT * FROM analysis_results 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
        
    except Exception as e:
        logging.error(f"Failed to get analysis history: {e}")
        return []

if __name__ == "__main__":
    build_database()
