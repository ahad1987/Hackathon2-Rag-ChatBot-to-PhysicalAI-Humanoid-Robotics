"""FastAPI RAG Chatbot Backend."""

import uuid
import time
import html
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

from config import get_settings
from database import get_db_manager, DatabaseManager
from vector_store import get_qdrant_manager, QdrantManager
from embeddings import get_embedding_manager, EmbeddingManager
from chunker import DocumentChunker

settings = get_settings()

# Global service instances
db_manager: Optional[DatabaseManager] = None
qdrant_manager: Optional[QdrantManager] = None
embedding_manager: Optional[EmbeddingManager] = None
openai_client: Optional[AsyncOpenAI] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global db_manager, qdrant_manager, embedding_manager, openai_client

    # Startup
    db_manager = await get_db_manager()
    qdrant_manager = await get_qdrant_manager()
    embedding_manager = get_embedding_manager()
    openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

    yield

    # Shutdown
    if db_manager:
        await db_manager.close()


app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation API for Physical AI & Humanoid Robotics book",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Data Models
# ============================================================================


class EmbedRequest(BaseModel):
    """Request to embed a document."""

    doc_id: str = Field(..., description="Unique document identifier")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Full document text")
    chapter: Optional[str] = Field(None, description="Chapter name")
    lesson: Optional[str] = Field(None, description="Lesson name")
    source_url: Optional[str] = Field(None, description="Source URL")
    file_path: Optional[str] = Field(None, description="File path")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata"
    )


class EmbedResponse(BaseModel):
    """Response from embedding endpoint."""

    doc_id: str
    chunks_created: int
    vectors_upserted: int
    total_tokens: int


class QueryRequest(BaseModel):
    """RAG query request."""

    query: str = Field(..., description="User query")
    user_id: Optional[str] = Field(None, description="User identifier")
    doc_id_filter: Optional[str] = Field(
        None, description="Filter by document ID"
    )
    chapter_filter: Optional[str] = Field(None, description="Filter by chapter")
    lesson_filter: Optional[str] = Field(None, description="Filter by lesson")
    top_k: Optional[int] = Field(
        settings.top_k_retrieval, description="Number of results to retrieve"
    )


class SelectionQueryRequest(BaseModel):
    """Query restricted to selected text."""

    query: str = Field(..., description="User query")
    selected_text: str = Field(
        ..., description="Text selected by user on the page"
    )
    user_id: Optional[str] = Field(None, description="User identifier")
    doc_id: Optional[str] = Field(None, description="Document context")


class SourceSnippet(BaseModel):
    """Source citation with snippet."""

    chunk_id: str
    doc_id: str
    chapter: Optional[str]
    lesson: Optional[str]
    text: str = Field(..., description="Source text snippet")
    start_char: int
    end_char: int
    score: float = Field(..., description="Relevance score")


class QueryResponse(BaseModel):
    """RAG query response."""

    query_id: str
    short_answer: str = Field(..., description="1-3 sentence answer")
    long_answer: Optional[str] = Field(None, description="Detailed explanation")
    sources: List[SourceSnippet] = Field(..., description="Source citations")
    confidence_score: float = Field(
        ..., ge=0, le=1, description="Confidence (0-1)"
    )
    is_selection_mode: bool = Field(
        False, description="Whether answer used selection mode"
    )
    processing_time_ms: float
    model_used: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    database: bool
    vector_store: bool
    embeddings: bool


# ============================================================================
# Endpoints
# ============================================================================


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check backend health."""
    db_healthy = False
    vector_healthy = False

    if db_manager:
        db_healthy = await db_manager.health_check()

    if qdrant_manager:
        vector_healthy = await qdrant_manager.health_check()

    return HealthResponse(
        status="healthy" if db_healthy and vector_healthy else "degraded",
        database=db_healthy,
        vector_store=vector_healthy,
        embeddings=embedding_manager is not None,
    )


@app.post("/embed", response_model=EmbedResponse)
async def embed_document(request: EmbedRequest) -> EmbedResponse:
    """Ingest and embed a document."""
    if not db_manager or not qdrant_manager or not embedding_manager:
        raise HTTPException(status_code=503, detail="Services not ready")

    try:
        # Save document metadata
        await db_manager.save_document(
            doc_id=request.doc_id,
            title=request.title,
            chapter=request.chapter,
            lesson=request.lesson,
            source_url=request.source_url,
            file_path=request.file_path,
            metadata=request.metadata,
        )

        # Chunk document
        chunker = DocumentChunker(
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap,
        )
        chunks = chunker.chunk_text(
            request.content,
            {
                "doc_id": request.doc_id,
                "chapter": request.chapter,
                "lesson": request.lesson,
            },
        )

        # Embed chunks
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = await embedding_manager.embed_texts_batch(chunk_texts)

        # Prepare vector data for Qdrant
        vectors_to_upsert = []
        total_tokens = 0

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"{request.doc_id}:chunk:{i}"

            # Save chunk to database
            await db_manager.save_chunk(
                chunk_id=chunk_id,
                doc_id=request.doc_id,
                chunk_index=i,
                start_char=chunk["start_char"],
                end_char=chunk["end_char"],
                text=chunk["text"],
                tokens=chunk["tokens"],
                metadata={
                    "chapter": request.chapter,
                    "lesson": request.lesson,
                },
            )

            vectors_to_upsert.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": request.doc_id,
                    "chapter": request.chapter,
                    "lesson": request.lesson,
                    "text": chunk["text"],
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"],
                    "tokens": chunk["tokens"],
                    "embedding": embedding,
                }
            )

            total_tokens += chunk["tokens"]

        # Upsert to Qdrant
        await qdrant_manager.upsert_vectors(vectors_to_upsert)

        return EmbedResponse(
            doc_id=request.doc_id,
            chunks_created=len(chunks),
            vectors_upserted=len(vectors_to_upsert),
            total_tokens=total_tokens,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest) -> QueryResponse:
    """Perform RAG query with LLM answering."""
    if not db_manager or not qdrant_manager or not embedding_manager or not openai_client:
        raise HTTPException(status_code=503, detail="Services not ready")

    query_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Check if this is an identity question
        query_lower = request.query.lower()
        if any(keyword in query_lower for keyword in ["who are you", "who am i", "what are you", "about yourself"]):
            # Direct response for identity questions
            short_answer = "I am a specialized chatbot powered by Ahad, designed to help you explore the 'Physical AI & Humanoid Robotics: The Rise of the Digital Human' book."
            long_answer = "I am a specialized chatbot powered by Ahad, designed to help you explore the 'Physical AI & Humanoid Robotics: The Rise of the Digital Human' book. I can answer questions about robotics, AI, humanoid robots, and related topics from this comprehensive guide."

            return QueryResponse(
                query_id=query_id,
                short_answer=short_answer,
                long_answer=long_answer,
                sources=[],
                confidence_score=1.0,
                is_selection_mode=False,
                processing_time_ms=(time.time() - start_time) * 1000,
                model_used="custom",
            )

        # Step 1: Embed query
        query_embedding = await embedding_manager.embed_text(request.query)

        # Step 2: Retrieve candidates from Qdrant
        search_results = await qdrant_manager.search(
            query_embedding=query_embedding,
            top_k=request.top_k or settings.top_k_retrieval,
            doc_id_filter=request.doc_id_filter,
            chapter_filter=request.chapter_filter,
            lesson_filter=request.lesson_filter,
        )

        # Step 3: Re-rank by similarity (already sorted by score from Qdrant)
        reranked = search_results[: settings.reranker_top_k]

        # Step 4: Prepare context for LLM
        context_text = "\n\n---\n\n".join(
            [
                f"[Source: {r['chapter']}/{r['lesson']}]\n{r['text']}"
                for r in reranked
            ]
        )

        # Check if this is an identity question and no context found
        identity_keywords = ["who are you", "who am i", "what are you", "about yourself", "yourself"]
        is_identity_question = any(keyword in request.query.lower() for keyword in identity_keywords)

        if is_identity_question and not reranked:
            # Direct identity answer when no context found
            identity_answer = (
                "I am a specialized chatbot powered by Ahad, designed to help you explore the 'Physical AI & Humanoid Robotics: "
                "The Rise of the Digital Human' book. I can answer questions about robotics, AI, humanoid robots, and related topics from this comprehensive guide."
            )
            short_answer = identity_answer[:300]
            long_answer = identity_answer
            confidence = 1.0
            sources = []
        else:
            # Step 5: Call LLM for answering
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an expert chatbot powered by Ahad, specialized in the book 'Physical AI & Humanoid Robotics: "
                        "The Rise of the Digital Human'. Answer questions based strictly on "
                        "the provided context. If the context doesn't contain enough information, "
                        "say so clearly. Always cite sources. "
                        "When asked who you are, mention that you are powered by Ahad."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context_text}\n\nQuestion: {request.query}",
                },
            ]

            response = await openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            answer = response.choices[0].message.content

            # Split answer into short and long
            short_answer = answer.split("\n")[0][:300]
            long_answer = answer if len(answer) > 300 else None

            # Calculate confidence (based on average score of top results)
            confidence = (
                sum(r["score"] for r in reranked) / len(reranked)
                if reranked
                else 0.0
            )

            # Prepare sources with sanitized HTML
            sources = [
                SourceSnippet(
                    chunk_id=r["chunk_id"],
                    doc_id=r["doc_id"],
                    chapter=r.get("chapter"),
                    lesson=r.get("lesson"),
                    text=html.escape(r["text"][:500]),
                    start_char=r.get("start_char", 0),
                    end_char=r.get("end_char", 0),
                    score=r["score"],
                )
                for r in reranked
            ]

        processing_time = (time.time() - start_time) * 1000

        # Save to query history
        await db_manager.save_query_history(
            query_id=query_id,
            query_text=request.query,
            user_id=request.user_id,
            is_selection_mode=False,
            retrieved_chunk_ids=[r["chunk_id"] for r in reranked],
            answer=short_answer,
            confidence_score=confidence,
            processing_time_ms=processing_time,
        )

        return QueryResponse(
            query_id=query_id,
            short_answer=short_answer,
            long_answer=long_answer,
            sources=sources,
            confidence_score=min(confidence, 1.0),
            is_selection_mode=False,
            processing_time_ms=processing_time,
            model_used=settings.openai_model,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/select-query", response_model=QueryResponse)
async def query_selection(request: SelectionQueryRequest) -> QueryResponse:
    """Query restricted to user-selected text only."""
    if not db_manager or not embedding_manager or not openai_client:
        raise HTTPException(status_code=503, detail="Services not ready")

    if not settings.enable_selection_mode:
        raise HTTPException(
            status_code=403, detail="Selection mode is disabled"
        )

    query_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Use selected text as context directly
        context_text = request.selected_text

        # Call LLM with selected text only
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert on the book 'Physical AI & Humanoid Robotics: "
                    "The Rise of the Digital Human'. Answer the question ONLY based on "
                    "the provided text selection. Do not use any other knowledge. "
                    "If the selection doesn't contain the answer, say so."
                ),
            },
            {
                "role": "user",
                "content": f"Text selection:\n{context_text}\n\nQuestion: {request.query}",
            },
        ]

        response = await openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.5,
            max_tokens=500,
        )

        answer = response.choices[0].message.content
        short_answer = answer.split("\n")[0][:300]
        long_answer = answer if len(answer) > 300 else None

        # High confidence for selection mode (direct context)
        confidence = 0.95

        processing_time = (time.time() - start_time) * 1000

        # Save to query history
        await db_manager.save_query_history(
            query_id=query_id,
            query_text=request.query,
            user_id=request.user_id,
            is_selection_mode=True,
            retrieved_chunk_ids=[],
            answer=short_answer,
            confidence_score=confidence,
            processing_time_ms=processing_time,
        )

        return QueryResponse(
            query_id=query_id,
            short_answer=short_answer,
            long_answer=long_answer,
            sources=[
                SourceSnippet(
                    chunk_id="selection",
                    doc_id=request.doc_id or "unknown",
                    chapter=None,
                    lesson=None,
                    text=html.escape(request.selected_text[:500]),
                    start_char=0,
                    end_char=len(request.selected_text),
                    score=1.0,
                )
            ],
            confidence_score=confidence,
            is_selection_mode=True,
            processing_time_ms=processing_time,
            model_used=settings.openai_model,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/openapi.json")
async def get_openapi():
    """Return OpenAPI schema."""
    return app.openapi()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.env == "development",
    )
