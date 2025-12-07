# RAG API Examples

Quick reference with curl commands for all endpoints.

---

## Setup

```bash
# Ensure backend is running
cd backend
uvicorn app:app --reload

# In another terminal, export base URL
export API_URL="http://localhost:8000"
```

---

## 1. Health Check

Check if all services are operational.

```bash
curl $API_URL/health | jq
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": true,
  "vector_store": true,
  "embeddings": true
}
```

---

## 2. Embed a Document

Ingest and embed a document for RAG.

```bash
curl -X POST $API_URL/embed \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "module1:robotics",
    "title": "Introduction to Humanoid Robotics",
    "content": "Humanoid robots are designed to interact with human environments. They combine advanced sensors, actuators, and AI algorithms. Modern humanoid robots can perform complex manipulation tasks. They use vision and language models to understand instructions. Safety is paramount in robotics, as robots work alongside humans. The integration of large language models with robotics has opened new possibilities for natural human-robot interaction.",
    "chapter": "Module 1",
    "lesson": "Robotics Basics",
    "source_url": "https://yourdomain.com/docs/module1",
    "metadata": {
      "author": "Abdul Ahad",
      "version": "1.0",
      "created": "2024-12-07"
    }
  }' | jq
```

**Response:**
```json
{
  "doc_id": "module1:robotics",
  "chunks_created": 2,
  "vectors_upserted": 2,
  "total_tokens": 145
}
```

---

## 3. Query with RAG

Ask a question about the ingested documents.

### Basic Query

```bash
curl -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are humanoid robots used for?"
  }' | jq
```

### Query with Filters

```bash
curl -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "chapter_filter": "Module 1",
    "lesson_filter": "Robotics Basics",
    "top_k": 5
  }' | jq
```

### Query with User Tracking

```bash
curl -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do robots perceive their environment?",
    "user_id": "user@example.com",
    "top_k": 10
  }' | jq
```

**Response:**
```json
{
  "query_id": "abc-123-def-456",
  "short_answer": "Humanoid robots perceive their environment primarily through vision sensors, which process visual information from cameras. They use advanced computer vision algorithms combined with language models to understand spatial relationships and follow instructions.",
  "long_answer": "Extended explanation with more detail...",
  "sources": [
    {
      "chunk_id": "module1:robotics:chunk:0",
      "doc_id": "module1:robotics",
      "chapter": "Module 1",
      "lesson": "Robotics Basics",
      "text": "Humanoid robots are designed to interact with human environments...",
      "start_char": 0,
      "end_char": 85,
      "score": 0.94
    }
  ],
  "confidence_score": 0.92,
  "is_selection_mode": false,
  "processing_time_ms": 523.45,
  "model_used": "gpt-4-turbo-preview"
}
```

---

## 4. Selection-Based Query

Query restricted to user-selected text.

```bash
curl -X POST $API_URL/select-query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What aspect is emphasized?",
    "selected_text": "Safety is paramount in robotics, as robots work alongside humans.",
    "user_id": "user@example.com",
    "doc_id": "module1:robotics"
  }' | jq
```

**Response:**
```json
{
  "query_id": "xyz-789-abc-123",
  "short_answer": "The emphasized aspect is that safety is crucial in robotics because robots work directly with humans in shared environments.",
  "long_answer": null,
  "sources": [
    {
      "chunk_id": "selection",
      "doc_id": "module1:robotics",
      "chapter": null,
      "lesson": null,
      "text": "Safety is paramount in robotics, as robots work alongside humans.",
      "start_char": 0,
      "end_char": 65,
      "score": 1.0
    }
  ],
  "confidence_score": 0.95,
  "is_selection_mode": true,
  "processing_time_ms": 245.67,
  "model_used": "gpt-4-turbo-preview"
}
```

---

## 5. Batch Document Ingestion

Ingest multiple documents in sequence.

```bash
#!/bin/bash

DOCS=(
  '{"doc_id":"m1:intro","title":"Introduction","content":"Intro text...","chapter":"M1"}'
  '{"doc_id":"m1:basics","title":"Basics","content":"Basics text...","chapter":"M1"}'
  '{"doc_id":"m2:advanced","title":"Advanced","content":"Advanced text...","chapter":"M2"}'
)

for doc in "${DOCS[@]}"; do
  echo "Ingesting: $doc"
  curl -X POST $API_URL/embed \
    -H "Content-Type: application/json" \
    -d "$doc" | jq '.doc_id'
  sleep 1
done

echo "Batch ingestion complete"
```

---

## 6. Query with Different Top-K Values

Compare results with different retrieval counts.

```bash
# Get top 3 results
curl -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Tell me about robotics",
    "top_k": 3
  }' | jq '.sources | length'

# Get top 10 results
curl -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Tell me about robotics",
    "top_k": 10
  }' | jq '.sources | length'
```

---

## 7. Error Handling Examples

### Missing Required Field

```bash
curl -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Service Unavailable

```bash
curl $API_URL/health
```

**Response (503 if services not ready):**
```json
{
  "status": "degraded",
  "database": false,
  "vector_store": true,
  "embeddings": true
}
```

---

## 8. OpenAPI Documentation

Get the OpenAPI schema programmatically.

```bash
# Download OpenAPI schema
curl $API_URL/openapi.json > openapi.json

# View in Swagger UI
open $API_URL/docs

# View in ReDoc
open $API_URL/redoc
```

---

## 9. Performance Testing

### Simple Load Test (bash)

```bash
#!/bin/bash

echo "Running 100 queries..."
start=$(date +%s%N)

for i in {1..100}; do
  curl -s -X POST $API_URL/query \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"Query number $i\"}" > /dev/null
  echo -ne "\rProgress: $i/100"
done

end=$(date +%s%N)
total_time=$(( (end - start) / 1000000 ))
avg_time=$(( total_time / 100 ))

echo ""
echo "Total time: ${total_time}ms"
echo "Average per query: ${avg_time}ms"
```

### Load Test with Apache Bench

```bash
# 100 requests, 10 concurrent
ab -n 100 -c 10 -p query.json -T application/json \
  http://localhost:8000/query
```

---

## 10. Data Export Examples

### Export Query History

```bash
# Get recent queries (requires database access)
psql $NEON_DB_URL -c \
  "SELECT query_id, query_text, confidence_score, created_at
   FROM query_history
   ORDER BY created_at DESC
   LIMIT 100;"
```

### Export Ingested Documents

```bash
psql $NEON_DB_URL -c \
  "SELECT doc_id, title, chapter, lesson, created_at
   FROM documents
   ORDER BY created_at DESC;"
```

### Export Chunks for Analysis

```bash
psql $NEON_DB_URL -c \
  "SELECT chunk_id, doc_id, tokens, LENGTH(text) as text_length
   FROM chunks
   LIMIT 50;"
```

---

## 11. Python Client Examples

```python
import requests
import json

BASE_URL = "http://localhost:8000"

class RAGClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def health(self):
        """Check service health."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

    def embed(self, doc_id, title, content, chapter=None, lesson=None):
        """Embed a document."""
        payload = {
            "doc_id": doc_id,
            "title": title,
            "content": content,
            "chapter": chapter,
            "lesson": lesson
        }
        response = requests.post(
            f"{self.base_url}/embed",
            json=payload
        )
        return response.json()

    def query(self, query_text, top_k=10):
        """Execute a RAG query."""
        payload = {"query": query_text, "top_k": top_k}
        response = requests.post(
            f"{self.base_url}/query",
            json=payload
        )
        return response.json()

    def select_query(self, query_text, selected_text):
        """Execute a selection-based query."""
        payload = {
            "query": query_text,
            "selected_text": selected_text
        }
        response = requests.post(
            f"{self.base_url}/select-query",
            json=payload
        )
        return response.json()

# Usage
client = RAGClient(BASE_URL)

# Check health
print(client.health())

# Embed a document
result = client.embed(
    doc_id="test:1",
    title="Test Document",
    content="This is test content...",
    chapter="Test Chapter"
)
print(result)

# Query
response = client.query("What is the document about?")
print(response["short_answer"])
print(f"Confidence: {response['confidence_score']}")

# Selection query
response = client.select_query(
    "What is emphasized?",
    "This is the selected text."
)
print(response["short_answer"])
```

---

## 12. JavaScript/Fetch Examples

```javascript
const BASE_URL = "http://localhost:8000";

class RAGClient {
  async health() {
    const response = await fetch(`${BASE_URL}/health`);
    return await response.json();
  }

  async embed(docId, title, content, chapter = null, lesson = null) {
    const response = await fetch(`${BASE_URL}/embed`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doc_id: docId,
        title: title,
        content: content,
        chapter: chapter,
        lesson: lesson
      })
    });
    return await response.json();
  }

  async query(queryText, topK = 10) {
    const response = await fetch(`${BASE_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: queryText,
        top_k: topK
      })
    });
    return await response.json();
  }

  async selectQuery(queryText, selectedText) {
    const response = await fetch(`${BASE_URL}/select-query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: queryText,
        selected_text: selectedText
      })
    });
    return await response.json();
  }
}

// Usage
const client = new RAGClient();

// Check health
client.health().then(status => console.log(status));

// Query
client.query("What is the book about?").then(response => {
  console.log(response.short_answer);
  console.log(`Confidence: ${response.confidence_score}`);
  response.sources.forEach(source => {
    console.log(`Source: ${source.chapter}/${source.lesson}`);
  });
});
```

---

## Troubleshooting API Calls

### Debug Response Headers

```bash
curl -v $API_URL/health
```

### Pretty Print JSON

```bash
curl -s $API_URL/health | jq '.'
```

### Save Response to File

```bash
curl -s -X POST $API_URL/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}' > response.json
```

### Measure Response Time

```bash
curl -w "@curl-format.txt" -o /dev/null -s $API_URL/health
```

(curl-format.txt contains timing format)

---

**Last Updated:** December 7, 2024
