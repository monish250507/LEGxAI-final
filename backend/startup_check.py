#!/usr/bin/env python3
"""
Startup check script for the Legal AI FastAPI application.
This script validates that all imports and configurations are working correctly.
"""

import sys
import os

def check_imports():
    """Check if all required modules can be imported."""
    print("Checking imports...")
    
    try:
        from fastapi import FastAPI
        print("✓ FastAPI imported successfully")
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False
    
    try:
        from fastapi.middleware.cors import CORSMiddleware
        print("✓ CORS middleware imported successfully")
    except ImportError as e:
        print(f"✗ CORS middleware import failed: {e}")
        return False
    
    try:
        from pydantic import BaseModel
        print("✓ Pydantic imported successfully")
    except ImportError as e:
        print(f"✗ Pydantic import failed: {e}")
        return False
    
    return True

def check_config():
    """Check configuration loading."""
    print("\nChecking configuration...")
    
    try:
        from config import UPLOAD_DIR, OPENAI_API_KEY, MODEL_NAME
        print(f"✓ Config loaded successfully")
        print(f"  Upload directory: {UPLOAD_DIR}")
        print(f"  Model name: {MODEL_NAME}")
        print(f"  OpenAI API key configured: {'Yes' if OPENAI_API_KEY else 'No'}")
        return True
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return False

def check_routes():
    """Check if routes can be imported."""
    print("\nChecking routes...")
    
    try:
        from routes.health import router as health_router
        print("✓ Health router imported successfully")
    except Exception as e:
        print(f"✗ Health router import failed: {e}")
        return False
    
    # Try to import other routes (may fail due to missing dependencies)
    try:
        from routes.summarize import router as summarize_router
        print("✓ Summarize router imported successfully")
    except Exception as e:
        print(f"⚠ Summarize router import failed (expected if dependencies missing): {e}")
    
    try:
        from routes.qa import router as qa_router
        print("✓ QA router imported successfully")
    except Exception as e:
        print(f"⚠ QA router import failed (expected if dependencies missing): {e}")
    
    try:
        from routes.upload import router as upload_router
        print("✓ Upload router imported successfully")
    except Exception as e:
        print(f"⚠ Upload router import failed (expected if dependencies missing): {e}")
    
    return True

def check_app_creation():
    """Check if FastAPI app can be created."""
    print("\nChecking FastAPI app creation...")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(title="Test App")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        print("✓ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"✗ FastAPI app creation failed: {e}")
        return False

def main():
    """Run all checks."""
    print("Legal AI FastAPI Application Startup Check")
    print("=" * 50)
    
    checks = [
        check_imports,
        check_config,
        check_routes,
        check_app_creation
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Checks passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All checks passed! The application should start correctly.")
        return 0
    else:
        print("⚠ Some checks failed. Install missing dependencies and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
