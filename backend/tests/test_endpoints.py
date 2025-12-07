"""Integration tests for RAG API endpoints."""

import pytest
import asyncio
from httpx import AsyncClient
from app import app


@pytest.fixture
async def client():
    """Create an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "vector_store" in data
    assert "embeddings" in data


@pytest.mark.asyncio
async def test_embed_endpoint_minimal(client):
    """Test document embedding endpoint with minimal data."""
    payload = {
        "doc_id": "test-doc-1",
        "title": "Test Document",
        "content": "This is a test document. " * 50,
    }

    response = await client.post("/embed", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["doc_id"] == "test-doc-1"
    assert "chunks_created" in data
    assert "vectors_upserted" in data
    assert "total_tokens" in data
    assert data["chunks_created"] > 0


@pytest.mark.asyncio
async def test_embed_endpoint_with_metadata(client):
    """Test document embedding with full metadata."""
    payload = {
        "doc_id": "test-doc-2",
        "title": "Test Chapter",
        "content": "This is test content. " * 50,
        "chapter": "Module 1",
        "lesson": "Introduction",
        "source_url": "http://example.com",
        "metadata": {"author": "test", "version": "1.0"},
    }

    response = await client.post("/embed", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["doc_id"] == "test-doc-2"


@pytest.mark.asyncio
async def test_query_endpoint(client):
    """Test RAG query endpoint."""
    # First ingest a document
    embed_payload = {
        "doc_id": "test-query-1",
        "title": "Test Query Document",
        "content": """
        Humanoid robots are designed to interact with human environments.
        They use vision and language models to understand instructions.
        Modern robots can perform complex manipulation tasks.
        """,
        "chapter": "Robotics Basics",
        "lesson": "Introduction",
    }

    await client.post("/embed", json=embed_payload)

    # Now query
    query_payload = {"query": "What are humanoid robots?"}

    response = await client.post("/query", json=query_payload)
    assert response.status_code == 200

    data = response.json()
    assert "query_id" in data
    assert "short_answer" in data
    assert "sources" in data
    assert "confidence_score" in data
    assert "processing_time_ms" in data
    assert data["is_selection_mode"] is False


@pytest.mark.asyncio
async def test_selection_query_endpoint(client):
    """Test selection-based query endpoint."""
    selected_text = "Humanoid robots use vision sensors to perceive their environment."

    payload = {
        "query": "What do the robots use to perceive?",
        "selected_text": selected_text,
    }

    response = await client.post("/select-query", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["is_selection_mode"] is True
    assert "short_answer" in data
    assert "sources" in data
    # Should have the selected text as source
    assert len(data["sources"]) > 0


@pytest.mark.asyncio
async def test_query_with_filters(client):
    """Test query with chapter and lesson filters."""
    # Ingest document
    embed_payload = {
        "doc_id": "test-filter-1",
        "title": "Filtered Document",
        "content": "Test content about AI. " * 50,
        "chapter": "AI Basics",
        "lesson": "Fundamentals",
    }

    await client.post("/embed", json=embed_payload)

    # Query with filters
    query_payload = {
        "query": "What is AI?",
        "chapter_filter": "AI Basics",
        "lesson_filter": "Fundamentals",
    }

    response = await client.post("/query", json=query_payload)
    assert response.status_code == 200
    data = response.json()
    assert "short_answer" in data


@pytest.mark.asyncio
async def test_invalid_query(client):
    """Test query endpoint with invalid input."""
    response = await client.post("/query", json={"invalid": "data"})
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_openapi_docs(client):
    """Test OpenAPI documentation endpoint."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
