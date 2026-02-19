import sys
import os
sys.path.append('ai')

from generative_service import GenerativeService, generate_full_clause_analysis

print("🔍 Testing Upgraded Generative Service:")

# Test service initialization
print("\n1. Testing service initialization...")
service = GenerativeService()
print(f"   API Available: {'✅' if service.api_available else '❌'}")
print(f"   API Validated: {'✅' if service.api_validated else '❌'}")

# Test comprehensive analysis
print("\n2. Testing comprehensive analysis...")
test_clause = "All citizens shall have the right to freedom of speech and expression"
test_constitution = "US Constitution"
test_type = "fundamental_rights"

# Test with mock article
mock_article = {
    'article_number': '1',
    'title': 'Freedom of Speech',
    'similarity_score': 0.85
}

try:
    analysis = generate_full_clause_analysis(
        test_clause, 
        test_constitution, 
        test_type, 
        mock_article
    )
    
    print("   ✅ Analysis generated successfully")
    print(f"   Explanation length: {len(analysis.get('explanation', ''))}")
    print(f"   Offensive analysis length: {len(analysis.get('offensive_analysis', ''))}")
    print(f"   Defensive analysis length: {len(analysis.get('defensive_analysis', ''))}")
    print(f"   Risk level: {analysis.get('risk_level', 'unknown')}")
    print(f"   Constitution reference: {analysis.get('constitution_reference', 'None')[:50]}...")
    
except Exception as e:
    print(f"   ❌ Analysis failed: {e}")

# Test legacy method
print("\n3. Testing legacy method...")
try:
    legacy_explanation = service.generate_clause_explanation(test_clause, test_constitution, test_type)
    print(f"   Legacy explanation length: {len(legacy_explanation)}")
    print("   ✅ Legacy method working")
except Exception as e:
    print(f"   ❌ Legacy method failed: {e}")

print("\n📋 Upgraded generative service testing completed.")
