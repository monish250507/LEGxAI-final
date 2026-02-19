import requests
import os

def test_openrouter_status():
    """Test OpenRouter API status and validate API key."""
    
    # Test with your NEW API key
    api_key = "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"
    
    print("🔍 Testing OpenRouter API Status...")
    print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    
    # Test API health
    health_url = "https://openrouter.ai/api/v1/auth/key"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(health_url, headers=headers)
        print(f"Health Check Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Key Valid: {data.get('data', {}).get('is_valid', False)}")
            print(f"Usage: {data.get('data', {}).get('usage', {})}")
        else:
            print(f"❌ API Key Invalid: {response.text}")
            
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
    
    # Test actual Claude call
    print("\n🤖 Testing Claude 3.5 Sonnet Call...")
    claude_url = "https://openrouter.ai/api/v1/chat/completions"
    
    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {
                "role": "user",
                "content": "Test message - say 'API working' if you receive this"
            }
        ]
    }
    
    try:
        response = requests.post(claude_url, headers=headers, json=payload)
        print(f"Claude API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
            print(f"✅ Claude Response: {message}")
        else:
            print(f"❌ Claude API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Claude Test Failed: {e}")

if __name__ == "__main__":
    test_openrouter_status()
