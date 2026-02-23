# LexAI - Constitution-Aware Generative Legal AI Platform

A production-grade legal document analysis platform with advanced AI capabilities including semantic clause extraction, constitution matching, generative analysis, and conversational AI.

## 🏗️ **Repository Structure**

```
lexai-legal-document-analysis/
│
├── backend/                    # FastAPI Python Backend
│   ├── main.py                # FastAPI application entry point
│   ├── ai/                    # AI Services
│   │   ├── generative_service.py
│   │   ├── constitution_matcher.py
│   │   ├── chatbot_service.py
│   │   └── performance_optimizer.py
│   ├── services/               # Business Logic
│   │   └── document_analysis_service.py
│   ├── routes/                 # API Endpoints
│   ├── data/                   # Constitution Files
│   ├── .env                    # Environment Variables
│   └── requirements.txt         # Python Dependencies
│
├── frontend/                   # Next.js TypeScript Frontend
│   ├── app/                    # Next.js 14 App Router
│   ├── components/              # React Components
│   ├── lib/                    # Utilities & API
│   ├── public/                 # Static Assets
│   ├── package.json            # Node.js Dependencies
│   └── tailwind.config.js      # Styling Configuration
│
└── README.md                  # This File
```

## 🚀 **Getting Started**

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:3000`

## 🤖 **AI Capabilities**

### Core Features
- **Semantic Clause Extraction**: Advanced NLP-powered clause identification
- **Constitution Matching**: Embedding-based similarity with multiple constitutions
- **Multi-Model Generative Analysis**: Claude 3.5 Sonnet + Llama 3.1 fallback
- **Comprehensive Legal Analysis**: Offensive/Defensive perspectives + Risk Assessment
- **Performance Optimization**: Intelligent caching for embeddings and API responses
- **Conversational AI**: Multi-turn chat with document context awareness

### Supported Constitutions
- India (COI.json)
- China (China_2018.json)
- Japan (Japan_1946.json)
- Russia (Russia_2014.json)

## 🎨 **Frontend Design**

- **Theme**: Black + Green inspired by trae.in
- **Framework**: Next.js 14 with TypeScript
- **Styling**: TailwindCSS with shadcn/ui components
- **State Management**: React hooks with SWR for API calls

## 📊 **API Endpoints**

### Document Analysis
- `POST /api/upload` - Upload and analyze documents
- `GET /api/analysis/{document_id}` - Get analysis results

### Chatbot Interface
- `POST /api/chatbot/session/create` - Create chat session
- `POST /api/chatbot/message` - Send message
- `POST /api/chatbot/analyze-clause` - Contextual clause analysis

### Health & Monitoring
- `GET /api/health` - System health check
- `GET /health` - Basic health endpoint

## 🔧 **Environment Configuration**

Backend `.env` file:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 📈 **Performance Features**

- **Embedding Caching**: Constitution embeddings cached for faster matching
- **API Response Caching**: Generative AI responses cached with 24-hour TTL
- **Batch Processing**: Optimized batch sizes for embedding generation
- **Fallback Mechanisms**: Graceful degradation when services unavailable

## 🛡️ **Security & Reliability**

- **API Key Validation**: Secure OpenRouter API key handling
- **Error Handling**: Comprehensive error recovery and logging
- **Graceful Fallbacks**: Multiple AI models and service levels
- **Input Validation**: Secure file upload and processing

## 📝 **Development Status**

✅ **Completed Features**
- [x] Multi-model generative AI service
- [x] Constitution-aware semantic matching
- [x] Performance optimization with caching
- [x] Chatbot infrastructure
- [x] Comprehensive legal analysis
- [x] Production-ready repository structure

## 🚀 **Deployment**

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment
```bash
cd frontend
npm run build
npm start
```

## 📄 **License**

This project is proprietary and confidential.

## 🤝 **Support**

For technical support and documentation, refer to the individual component documentation files in the backend directory.
- **Constitution Context**: Support for multiple legal frameworks
- **Risk Assessment**: Priority scoring and color-coded risk levels
- **Modern UI**: Next.js frontend with Tailwind CSS

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- Tesseract OCR (for image text extraction)

## 🛠️ Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file and add your API key:
```
CLAUDE_SONNET_3_API_KEY=your_claude_sonnet_3_api_key_here
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to root directory:
```bash
cd ..
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the frontend server:
```bash
npm run dev
```

## 🔧 Environment Variables

### Required
- `CLAUDE_SONNET_3_API_KEY`: Claude 3.5 Sonnet API key from OpenRouter

### Optional
- `OPENROUTER_API_KEY`: Alternative API key (legacy support)
- `UPLOAD_DIR`: Custom upload directory (default: ./uploads)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 52428800)

## 🌐 Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Supported File Formats

| Format | Extension | OCR Support | Status |
|--------|------------|-------------|---------|
| Text | .txt | N/A | ✅ |
| PDF | .pdf | N/A | ✅ |
| PowerPoint | .ppt, .pptx | N/A | ✅ |
| JPEG | .jpg, .jpeg | ✅ | ✅ |
| PNG | .png | ✅ | ✅ |
| Word | .docx, .doc | N/A | ✅ |

## 🤖 AI Pipeline

1. **Text Extraction**: Format-specific extraction with OCR fallback
2. **Clause Detection**: Pattern-based clause identification
3. **Semantic Classification**: sentence-transformers embeddings
4. **Priority Ranking**: Importance scoring algorithm
5. **Legal Explanation**: Claude 3.5 Sonnet analysis
6. **Response Standardization**: Structured JSON output

## 📊 API Response Structure

```json
{
  "status": "success",
  "filename": "document.pdf",
  "document_stats": {
    "total_characters": 1245,
    "total_clauses": 5,
    "classified_clauses": 5,
    "ranked_clauses": 5
  },
  "clauses": [
    {
      "clause_id": "clause_001",
      "text": "Clause text...",
      "type": "payment",
      "confidence": 0.848,
      "priority_score": 0.6,
      "color": "yellow",
      "rank": 1,
      "explanation": "AI explanation..."
    }
  ],
  "summary": {
    "high_priority_count": 1,
    "medium_priority_count": 3,
    "low_priority_count": 1,
    "clause_types": ["payment", "liability", "termination"]
  }
}
```

## 🧪 Testing

Run the integration tests:

```bash
# Test complete integration
python test_complete_integration.py

# Test OCR functionality
python test_ocr_integration.py

# Test API directly
python test_claude_direct.py
```

## 🔍 Troubleshooting

### Common Issues

1. **"File type not allowed" error**
   - Check file extension in `ALLOWED_EXT` in `routes/upload.py`
   - Ensure file extension is lowercase

2. **"No text could be extracted" error**
   - Install Tesseract OCR for image processing
   - Check if file is corrupted or password-protected

3. **Claude API not working**
   - Verify `CLAUDE_SONNET_3_API_KEY` is set correctly
   - Check OpenRouter API key validity

4. **Dependencies missing**
   - Run `pip install -r requirements.txt`
   - Install Tesseract OCR system-wide

### OCR Setup

**Windows:**
```bash
# Install Tesseract
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH and set TESSDATA_PREFIX
```

**macOS:**
```bash
brew install tesseract
```

**Ubuntu:**
```bash
sudo apt-get install tesseract-ocr
```

## 📝 Development

### Project Structure
```
lexai-legal-document-analysis/
├── backend/
│   ├── ai/
│   │   └── generative_service.py
│   ├── routes/
│   │   └── upload.py
│   ├── services/
│   │   └── document_analysis_service.py
│   ├── document_processor.py
│   ├── main.py
│   └── requirements.txt
├── components/
│   └── upload-content.tsx
├── lib/
│   ├── api.ts
│   └── types.ts
├── public/
│   └── icons/
├── app/
├── package.json
└── README.md
```

### Adding New File Types

1. Add extension to `ALLOWED_EXT` in `routes/upload.py`
2. Add extraction method to `document_processor.py`
3. Update `supported_formats` in DocumentProcessor class
4. Add MIME type to frontend validation

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the API documentation
- Create an issue with detailed information
│   ├── clause_extractor.py     # Extract clauses from legal documents
│   ├── clause_classifier.py    # Classify clauses by type
│   ├── clause_ranker.py        # Rank clauses by importance/relevance
│   ├── document_processor.py   # Main document processing pipeline
│   ├── models.py               # Data models for legal entities
│   ├── database.py             # Database operations
│   ├── config.py               # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── routes/                 # API endpoints
│   │   ├── summarize.py
│   │   ├── qa.py
│   │   ├── upload.py
│   │   └── health.py
│   └── services/               # Core services
│       ├── ai_pipeline.py
│       ├── embeddings.py
│       ├── parser.py
│       ├── pdf_generator.py
│       └── preprocessing.py
└── frontend/
    ├── pages/                  # Frontend pages
    ├── components/             # Reusable components
    └── styles/                 # CSS/styling files
```

## Features

- **Document Processing**: Extract and process legal documents from various formats (PDF, DOCX, TXT)
- **Clause Extraction**: AI-powered extraction of key legal clauses
- **Clause Classification**: Automatic classification of clauses (obligations, rights, prohibitions, etc.)
- **Clause Ranking**: Rank clauses by importance and relevance to queries
- **Question Answering**: Answer questions about legal documents using AI
- **Summarization**: Generate concise summaries of legal documents
- **Entity Recognition**: Extract legal entities using NLP

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the application:
   ```bash
   # For development (minimal dependencies)
   python run_server.py
   
   # Or with uvicorn directly
   uvicorn main_minimal:app --reload --host 0.0.0.0 --port 8000
   
   # For full functionality (requires all dependencies)
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will start on `http://localhost:8000`

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/upload` - Upload and process documents  
- `POST /api/summarize` - Generate document summaries
- `POST /api/qa` - Ask questions about documents
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Usage

### Upload a Document
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8000/api/upload
```

### Summarize Text
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"document_text": "Your legal text here..."}' \
  http://localhost:8000/api/summarize
```

### Ask Questions
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "What are the main obligations in this contract?"}' \
  http://localhost:8000/api/qa
```

## Development

The application is structured with separation of concerns:

- **Routes**: Handle HTTP requests and responses
- **Services**: Core business logic and AI processing
- **Models**: Data structures and database operations
- **Utils**: Helper functions and utilities

## Dependencies

- FastAPI: Modern web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- OpenAI: AI processing
- Sentence Transformers: Text embeddings
- FAISS: Vector search
- spaCy: Natural language processing
- textract: Document text extraction
- ReportLab: PDF generation

## License

[Add your license information here]
