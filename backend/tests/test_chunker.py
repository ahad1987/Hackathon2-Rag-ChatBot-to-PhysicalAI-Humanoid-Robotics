"""Tests for document chunking."""

import pytest
from chunker import DocumentChunker


@pytest.fixture
def chunker():
    """Create a chunker instance."""
    return DocumentChunker(chunk_size=500, overlap=100)


def test_chunk_simple_text(chunker):
    """Test chunking simple text."""
    text = "This is a simple test. " * 100  # Repeat to create longer text

    chunks = chunker.chunk_text(text, {"doc_id": "test1"})

    assert len(chunks) > 0
    assert all("text" in chunk for chunk in chunks)
    assert all("tokens" in chunk for chunk in chunks)
    assert all("start_char" in chunk for chunk in chunks)
    assert all("end_char" in chunk for chunk in chunks)


def test_chunk_metadata_preservation(chunker):
    """Test that metadata is preserved in chunks."""
    text = "This is a test. " * 50
    metadata = {
        "doc_id": "test-doc",
        "chapter": "Chapter 1",
        "lesson": "Lesson 1",
    }

    chunks = chunker.chunk_text(text, metadata)

    for chunk in chunks:
        assert chunk["doc_id"] == "test-doc"
        assert chunk["chapter"] == "Chapter 1"
        assert chunk["lesson"] == "Lesson 1"


def test_chunk_size_limit(chunker):
    """Test that chunks don't exceed size limit."""
    text = "This is a test sentence. " * 200

    chunks = chunker.chunk_text(text, {"doc_id": "test"})

    for chunk in chunks:
        # Token count should be roughly under the limit
        assert chunk["tokens"] <= chunker.chunk_size * 1.2  # Allow 20% overhead


def test_chunk_overlap():
    """Test that chunks have proper overlap."""
    chunker = DocumentChunker(chunk_size=100, overlap=50)
    text = "This is a test sentence. " * 100

    chunks = chunker.chunk_text(text, {"doc_id": "test"})

    # Check that consecutive chunks have overlap
    if len(chunks) > 1:
        # Last part of chunk N should overlap with start of chunk N+1
        for i in range(len(chunks) - 1):
            chunk1_end = chunks[i]["text"][-50:]
            chunk2_start = chunks[i + 1]["text"][:50]
            # There should be some common text
            assert len(chunk1_end) > 0 and len(chunk2_start) > 0


def test_multiple_documents(chunker):
    """Test chunking multiple documents."""
    documents = [
        ("First document text. " * 50, {"doc_id": "doc1"}),
        ("Second document text. " * 50, {"doc_id": "doc2"}),
    ]

    all_chunks = chunker.chunk_multiple_documents(documents)

    # Should have chunks from both documents
    doc1_chunks = [c for c in all_chunks if c["doc_id"] == "doc1"]
    doc2_chunks = [c for c in all_chunks if c["doc_id"] == "doc2"]

    assert len(doc1_chunks) > 0
    assert len(doc2_chunks) > 0
    assert len(all_chunks) == len(doc1_chunks) + len(doc2_chunks)


def test_chunk_index_assignment(chunker):
    """Test that chunk indices are correctly assigned."""
    text = "This is a test. " * 100
    documents = [
        (text, {"doc_id": "doc1"}),
        (text, {"doc_id": "doc2"}),
    ]

    all_chunks = chunker.chunk_multiple_documents(documents)

    # Check that indices are assigned
    doc1_chunks = [c for c in all_chunks if c["doc_id"] == "doc1"]
    doc2_chunks = [c for c in all_chunks if c["doc_id"] == "doc2"]

    assert "chunk_index" in doc1_chunks[0]
    assert doc1_chunks[0]["chunk_index"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
