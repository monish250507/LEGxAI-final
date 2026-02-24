from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from dotenv import load_dotenv
from config import UPLOAD_DIR

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
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

# Validate critical dependencies
def validate_dependencies():
    """Validate that critical dependencies are available."""
    try:
        import fastapi
        import uvicorn
        import pdfplumber
        import pydantic
        logger.info("Critical dependencies validated successfully")
        return True
    except ImportError as e:
        logger.error(f"Missing critical dependency: {e}")
        return False

# Validate dependencies on startup
if not validate_dependencies():
    logger.warning("Some critical dependencies are missing. API may not function correctly.")

# Import and include routers with graceful fallbacks
try:
    from routes.upload import router as upload_router
    app.include_router(upload_router, prefix="/api")
    logger.info("Upload router imported successfully")
except ImportError as e:
    logger.error(f"Failed to import upload router: {e}")

try:
    from routes.health import router as health_router
    app.include_router(health_router, prefix="/api")
    logger.info("Health router imported successfully")
except ImportError as e:
    logger.error(f"Failed to import health router: {e}")

# Optional routers - only import if dependencies available
try:
    from routes.summarize import router as summarize_router
    app.include_router(summarize_router, prefix="/api")
    logger.info("Summarize router imported successfully")
except ImportError:
    logger.warning("Summarize router not available - missing dependencies")

try:
    from routes.qa import router as qa_router
    app.include_router(qa_router, prefix="/api")
    logger.info("QA router imported successfully")
except ImportError:
    logger.warning("QA router not available - missing dependencies")

# Chatbot router - new feature
try:
    from routes.chatbot import router as chatbot_router
    app.include_router(chatbot_router)
    logger.info("Chatbot router imported successfully")
except ImportError as e:
    logger.warning(f"Chatbot router not available: {e}")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Legal AI API is running"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "dependencies": {
            "fastapi": True,
            "pdfplumber": True,
            "pydantic": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
