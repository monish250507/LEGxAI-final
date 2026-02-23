#!/usr/bin/env python3
"""
Test script for the upload endpoint with semantic analysis.
"""

import requests
import json

def test_upload_endpoint():
    """Test the upload endpoint with sample contract."""
    
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
                
                # Verify required fields
                required_fields = ['status', 'filename', 'analysis_method', 'document_stats', 'clauses', 'summary']
                for field in required_fields:
                    if field in result:
                        print(f"✅ Field '{field}' present")
                    else:
                        print(f"❌ Field '{field}' missing")
                
                # Check clause structure
                if 'clauses' in result and result['clauses']:
                    clause = result['clauses'][0]
                    clause_fields = ['clause_id', 'text', 'type', 'confidence', 'priority_score', 'color', 'rank']
                    print(f"\n=== SAMPLE CLAUSE ===")
                    print(json.dumps(clause, indent=2))
                    
                    for field in clause_fields:
                        if field in clause:
                            print(f"✅ Clause field '{field}' present")
                        else:
                            print(f"❌ Clause field '{field}' missing")
                
                return True
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint."""
    url = "http://127.0.0.1:8000/api/health"
    
    try:
        response = requests.get(url)
        print(f"\n=== HEALTH CHECK ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Legal AI Backend with Semantic Analysis")
    print("=" * 50)
    
    # Test health endpoint first
    health_ok = test_health_endpoint()
    
    # Test upload endpoint
    upload_ok = test_upload_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Upload Test: {'✅ PASS' if upload_ok else '❌ FAIL'}")
    
    if health_ok and upload_ok:
        print("\n🎉 ALL TESTS PASSED! Backend is working with semantic analysis!")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")
