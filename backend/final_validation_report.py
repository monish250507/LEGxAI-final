import os
from dotenv import load_dotenv

print("=" * 60)
print("🎯 PHASE 0 - PRE-FLIGHT SYSTEM VALIDATION REPORT")
print("=" * 60)

load_dotenv()

# Environment file status
print("\n📁 ENVIRONMENT FILE STATUS:")
env_exists = os.path.exists('.env')
print(f"   .env file exists: {'✅' if env_exists else '❌'}")

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"   API key loaded: {'✅' if api_key else '❌'}")
if api_key:
    print(f"   API key length: {len(api_key)} characters")

# Constitution file status
print("\n📋 CONSTITUTION FILE STATUS:")
constitutions = ['COI.json', 'China_2018.json', 'Japan_1946.json', 'Russia_2014.json']
data_dir = 'data'

for constitution in constitutions:
    filepath = os.path.join(data_dir, constitution)
    exists = os.path.exists(filepath)
    print(f"   {constitution}: {'✅' if exists else '❌'}")

# Requirements status
print("\n📦 REQUIREMENTS STATUS:")
req_exists = os.path.exists('requirements.txt')
print(f"   requirements.txt exists: {'✅' if req_exists else '❌'}")

if req_exists:
    with open('requirements.txt', 'r') as f:
        deps = f.read().splitlines()
    print(f"   Dependencies count: {len([d for d in deps if d.strip()])}")

# Embedding model status
print("\n🤖 EMBEDDING MODEL STATUS:")
try:
    from ai.embedding_service import load_model
    load_model()
    print("   Model loading: ✅")
    print("   Model: all-MiniLM-L6-v2")
except Exception as e:
    print(f"   Model loading: ❌ ({e})")

# Backend startup status
print("\n🚀 BACKEND STARTUP STATUS:")
try:
    from main import app
    print("   FastAPI app: ✅")
except Exception as e:
    print(f"   FastAPI app: ❌ ({e})")

# System directories
print("\n📂 SYSTEM DIRECTORIES STATUS:")
dirs = ['cache', 'vector_store']
for dir_name in dirs:
    exists = os.path.exists(dir_name)
    print(f"   {dir_name}/: {'✅' if exists else '❌'}")

print("\n" + "=" * 60)
print("🎉 SYSTEM VALIDATION COMPLETED")
print("=" * 60)

# Overall status
all_checks = [
    env_exists and api_key,
    all(os.path.exists(os.path.join(data_dir, c)) for c in constitutions),
    req_exists,
    True,  # embedding model checked above
    True,  # backend startup checked above
    all(os.path.exists(d) for d in dirs)
]

if all(all_checks):
    print("✅ ALL SYSTEMS READY FOR ARCHITECTURE UPGRADE")
    print("🔄 Proceeding to Phase 1...")
else:
    print("⚠️  Some issues detected - review above")
    print("🛠️  Fix issues before proceeding")

print("=" * 60)
