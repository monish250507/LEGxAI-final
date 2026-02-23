import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test API key loading
api_key = os.getenv("OPENROUTER_API_KEY")

print("🔍 Environment Validation:")
print(f"Environment file exists: {os.path.exists('.env')}")
print(f"OPENROUTER_API_KEY loaded: {'✅' if api_key else '❌'}")

if api_key:
    print(f"API Key length: {len(api_key)} characters")
    print(f"API Key preview: {api_key[:20]}...{api_key[-10:]}")
else:
    print("WARNING: OPENROUTER_API_KEY not found. Generative AI will use fallback mode.")
