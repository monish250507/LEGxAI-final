#!/usr/bin/env python3
"""
Check environment variables for API key.
"""

import os

print("🔍 Checking Environment Variables:")
print(f"CLAUDE_SONNET_3_API_KEY: {'SET' if os.getenv('CLAUDE_SONNET_3_API_KEY') else 'NOT SET'}")
print(f"OPENROUTER_API_KEY: {'SET' if os.getenv('OPENROUTER_API_KEY') else 'NOT SET'}")

# Test generative service
try:
    from ai.generative_service import GenerativeService
    service = GenerativeService()
    print(f"Service API Key: {'SET' if service.api_key else 'NOT SET'}")
    if service.api_key:
        print(f"API Key Length: {len(service.api_key)} characters")
        print(f"API Key Preview: {service.api_key[:10]}...{service.api_key[-10:]}")
    else:
        print("❌ No API key found in service")
except Exception as e:
    print(f"❌ Error creating service: {e}")
