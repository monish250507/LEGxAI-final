#!/usr/bin/env python3
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
