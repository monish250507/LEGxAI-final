import requests

# Test LATEST API key
api_key = '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'
print('🔍 Testing NEW API Key...')
print(f'API Key: {api_key[:20]}...{api_key[-10:]}')

# Test health
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.get('https://openrouter.ai/api/v1/auth/key', headers=headers)
print(f'Health Status: {response.status_code}')

if response.status_code == 200:
    print('✅ API Key is VALID!')
    data = response.json()
    print(f'User: {data.get("data", {}).get("user", "Unknown")}')
else:
    print(f'❌ API Key Error: {response.text}')

# Test Claude call
print('\n🤖 Testing Claude 3.5 Sonnet...')
claude_url = 'https://openrouter.ai/api/v1/chat/completions'
payload = {
    'model': 'anthropic/claude-3.5-sonnet',
    'messages': [
        {
            'role': 'user',
            'content': 'Test message - say "API WORKING" if you receive this'
        }
    ]
}

try:
    response = requests.post(claude_url, headers=headers, json=payload)
    print(f'Claude Status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        message = data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        print(f'✅ Claude Response: {message}')
    else:
        print(f'❌ Claude Error: {response.text}')
except Exception as e:
    print(f'❌ Claude Test Failed: {e}')
