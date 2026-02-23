import sys
import os
sys.path.append('ai')
sys.path.append('routes')

from dotenv import load_dotenv
load_dotenv()

from ai.chatbot_service import get_chatbot_service
from services.document_analysis_service import DocumentAnalysisService

print("🔍 Testing Chatbot Infrastructure:")

# Test chatbot service initialization
print("\n1. Testing chatbot service initialization...")
chatbot = get_chatbot_service()
print(f"   Chatbot service: {'✅' if chatbot else '❌'}")
print(f"   Generative service available: {'✅' if chatbot.generative_service.api_available else '❌'}")
print(f"   Constitution matcher available: {'✅' if chatbot.constitution_matcher else '❌'}")

# Test session creation
print("\n2. Testing session creation...")
sample_clauses = [
    {
        "text": "All parties shall have the right to freedom of speech and expression.",
        "type": "fundamental_rights",
        "risk_level": "medium",
        "constitution_reference": "Article 1: Freedom of Speech",
        "explanation": "This clause guarantees freedom of speech."
    },
    {
        "text": "No person shall be deprived of their property without due process of law.",
        "type": "property_rights",
        "risk_level": "low",
        "constitution_reference": "Article 2: Due Process",
        "explanation": "This clause protects property rights."
    }
]

sample_document = """
This agreement is made on January 1, 2024 between Party A and Party B.

1. All parties shall have the right to freedom of speech and expression.
2. No person shall be deprived of their property without due process of law.
3. The parties agree to maintain confidentiality of all information shared.
"""

try:
    session_id = chatbot.create_session(
        document_text=sample_document,
        constitution="US Constitution",
        clauses=sample_clauses
    )
    print(f"   ✅ Session created: {session_id}")
except Exception as e:
    print(f"   ❌ Session creation failed: {e}")
    session_id = None

# Test message handling
if session_id:
    print("\n3. Testing message handling...")
    try:
        # Add user message
        chatbot.add_message(session_id, "user", "What are the key risks in this document?")
        
        # Get conversation history
        history = chatbot.get_conversation_history(session_id)
        print(f"   ✅ Messages in conversation: {len(history)}")
        
        # Test contextual analysis
        result = chatbot.analyze_clause_in_context(
            session_id=session_id,
            clause_text="All parties shall have the right to freedom of speech and expression",
            question="What are the implications of this clause?"
        )
        
        print(f"   ✅ Contextual analysis completed")
        print(f"   Analysis length: {len(result.get('analysis', ''))}")
        print(f"   Clause type: {result.get('clause_type', 'unknown')}")
        print(f"   Risk level: {result.get('risk_level', 'unknown')}")
        
    except Exception as e:
        print(f"   ❌ Message handling failed: {e}")

# Test document summary
if session_id:
    print("\n4. Testing document summary...")
    try:
        summary = chatbot.get_document_summary(session_id)
        print(f"   ✅ Document summary generated")
        print(f"   Total clauses: {summary['document_info']['total_clauses']}")
        print(f"   High risk clauses: {summary['document_info']['high_risk_clauses']}")
        print(f"   Most common clause type: {summary['key_insights']['most_common_clause_type']}")
        
    except Exception as e:
        print(f"   ❌ Document summary failed: {e}")

# Test session stats
if session_id:
    print("\n5. Testing session statistics...")
    try:
        stats = chatbot.get_session_stats(session_id)
        print(f"   ✅ Session stats retrieved")
        print(f"   Total messages: {stats['total_messages']}")
        print(f"   Document clauses: {stats['document_clauses']}")
        print(f"   Performance hit rate: {stats['performance_stats']['hit_rate_percent']}%")
        
    except Exception as e:
        print(f"   ❌ Session stats failed: {e}")

# Test session cleanup
if session_id:
    print("\n6. Testing session cleanup...")
    try:
        chatbot.clear_session(session_id)
        print(f"   ✅ Session cleared successfully")
        
        # Verify session is gone
        try:
            chatbot.get_document_summary(session_id)
            print("   ❌ Session still exists after cleanup")
        except ValueError:
            print("   ✅ Session properly removed")
            
    except Exception as e:
        print(f"   ❌ Session cleanup failed: {e}")

print("\n📋 Chatbot infrastructure testing completed.")
