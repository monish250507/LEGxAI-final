#!/usr/bin/env python3
"""
Test script for Claude 3.5 Sonnet integration.
"""

import os
os.environ['OPENROUTER_API_KEY'] = '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'

import requests
import json

def test_upload_endpoint():
    """Test upload endpoint with sample contract."""
    
    # API endpoint
    url = "http://127.0.0.1:8000/api/upload"
    
    # Sample file path
    file_path = "sample_contract.txt"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'text/plain')}
            headers = {'accept': 'application/json'}
            
            print(f"Testing upload endpoint: {url}")
            print(f"Uploading file: {file_path}")
            
            response = requests.post(url, files=files, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Upload successful!")
                print("\n=== ANALYSIS RESULT ===")
                print(json.dumps(result, indent=2))
                
                # Check for explanation field
                if 'clauses' in result and result['clauses']:
                    clause = result['clauses'][0]
                    if 'explanation' in clause:
                        print(f"✅ Explanation field present: {clause['explanation'][:100]}...")
                    else:
                        print("❌ Explanation field missing")
                
                return True
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_upload_endpoint()
    if success:
        print("\n🎉 Upload test with Claude 3.5 Sonnet PASSED!")
    else:
        print("\n⚠️ Upload test FAILED!")
