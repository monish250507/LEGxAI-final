print("🔍 Requirements.txt Validation:")

required_deps = [
    "fastapi",
    "uvicorn", 
    "sentence-transformers",
    "torch",
    "requests",
    "python-dotenv",
    "numpy",
    "pdfplumber",
    "scikit-learn"
]

with open('requirements.txt', 'r') as f:
    current_deps = f.read().splitlines()

print("Current dependencies:")
for dep in current_deps:
    if dep.strip():
        print(f"  ✅ {dep}")

print("\nChecking for missing dependencies:")
missing = []
for req_dep in required_deps:
    found = any(req_dep.lower() in dep.lower() for dep in current_deps)
    if found:
        print(f"  ✅ {req_dep}")
    else:
        print(f"  ❌ {req_dep} - MISSING")
        missing.append(req_dep)

if missing:
    print(f"\n📝 Adding missing dependencies: {missing}")
    with open('requirements.txt', 'a') as f:
        for dep in missing:
            f.write(f"\n{dep}")
    print("✅ Requirements.txt updated")
else:
    print("\n✅ All required dependencies present")
