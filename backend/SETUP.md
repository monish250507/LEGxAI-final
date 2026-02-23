# FastAPI Backend Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application
```bash
# Option 1: Using the test script (minimal dependencies)
python run_server.py

# Option 2: Using uvicorn directly
uvicorn main_minimal:app --reload --host 0.0.0.0 --port 8000

# Option 3: Full application (requires all dependencies)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Available Endpoints

### Health Check
- `GET /api/health` - Health check endpoint

### Document Analysis
- `POST /api/summarize` - Summarize legal documents
- `POST /api/qa` - Ask questions about documents
- `POST /api/upload` - Upload document files

## Testing

### Run Startup Checks
```bash
python startup_check.py
```

### Run Startup Tests
```bash
python test_startup.py
```

## Dependencies

### Core Dependencies
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `pydantic` - Data validation

### AI/ML Dependencies
- `openai` - OpenAI API client
- `sentence-transformers` - Text embeddings
- `faiss-cpu` - Vector search
- `spacy` - NLP processing

### Document Processing
- `textract` - Document text extraction
- `reportlab` - PDF generation

### Utilities
- `python-dotenv` - Environment variable management
- `python-multipart` - File upload support

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'openai'**
   - Solution: Install dependencies with `pip install -r requirements.txt`

2. **Permission denied on upload directory**
   - Solution: Ensure the data/uploads directory exists and is writable

3. **OpenAI API key not configured**
   - Solution: Set OPENAI_API_KEY in .env file

### Development Mode

For development with auto-reload:
```bash
uvicorn main_minimal:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

For production deployment:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Architecture

```
backend/
├── main.py              # Full FastAPI application (requires all deps)
├── main_minimal.py      # Minimal version for testing
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── routes/              # API route handlers
│   ├── health.py        # Health check endpoint
│   ├── summarize.py     # Document summarization
│   ├── qa.py           # Question answering
│   └── upload.py       # File upload
├── services/            # Business logic
│   ├── ai_pipeline.py   # AI processing (requires OpenAI)
│   ├── embeddings.py    # Text embeddings
│   ├── parser.py        # Document parsing
│   └── ...
├── models.py            # Data models
├── database.py          # Database operations
└── clause_*.py          # Legal clause processing
```
