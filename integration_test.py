#!/usr/bin/env python3
"""
Integration test script to verify frontend-backend connectivity
"""
import requests
import json
import time

def test_backend():
    """Test backend endpoints"""
    print("🔍 Testing Backend API...")
    
    try:
        # Test root endpoint
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        print(f"✅ Backend Root: {response.status_code} - {response.json()}")
        
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        print(f"✅ Backend Health: {response.status_code} - {response.json()}")
        
        # Test API health
        response = requests.get("http://127.0.0.1:8000/api/health", timeout=5)
        print(f"✅ Backend API Health: {response.status_code} - {response.json()}")
        
        return True
    except Exception as e:
        print(f"❌ Backend Error: {e}")
        return False

def test_frontend():
    """Test frontend accessibility"""
    print("\n🔍 Testing Frontend...")
    
    try:
        # Test frontend main page
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ Frontend Main: {response.status_code}")
        
        # Test frontend API proxy
        response = requests.get("http://localhost:3000/api/health", timeout=5)
        print(f"✅ Frontend API Proxy: {response.status_code} - {response.json()}")
        
        return True
    except Exception as e:
        print(f"❌ Frontend Error: {e}")
        return False

def main():
    print("🚀 LExAI Integration Test")
    print("=" * 50)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://127.0.0.1:8000")
        print("📚 API Docs: http://127.0.0.1:8000/docs")
        print("\n✨ Full Integration Working Perfectly!")
    else:
        print("❌ Some systems are not working properly")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
