from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def load_model():
    """
    Load embedding model once globally.
    Prevents reloading on every request.
    """
    global _model
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded successfully.")

def generate_embeddings(clauses):
    """
    Generate embeddings for clause list.

    Input:
        clauses: list of dicts with "text" field

    Output:
        numpy array of embeddings
    """
    load_model()

    if not clauses:
        return np.array([])

    texts = []

    for clause in clauses:
        if isinstance(clause, dict) and "text" in clause:
            texts.append(str(clause["text"]))
        else:
            texts.append(str(clause))

    embeddings = _model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    return embeddings
