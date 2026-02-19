import requests
import json

def test_openrouter_alternative():
    """Test OpenRouter with different approaches."""
    
    print("🔍 Testing OpenRouter API Alternatives...")
    
    # Test 1: Direct health check
    print("\n1. Testing OpenRouter Health...")
    try:
        health_response = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        print(f"   Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            models = health_response.json()
            claude_models = [m for m in models.get('data', []) if 'claude' in m.get('id', '')]
            print(f"   Claude Models Available: {len(claude_models)}")
            for model in claude_models:
                print(f"   - {model.get('id', 'Unknown')}")
    except Exception as e:
        print(f"   Health Error: {e}")
    
    # Test 2: Try with different key format
    print("\n2. Testing with sample key format...")
    test_keys = [
        "sk-or-v1-test-key-format",
        "sk-test-key-format",
    ]
    
    for test_key in test_keys:
        try:
            headers = {"Authorization": f"Bearer {test_key}"}
            response = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers, timeout=5)
            print(f"   Key {test_key[:10]}...: Status {response.status_code}")
        except Exception as e:
            print(f"   Key {test_key[:10]}...: Error {e}")
    
    # Test 3: Check if service is down
    print("\n3. Testing service availability...")
    try:
        response = requests.get("https://status.openrouter.ai/", timeout=10)
        print(f"   Service Status: {response.status_code}")
    except Exception as e:
        print(f"   Service Check Error: {e}")
    
    print("\n📋 RECOMMENDATIONS:")
    print("1. Check if OpenRouter API is operational")
    print("2. Verify API key format (should start with 'sk-or-v1-')")
    print("3. Check if API key has proper permissions")
    print("4. Try generating a new API key from OpenRouter dashboard")
    print("5. Consider using alternative AI service temporarily")

if __name__ == "__main__":
    test_openrouter_alternative()
