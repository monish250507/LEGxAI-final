import sys
import os
from dotenv import load_dotenv

print("🔍 Backend Startup Validation:")

# Load environment variables
load_dotenv()

# Test 1: Environment variables
print("\n1. Environment Variables:")
api_key = os.getenv("OPENROUTER_API_KEY")
print(f"   OPENROUTER_API_KEY: {'✅' if api_key else '❌'}")

# Test 2: Import critical modules
print("\n2. Module Imports:")
try:
    from fastapi import FastAPI
    print("   ✅ FastAPI")
except ImportError as e:
    print(f"   ❌ FastAPI: {e}")

try:
    from services.document_analysis_service import DocumentAnalysisService
    print("   ✅ DocumentAnalysisService")
except ImportError as e:
    print(f"   ❌ DocumentAnalysisService: {e}")

try:
    from ai.embedding_service import load_model
    print("   ✅ EmbeddingService")
except ImportError as e:
    print(f"   ❌ EmbeddingService: {e}")

try:
    from document_processor import DocumentProcessor
    print("   ✅ DocumentProcessor")
except ImportError as e:
    print(f"   ❌ DocumentProcessor: {e}")

# Test 3: FastAPI app initialization
print("\n3. FastAPI App Initialization:")
try:
    from main import app
    print("   ✅ FastAPI app initialized")
except Exception as e:
    print(f"   ❌ FastAPI app failed: {e}")

# Test 4: Service initialization
print("\n4. Service Initialization:")
try:
    doc_service = DocumentAnalysisService()
    print("   ✅ DocumentAnalysisService initialized")
except Exception as e:
    print(f"   ❌ DocumentAnalysisService failed: {e}")

try:
    processor = DocumentProcessor()
    print("   ✅ DocumentProcessor initialized")
except Exception as e:
    print(f"   ❌ DocumentProcessor failed: {e}")

print("\n📋 Backend startup validation completed.")
