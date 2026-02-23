import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai'))

from embedding_service import load_model, generate_embeddings

print("🔍 Embedding Model Validation:")

try:
    # Test model loading
    print("Loading embedding model...")
    load_model()
    print("✅ Model loaded successfully")
    
    # Test embedding generation
    test_text = "test clause for embedding validation"
    test_clauses = [{"text": test_text}]
    
    print("Generating test embedding...")
    embeddings = generate_embeddings(test_clauses)
    
    if embeddings is not None and len(embeddings) > 0:
        print(f"✅ Embedding generated successfully")
        print(f"   Shape: {embeddings.shape}")
        print(f"   Dimensions: {len(embeddings[0])}")
    else:
        print("❌ Embedding generation failed")
        
except Exception as e:
    print(f"❌ Embedding test failed: {e}")
    print("   This may indicate missing dependencies or model loading issues")

print("\n📋 Embedding validation completed.")
