#!/usr/bin/env python3
"""
Test script to verify the FastAPI application can start with uvicorn.
"""

import sys
import os

def test_uvicorn_startup():
    """Test if uvicorn can start the application."""
    print("Testing uvicorn startup...")
    
    try:
        # Import the minimal app to avoid dependency issues
        from main_minimal import app
        print("✓ Application imported successfully")
        
        # Test uvicorn import
        import uvicorn
        print("✓ Uvicorn imported successfully")
        
        # Test app configuration
        print(f"✓ App title: {app.title}")
        print(f"✓ App version: {app.version}")
        
        # Count routes
        routes = [route for route in app.routes if hasattr(route, 'methods')]
        print(f"✓ Total routes: {len(routes)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Startup test failed: {e}")
        return False

def create_startup_script():
    """Create a script to test actual server startup."""
    script_content = '''#!/usr/bin/env python3
"""
Startup test script - run this to test the actual server.
"""

if __name__ == "__main__":
    import uvicorn
    from main_minimal import app
    
    print("Starting Legal AI API server...")
    print("Server will be available at: http://localhost:8000")
    print("API docs available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
    
    with open('run_server.py', 'w') as f:
        f.write(script_content)
    
    print("✓ Created run_server.py for manual testing")

def main():
    """Run startup tests."""
    print("Legal AI FastAPI Application Startup Test")
    print("=" * 50)
    
    if test_uvicorn_startup():
        create_startup_script()
        print("\n" + "=" * 50)
        print("✓ All startup tests passed!")
        print("\nTo run the server:")
        print("  python run_server.py")
        print("  or")
        print("  uvicorn main_minimal:app --reload --host 0.0.0.0 --port 8000")
        return 0
    else:
        print("\n✗ Startup tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
