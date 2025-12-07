# RAG Chatbot Setup & Deployment Guide

**Book:** Physical AI & Humanoid Robotics: The Rise of the Digital Human

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Local Development Setup](#local-development-setup)
5. [Environment Configuration](#environment-configuration)
6. [Document Ingestion](#document-ingestion)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)

---

## Quick Start

**Fastest path to a working RAG chatbot (5 minutes):**

```bash
# 1. Clone and navigate to project
cd hackathon-Project

# 2. Set up environment
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 3. Start backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

# 4. In another terminal, start frontend
cd docusaurus-book
npm install
npm run start

# 5. In a third terminal, run verification
bash verify_rag.sh

# 6. Open http://localhost:3000/chat
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Docusaurus Frontend                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  /chat Route (React Component)                       │  │
│  │  - Chat UI                                           │  │
│  │  - Text selection for targeted queries               │  │
│  │  - Source citations with links                       │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │  /embed       - Ingest & chunk documents           │    │
│  │  /query       - RAG query with LLM answering        │    │
│  │  /select-query - Query restricted to selection      │    │
│  │  /health      - Service health status               │    │
│  └────────────────────────────────────────────────────┘    │
│              │              │              │                 │
│              ▼              ▼              ▼                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Chunker &    │  │ Embeddings   │  │ LLM Agent    │      │
│  │ Metadata     │  │ (OpenAI)     │  │ (ChatKit)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
        │                    │                   │
        ▼                    ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Neon Postgres│    │ Qdrant Cloud │    │  OpenAI API  │
│ - Documents  │    │ - Vectors    │    │ - Embeddings │
│ - Chunks     │    │ - Similarity │    │ - LLM Answers│
│ - Metadata   │    │   Search     │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## Prerequisites

### Required Services (Free Tier Options)

1. **OpenAI API**: https://platform.openai.com/api-keys
   - Model: gpt-4-turbo-preview or gpt-4
   - Embeddings: text-embedding-3-small
   - Budget: ~$0.001 per query (varies)

2. **Qdrant Cloud**: https://cloud.qdrant.io
   - Free tier: 1 cluster, 5GB storage
   - Collection name: `book-embeddings`

3. **Neon PostgreSQL**: https://neon.tech
   - Free tier: 0.5GB storage, 3 GB/month
   - Database name: `rag_chatbot`

### Local Requirements

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional, for containerized setup)
- Git

---

## Local Development Setup

### Step 1: Clone Repository

```bash
cd hackathon-Project
git checkout 004-module4-vla  # Current branch
```

### Step 2: Create Environment File

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small

# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=book-embeddings

# Neon PostgreSQL Configuration
NEON_DB_URL=postgresql://user:password@ep-xxxx.us-east-1.neon.tech/rag_chatbot

# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENV=development
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# RAG Configuration
TOP_K_RETRIEVAL=10
RERANKER_TOP_K=5
MAX_TOKENS_PER_QUERY=4000
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Security
RATE_LIMIT_QUERIES_PER_MINUTE=60
ENABLE_SELECTION_MODE=true
```

### Step 3: Install Backend Dependencies

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 4: Start Backend

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Output should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 5: Install Frontend Dependencies

```bash
cd docusaurus-book
npm install
```

### Step 6: Start Frontend

```bash
cd docusaurus-book
npm run start
```

Output should show:
```
[INFO] Starting dev server...
[SUCCESS] Docusaurus server started on: http://localhost:3000
```

### Step 7: Verify Installation

```bash
# In a new terminal, from project root
bash verify_rag.sh
```

Expected output:
```
✓ Health endpoint responds
✓ Embedding successful (created X chunks)
✓ Query successful
✓ Selection query successful
✓ OpenAPI schema available

VERIFICATION SUMMARY
Passed: 5
Failed: 0
```

---

## Environment Configuration

### OpenAI Setup

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy to `.env` file as `OPENAI_API_KEY`

**Cost Estimation:**
- Embeddings: ~$0.00002 per 1K tokens
- GPT-4 Turbo: ~$0.01 per 1K input tokens, $0.03 per 1K output tokens
- Average query: ~$0.02

### Qdrant Cloud Setup

1. Go to https://cloud.qdrant.io
2. Create a free account
3. Create a cluster (select region close to you)
4. In cluster dashboard:
   - Copy cluster URL → `QDRANT_URL`
   - Generate API key → `QDRANT_API_KEY`

### Neon PostgreSQL Setup

1. Go to https://neon.tech
2. Create an account
3. Create a new project
4. Create a database named `rag_chatbot`
5. Copy connection string → `NEON_DB_URL`

Format: `postgresql://[user]:[password]@[host]/[database]`

---

## Document Ingestion

### Ingesting Book Documents

```bash
# From project root
python scripts/ingest_documents.py --path docusaurus-book/docs
```

This will:
1. Read all `.md` files from the docs directory
2. Parse frontmatter (title, chapter, lesson)
3. Chunk text (1000 tokens, 200 overlap)
4. Generate embeddings via OpenAI
5. Store in Neon PostgreSQL and Qdrant Cloud

**Output:**
```
Ingestion Complete
======================================================================
Files processed: 12
Documents saved: 12
Chunks created: 245
Vectors upserted: 245
Total tokens: 182,450
```

### Ingesting Sample Documents

For testing without your full book:

```bash
python scripts/ingest_documents.py --sample
```

This creates 2 sample documents for testing the full pipeline.

### Ingestion Script Options

```bash
# Ingest specific directory
python scripts/ingest_documents.py --path /path/to/docs

# Ingest samples only
python scripts/ingest_documents.py --sample

# Check ingestion stats
# Automatically printed as JSON_STATS
```

---

## Testing

### Run Unit Tests

```bash
cd backend
pytest tests/test_chunker.py -v
```

### Run Integration Tests

```bash
cd backend
pytest tests/test_endpoints.py -v -s
```

Requires:
- Backend running on http://localhost:8000
- Neon database configured
- Qdrant accessible

### Run End-to-End Verification

```bash
bash verify_rag.sh
```

Tests:
1. Health check
2. Document embedding
3. RAG query
4. Selection-based query
5. OpenAPI documentation

---

## Deployment

### Option 1: Docker Compose (Local)

```bash
# Create .env file
cp backend/.env.example .env

# Edit .env with your API keys

# Start all services
docker-compose up --build

# Services:
# Backend:  http://localhost:8000
# Frontend: http://localhost:3000
# Postgres: localhost:5432 (local development only)
```

### Option 2: Production Deployment

#### Backend (FastAPI on Cloud Run, Heroku, or DigitalOcean)

**Google Cloud Run:**

```bash
# Build image
docker build -t gcr.io/PROJECT_ID/rag-backend:latest ./backend
docker push gcr.io/PROJECT_ID/rag-backend:latest

# Deploy
gcloud run deploy rag-backend \
  --image gcr.io/PROJECT_ID/rag-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,QDRANT_URL=$QDRANT_URL,QDRANT_API_KEY=$QDRANT_API_KEY,NEON_DB_URL=$NEON_DB_URL
```

#### Frontend (Docusaurus on Vercel or Netlify)

**Vercel:**

```bash
cd docusaurus-book
npm install -g vercel
vercel
```

**Netlify:**

```bash
cd docusaurus-book
npm run build
# Deploy build/ folder to Netlify
```

### Pre-Deployment Checklist

- [ ] All tests pass locally
- [ ] `.env` file configured with production keys
- [ ] CORS origins updated for production domain
- [ ] Database backups configured
- [ ] API rate limiting enabled
- [ ] Error logging configured (Sentry, DataDog, etc.)
- [ ] CDN configured for static assets
- [ ] SSL/TLS certificates installed
- [ ] Monitoring and alerting set up

---

## Troubleshooting

### Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

**Error:** `Connection refused` to Neon/Qdrant

```bash
# Solution: Check environment variables
cat backend/.env

# Check connectivity
curl https://<QDRANT_URL>/health
```

### Embedding Fails

**Error:** `401 Unauthorized` from OpenAI

```bash
# Solution: Verify API key
echo $OPENAI_API_KEY  # Should not be empty
# Get new key from https://platform.openai.com/api-keys
```

### Queries Return Poor Results

1. Check embedding quality:
   ```bash
   python -c "from embeddings import get_embedding_manager; import asyncio; asyncio.run(get_embedding_manager().embed_text('test'))"
   ```

2. Verify document ingestion:
   ```bash
   # Check Neon
   SELECT COUNT(*) FROM documents;
   SELECT COUNT(*) FROM chunks;
   ```

3. Re-ingest documents:
   ```bash
   python scripts/ingest_documents.py --path docusaurus-book/docs
   ```

### Frontend Can't Connect to Backend

**Check CORS:**

```bash
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS http://localhost:8000/query -v
```

Update `CORS_ORIGINS` in backend `.env` if needed.

---

## API Reference

### Base URL
```
http://localhost:8000
```

### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": true,
  "vector_store": true,
  "embeddings": true
}
```

### 2. Embed Document

```http
POST /embed
```

**Request:**
```json
{
  "doc_id": "module1:intro",
  "title": "Introduction to Humanoid Robotics",
  "content": "Full text content...",
  "chapter": "Module 1",
  "lesson": "Fundamentals",
  "source_url": "https://example.com",
  "metadata": {
    "author": "Abdul Ahad",
    "version": "1.0"
  }
}
```

**Response:**
```json
{
  "doc_id": "module1:intro",
  "chunks_created": 15,
  "vectors_upserted": 15,
  "total_tokens": 12450
}
```

### 3. RAG Query

```http
POST /query
```

**Request:**
```json
{
  "query": "What is humanoid robotics?",
  "user_id": "user123",
  "doc_id_filter": null,
  "chapter_filter": "Module 1",
  "lesson_filter": null,
  "top_k": 10
}
```

**Response:**
```json
{
  "query_id": "abc-123-def",
  "short_answer": "Humanoid robotics is the field of building robots that mimic human form and movement...",
  "long_answer": "Extended explanation...",
  "sources": [
    {
      "chunk_id": "module1:intro:chunk:0",
      "doc_id": "module1:intro",
      "chapter": "Module 1",
      "lesson": "Fundamentals",
      "text": "Humanoid robots are designed to...",
      "start_char": 100,
      "end_char": 250,
      "score": 0.92
    }
  ],
  "confidence_score": 0.91,
  "is_selection_mode": false,
  "processing_time_ms": 245.5,
  "model_used": "gpt-4-turbo-preview"
}
```

### 4. Selection Query

```http
POST /select-query
```

**Request:**
```json
{
  "query": "What aspect is highlighted?",
  "selected_text": "Humanoid robots can perform complex manipulation tasks.",
  "user_id": "user123",
  "doc_id": "module1:basics"
}
```

**Response:**
```json
{
  "query_id": "xyz-456-abc",
  "short_answer": "The highlighted aspect is that humanoid robots possess the capability to perform complex manipulation tasks.",
  "sources": [
    {
      "chunk_id": "selection",
      "doc_id": "module1:basics",
      "text": "Humanoid robots can perform complex manipulation tasks.",
      "score": 1.0
    }
  ],
  "confidence_score": 0.95,
  "is_selection_mode": true,
  "processing_time_ms": 180.2,
  "model_used": "gpt-4-turbo-preview"
}
```

### 5. OpenAPI Documentation

```http
GET /openapi.json
GET /docs         (Interactive Swagger UI)
GET /redoc        (ReDoc documentation)
```

---

## Security & Safety

### API Security

1. **Rate Limiting:** 60 queries/minute per user
2. **CORS:** Restricted to configured origins only
3. **Input Sanitization:** HTML entities escaped in responses
4. **No Secret Leakage:** API keys never logged or returned

### Secrets Management

```bash
# .env file should NEVER be committed
echo ".env" >> .gitignore

# For CI/CD, use environment secrets:
# GitHub: Settings > Secrets & variables
# Vercel: Project settings > Environment variables
# Heroku: Config Vars
```

### Data Privacy

- Documents stored in Neon (HIPAA-eligible with premium)
- Vectors stored in Qdrant (SOC 2 Type II certified)
- Query history kept for 30 days, then deleted
- User data not shared with OpenAI beyond API calls

---

## Maintenance

### Database Backups

**Neon:**
- Automatic daily backups (7-day retention free tier)
- Manual backup: https://neon.tech/docs/manage/backups

**Qdrant:**
- Snapshots: API endpoint `/snapshots`
- Export collection: `qdrant-client` Python library

### Monitoring

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Logs:**
```bash
# Docker
docker logs rag-backend

# Local
# Check stdout of uvicorn server
```

### Performance Optimization

1. **Increase `TOP_K_RETRIEVAL`** if results are poor
2. **Decrease `CHUNK_SIZE`** for more granular results
3. **Add payload indexes** in Qdrant for frequently filtered fields
4. **Cache embeddings** for repeated queries
5. **Use CDN** for frontend assets

---

## Support & Contribution

For issues, questions, or contributions:

1. Check this guide and troubleshooting section
2. Review OpenAPI docs at http://localhost:8000/docs
3. Check backend logs for detailed error messages
4. For book content issues, refer to project constitution in `.specify/memory/book-constitution.md`

---

**Last Updated:** December 7, 2024
**Maintained By:** Abdul Ahad Javaid
**Project:** Physical AI & Humanoid Robotics RAG Chatbot
