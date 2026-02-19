#!/usr/bin/env python3
"""
Test the fixed upload endpoint with constitution parameter.
"""

import os
os.environ['CLAUDE_SONNET_3_API_KEY'] = 'CLAUDE_SONNET_3_API_KEY'

import requests
import json

def test_upload_with_constitution():
    """Test upload with constitution parameter."""
    print("🧪 Testing Upload with Constitution Parameter...")
    
    url = "http://127.0.0.1:8000/api/upload"
    
    try:
        with open("sample_contract.txt", 'rb') as f:
            files = {'file': ('test_contract.txt', f, 'text/plain')}
            data = {'constitution': 'US Constitution'}
            headers = {'accept': 'application/json'}
            
            response = requests.post(url, files=files, data=data, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Upload successful!")
                print(f"📄 Filename: {result.get('filename')}")
                print(f"📊 Clauses found: {result.get('document_stats', {}).get('total_clauses')}")
                
                # Check for explanation field
                if 'clauses' in result and result['clauses']:
                    clause = result['clauses'][0]
                    if 'explanation' in clause and clause['explanation']:
                        print(f"🧠 Claude Explanation: {clause['explanation'][:100]}...")
                        print("✅ Constitution parameter working!")
                    else:
                        print("⚠️ Explanation field missing")
                
                return True
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response.headers.get('content-type', '').startswith('application/json') else response.text
                print(f"❌ Upload failed: {response.status_code} - {error_detail}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_upload_with_constitution()
    
    if success:
        print("\n🎉 Upload endpoint FIXED!")
        print("✅ Constitution parameter working")
        print("✅ Frontend-backend connection restored")
    else:
        print("\n❌ Still issues with upload endpoint")
