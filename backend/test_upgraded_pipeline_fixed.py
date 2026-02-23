import sys
import os
sys.path.append('services')
sys.path.append('ai')

from dotenv import load_dotenv
load_dotenv()

from services.document_analysis_service import DocumentAnalysisService
from fastapi import UploadFile
import tempfile

print("🔍 Testing Upgraded Document Analysis Pipeline:")

# Test service initialization
print("\n1. Testing service initialization...")
service = DocumentAnalysisService()
print(f"   Semantic enabled: {'✅' if service.semantic_enabled else '❌'}")
print(f"   Constitution matcher: {'✅' if service.constitution_matcher else '❌'}")

# Test pipeline with real file
print("\n2. Testing comprehensive analysis pipeline...")

try:
    # Create a proper UploadFile object
    with open('test_sample.txt', 'rb') as f:
        file_content = f.read()
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name
    
    # Create UploadFile object
    with open(tmp_path, 'rb') as f:
        upload_file = UploadFile(filename="test_agreement.txt", file=f)
        
        # Test the analysis
        import asyncio
        result = asyncio.run(service.analyze_document(upload_file, "US Constitution"))
    
    print("   ✅ Analysis completed successfully")
    print(f"   Status: {result.get('status', 'unknown')}")
    print(f"   Filename: {result.get('filename', 'unknown')}")
    print(f"   Clauses found: {len(result.get('clauses', []))}")
    
    # Check first clause for comprehensive analysis
    if result.get('clauses'):
        first_clause = result['clauses'][0]
        print(f"   First clause type: {first_clause.get('type', 'unknown')}")
        print(f"   Explanation length: {len(first_clause.get('explanation', '') or '')}")
        print(f"   Offensive analysis length: {len(first_clause.get('offensive_analysis', '') or '')}")
        print(f"   Defensive analysis length: {len(first_clause.get('defensive_analysis', '') or '')}")
        print(f"   Risk level: {first_clause.get('risk_level', 'unknown')}")
        print(f"   Constitution reference: {first_clause.get('constitution_reference', '')[:50]}...")
    
    # Clean up
    os.unlink(tmp_path)
    
except Exception as e:
    print(f"   ❌ Analysis failed: {e}")
    import traceback
    traceback.print_exc()

print("\n📋 Upgraded pipeline testing completed.")
