from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Test basic FastAPI app creation
app = FastAPI(
    title="Legal AI API",
    description="AI-powered legal document analysis API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Legal AI API is running"}

@app.get("/test")
def test():
    return {"status": "ok", "message": "FastAPI app is working"}

if __name__ == "__main__":
    import uvicorn
    print("Testing FastAPI app startup...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
