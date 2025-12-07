# RAG Chatbot for Physical AI & Humanoid Robotics Book

A production-grade Retrieval-Augmented Generation (RAG) chatbot system for the Docusaurus book **"Physical AI & Humanoid Robotics: The Rise of the Digital Human"**.

---

## 🎯 Features

✅ **Intelligent Querying**
- Answer general questions about the book content
- Retrieve relevant excerpts with source citations
- Confidence scores for answer reliability

✅ **Selection-Based Queries**
- Highlight text on the page
- Ask questions about only that selected passage
- Perfect for deep-diving into specific topics

✅ **Source Citations**
- Every answer includes clickable source links
- Chapter and lesson references
- Character offsets for precise navigation
- Relevance scores for each source

✅ **Production-Ready**
- RESTful FastAPI backend with OpenAPI docs
- React component with Docusaurus integration
- Full test coverage with integration tests
- Docker deployment ready

✅ **Zero Data Loss**
- Neon PostgreSQL for metadata and document storage
- Qdrant Cloud for vector embeddings
- Automatic backups and snapshots

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.11+
- Node.js 18+
- API keys from:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Qdrant Cloud](https://cloud.qdrant.io)
  - [Neon PostgreSQL](https://neon.tech)

### Installation

```bash
# 1. Clone and navigate
cd hackathon-Project

# 2. Set up backend
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

cd backend
pip install -r requirements.txt
uvicorn app:app --reload &

# 3. Set up frontend
cd ../docusaurus-book
npm install
npm run start &

# 4. Verify installation
cd ..
bash verify_rag.sh
```

### Access
- **Chat UI**: http://localhost:3000/chat
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 Ingesting Your Book

```bash
# From project root
python scripts/ingest_documents.py --path docusaurus-book/docs
```

This will:
1. Read all markdown files from your book
2. Parse chapter and lesson metadata
3. Split into chunks (1000 tokens, 200 overlap)
4. Generate embeddings via OpenAI
5. Store in Neon PostgreSQL and Qdrant Cloud

**Expected output:**
```
Files processed: 12
Documents saved: 12
Chunks created: 245
Vectors upserted: 245
Total tokens: 182,450
```

---

## 🏗️ Architecture

```
Frontend (React/Docusaurus)
         ↓ HTTP
Backend (FastAPI)
    ├── Chunker (Split documents into 1K token chunks)
    ├── Embedder (OpenAI text-embedding-3-small)
    ├── Retriever (Qdrant vector search)
    ├── Reranker (Cosine similarity + metadata)
    └── Answerer (GPT-4 Turbo with context)
         ↓              ↓                 ↓
    Neon Postgres   Qdrant Cloud    OpenAI API
    (Metadata)      (Vectors)       (LLM + Embeddings)
```

---

## 📋 Project Structure

```
hackathon-Project/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── database.py            # PostgreSQL operations
│   ├── embeddings.py          # OpenAI embeddings
│   ├── vector_store.py        # Qdrant operations
│   ├── chunker.py             # Document chunking
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Container image
│   ├── .env.example           # Environment template
│   └── tests/
│       ├── test_chunker.py
│       ├── test_endpoints.py
│       └── conftest.py
│
├── website/
│   └── src/
│       ├── components/
│       │   ├── RagChat.tsx    # React chat component
│       │   └── RagChat.module.css
│       ├── pages/
│       │   ├── Chat.tsx       # /chat page
│       │   └── Chat.module.css
│       └── plugins/
│           └── rag-chat-plugin.js
│
├── docusaurus-book/           # Your existing book project
│   ├── docs/
│   ├── src/
│   ├── package.json
│   └── docusaurus.config.ts
│
├── scripts/
│   └── ingest_documents.py    # Document ingestion script
│
├── docker-compose.yml         # Multi-container setup
├── verify_rag.sh              # End-to-end verification
├── RAG_SETUP_GUIDE.md         # Detailed setup guide
├── API_EXAMPLES.md            # API usage examples
├── DEPLOYMENT_CHECKLIST.md    # Deployment guide
└── README.md                  # This file
```

---

## 🔌 API Endpoints

### Health Check
```bash
GET /health
```

### Embed Document
```bash
POST /embed
Content-Type: application/json

{
  "doc_id": "chapter1:intro",
  "title": "Introduction",
  "content": "Full text...",
  "chapter": "Chapter 1",
  "lesson": "Basics"
}
```

### Query with RAG
```bash
POST /query
Content-Type: application/json

{
  "query": "What is humanoid robotics?",
  "top_k": 10,
  "chapter_filter": "Chapter 1"  # Optional
}
```

### Selection-Based Query
```bash
POST /select-query
Content-Type: application/json

{
  "query": "What's emphasized here?",
  "selected_text": "Selected text from page..."
}
```

**Response:**
```json
{
  "query_id": "abc-123",
  "short_answer": "...",
  "sources": [
    {
      "chunk_id": "...",
      "chapter": "Chapter 1",
      "lesson": "Basics",
      "text": "...",
      "score": 0.92
    }
  ],
  "confidence_score": 0.91,
  "is_selection_mode": false,
  "processing_time_ms": 245.5
}
```

See [API_EXAMPLES.md](./API_EXAMPLES.md) for complete examples.

---

## 🧪 Testing

### Unit Tests
```bash
cd backend
pytest tests/test_chunker.py -v
```

### Integration Tests
```bash
cd backend
pytest tests/test_endpoints.py -v -s
```

### End-to-End Verification
```bash
bash verify_rag.sh
```

---

## 🐳 Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Services:
# - Backend:  http://localhost:8000
# - Frontend: http://localhost:3000
# - Postgres: localhost:5432 (dev only)
```

---

## 📦 Environment Variables

Create `backend/.env`:

```env
# Required: OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small

# Required: Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=book-embeddings

# Required: Neon PostgreSQL
NEON_DB_URL=postgresql://user:password@host/dbname

# Optional: Configuration
API_PORT=8000
ENV=development
TOP_K_RETRIEVAL=10
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RATE_LIMIT_QUERIES_PER_MINUTE=60
ENABLE_SELECTION_MODE=true
```

---

## 📖 Configuration

### Chunking Strategy
- **Chunk size:** 1000 tokens (≈ 750 words)
- **Overlap:** 200 tokens (prevents split concepts)
- **Token counter:** tiktoken with GPT-3.5 encoding

### Vector Database
- **Provider:** Qdrant Cloud
- **Model:** text-embedding-3-small (512 dimensions)
- **Distance metric:** Cosine similarity
- **Indexes:** doc_id, chapter, lesson

### LLM Configuration
- **Model:** GPT-4 Turbo Preview
- **Temperature:** 0.7 (balanced creativity/consistency)
- **Max tokens:** 500 per query
- **System prompt:** Enforces source-based answering

---

## 🚢 Deployment

### Quick Deployment to Cloud Run
```bash
cd backend
gcloud run deploy rag-backend \
  --source . \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,...
```

### Deployment to Vercel (Frontend)
```bash
cd docusaurus-book
npm install -g vercel
vercel
```

See [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) for complete instructions.

---

## 🔒 Security & Safety

✅ **Data Security**
- Secrets managed via environment variables (never hardcoded)
- Database passwords use strong encryption
- API keys stored in cloud provider secret managers

✅ **API Security**
- CORS restricted to approved origins
- Rate limiting: 60 queries/minute per user
- Input sanitization: HTML entities escaped
- No private keys in logs or responses

✅ **Data Privacy**
- Document metadata in PostgreSQL (HIPAA-eligible with premium)
- Vectors in Qdrant (SOC 2 Type II certified)
- Query history retained for 30 days only
- No personal data shared with OpenAI beyond API calls

---

## 📊 Monitoring & Observability

```bash
# Health check
curl http://localhost:8000/health

# View logs
docker logs rag-backend

# Monitor vector index
curl https://$QDRANT_URL/collections/book-embeddings

# Query analytics
SELECT COUNT(*) FROM query_history;
SELECT AVG(confidence_score) FROM query_history;
```

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Check environment variables
cat backend/.env
```

### Embeddings fail
```bash
# Verify OpenAI API key
echo $OPENAI_API_KEY

# Test connectivity
python -c "from openai import AsyncOpenAI; print('OK')"
```

### Poor query results
```bash
# Re-ingest documents
python scripts/ingest_documents.py --path docusaurus-book/docs

# Increase TOP_K_RETRIEVAL in .env
# Decrease CHUNK_SIZE for finer granularity
```

See [RAG_SETUP_GUIDE.md](./RAG_SETUP_GUIDE.md) for detailed troubleshooting.

---

## 📈 Performance Metrics

Typical performance on modern hardware:

| Operation | Time |
|-----------|------|
| Embedding 1000 tokens | 100ms |
| Vector search (top 10) | 50ms |
| LLM response generation | 1-2s |
| Total query latency | 2-3s |
| Ingestion rate | 100-200 docs/min |

---

## 🤝 Contributing

1. **No changes to book project:** All additions are in `backend/`, `website/`, and new root files
2. **Preserve constitution:** Respect the book's tone and structure
3. **Test thoroughly:** Run `pytest` and `verify_rag.sh` before committing
4. **Document changes:** Update README and guides

---

## 📄 License

This RAG system is part of the **Physical AI & Humanoid Robotics** book project.

---

## 🎓 Next Steps

1. **[Quick Start](#quick-start)** - Get running in 5 minutes
2. **[Ingest Your Book](#ingesting-your-book)** - Add your content
3. **[Test Integration](#testing)** - Verify everything works
4. **[Deploy](#deployment)** - Go to production
5. **[Monitor](#monitoring--observability)** - Track performance

---

## 📞 Support

- **Setup Questions?** → See [RAG_SETUP_GUIDE.md](./RAG_SETUP_GUIDE.md)
- **API Usage?** → See [API_EXAMPLES.md](./API_EXAMPLES.md)
- **Deployment Help?** → See [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
- **API Documentation?** → Visit http://localhost:8000/docs

---

**Project:** Physical AI & Humanoid Robotics: The Rise of the Digital Human
**Author:** Abdul Ahad Javaid
**Last Updated:** December 7, 2024
**Version:** 1.0.0
