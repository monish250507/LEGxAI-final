import os
from ai.generative_service import GenerativeService

print('Environment Check:')
print(f'CLAUDE_SONNET_3_API_KEY: {os.getenv("CLAUDE_SONNET_3_API_KEY", "NOT SET")[:20]}...')
service = GenerativeService()
print(f'Service API Key: {service.api_key[:20] if service.api_key else "NOT SET"}...')
print(f'API Key Valid: {len(service.api_key) > 10 if service.api_key else False}')

# Test actual API call
if service.api_key:
    try:
        result = service.generate_clause_explanation(
            "Payment shall be made within thirty days.",
            "US Constitution", 
            "payment"
        )
        print(f'API Test: {"SUCCESS" if result and "AI explanation unavailable" not in result else "FAILED"}')
        print(f'Result Preview: {result[:100] if result else "No result"}...')
    except Exception as e:
        print(f'API Error: {e}')
