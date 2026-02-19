#!/usr/bin/env python3
"""
Direct test of Claude 3.5 Sonnet API.
"""

import os
os.environ['CLAUDE_SONNET_3_API_KEY'] = 'CLAUDE_SONNET_3_API_KEY'

from ai.generative_service import generate_clause_explanation

def test_claude_direct():
    """Test Claude API directly."""
    print("🧪 Testing Claude 3.5 Sonnet API directly...")
    
    clause_text = "Payment shall be made within thirty (30) days of receipt of invoice. All payments shall be made in US dollars."
    constitution = "US Constitution"
    clause_type = "payment"
    
    try:
        explanation = generate_clause_explanation(clause_text, constitution, clause_type)
        
        print(f"🤖 Claude Response: {explanation[:200]}...")
        
        if explanation and explanation != "AI explanation unavailable.":
            print("✅ Claude 3.5 Sonnet API working!")
            return True
        else:
            print("❌ Claude API returned fallback message")
            return False
            
    except Exception as e:
        print(f"❌ Claude test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_claude_direct()
    
    if success:
        print("\n🎉 Claude API Test PASSED!")
    else:
        print("\n❌ Claude API Test FAILED!")
