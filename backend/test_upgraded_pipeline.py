import sys
import os
sys.path.append('services')
sys.path.append('ai')

from dotenv import load_dotenv
load_dotenv()

from services.document_analysis_service import DocumentAnalysisService

print("🔍 Testing Upgraded Document Analysis Pipeline:")

# Test service initialization
print("\n1. Testing service initialization...")
service = DocumentAnalysisService()
print(f"   Semantic enabled: {'✅' if service.semantic_enabled else '❌'}")
print(f"   Constitution matcher: {'✅' if service.constitution_matcher else '❌'}")

# Test pipeline with sample text
print("\n2. Testing comprehensive analysis pipeline...")

# Create a mock file object
class MockFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content.encode()
    
    async def read(self):
        return self.content

# Test with sample contract
sample_text = """
This agreement is made on January 1, 2024 between Party A and Party B.

1. All parties shall have the right to freedom of speech and expression.
2. No person shall be deprived of their property without due process of law.
3. The parties agree to maintain confidentiality of all information shared.
"""

mock_file = MockFile("test_agreement.txt", sample_text)

try:
    # Test the analysis
    import asyncio
    result = asyncio.run(service.analyze_document(mock_file, "US Constitution"))
    
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
    
except Exception as e:
    print(f"   ❌ Analysis failed: {e}")
    import traceback
    traceback.print_exc()

print("\n📋 Upgraded pipeline testing completed.")
