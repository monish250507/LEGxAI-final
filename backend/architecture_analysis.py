import os
import json

print("=" * 80)
print("🔍 PHASE 1 - FULL FILE STRUCTURE ANALYSIS")
print("=" * 80)

# Core files analysis
core_files = {
    "main.py": "FastAPI application entry point",
    "document_analysis_service.py": "Main document processing pipeline",
    "embedding_service.py": "Embedding generation service",
    "semantic_classifier.py": "Clause classification service", 
    "semantic_ranker.py": "Clause ranking service",
    "clause_extractor.py": "Clause extraction service",
    "document_processor.py": "Document text extraction",
    "generative_service.py": "AI generative reasoning"
}

print("\n📁 CORE FILES STATUS:")
for file, desc in core_files.items():
    if os.path.exists(file):
        print(f"   ✅ {file}: {desc}")
    elif os.path.exists(f"ai/{file}"):
        print(f"   ✅ ai/{file}: {desc}")
    elif os.path.exists(f"services/{file}"):
        print(f"   ✅ services/{file}: {desc}")
    else:
        print(f"   ❌ {file}: MISSING - {desc}")

# Current pipeline analysis
print("\n🔄 CURRENT PIPELINE ANALYSIS:")
try:
    with open('services/document_analysis_service.py', 'r') as f:
        content = f.read()
    
    if "extract_text" in content:
        print("   ✅ Text extraction")
    if "extract_clauses" in content:
        print("   ✅ Clause extraction")
    if "semantic_classify" in content:
        print("   ✅ Semantic classification")
    if "semantic_rank" in content:
        print("   ✅ Semantic ranking")
    if "generate_clause_explanation" in content:
        print("   ✅ Generative explanation")
    if "constitution" in content.lower():
        print("   ⚠️  Constitution awareness (partial)")
    else:
        print("   ❌ Constitution awareness (missing)")
        
except Exception as e:
    print(f"   ❌ Pipeline analysis failed: {e}")

# Missing components analysis
print("\n🚨 MISSING COMPONENTS:")
missing_components = []

if not os.path.exists('ai/constitution_matcher.py'):
    missing_components.append("Constitution matcher")

if not os.path.exists('ai/chat_service.py'):
    missing_components.append("Chat service")

if missing_components:
    for comp in missing_components:
        print(f"   ❌ {comp}")
else:
    print("   ✅ All components present")

# Constitution data analysis
print("\n📋 CONSTITUTION DATA ANALYSIS:")
constitutions = ['COI.json', 'China_2018.json', 'Japan_1946.json', 'Russia_2014.json']
for const in constitutions:
    if os.path.exists(f'data/{const}'):
        try:
            with open(f'data/{const}', 'r') as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                print(f"   ✅ {const}: {len(data[0]) if isinstance(data[0], list) else len(data)} sections")
            elif 'document' in data:
                print(f"   ✅ {const}: {len(data['document']['section'])} sections")
            else:
                print(f"   ⚠️  {const}: Unknown structure")
        except:
            print(f"   ❌ {const}: Load error")
    else:
        print(f"   ❌ {const}: Missing")

# Architecture summary
print("\n" + "=" * 80)
print("📊 ARCHITECTURE SUMMARY")
print("=" * 80)

print("\n✅ WORKING COMPONENTS:")
print("   - FastAPI backend with CORS")
print("   - Document upload and processing")
print("   - Multi-format text extraction")
print("   - Semantic classification and ranking")
print("   - Embedding generation")
print("   - Constitution data files")

print("\n⚠️  NEEDS UPGRADING:")
print("   - Constitution-aware matching")
print("   - Multi-model generative fallback")
print("   - Offensive/defensive analysis")
print("   - Chatbot infrastructure")

print("\n🎯 UPGRADE PLAN:")
print("   1. Add constitution matcher")
print("   2. Upgrade generative service")
print("   3. Enhance document analysis pipeline")
print("   4. Add performance optimization")
print("   5. Create chat service")

print("=" * 80)
