"""Database operations for storing document metadata in Neon PostgreSQL."""

import asyncpg
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from config import get_settings

settings = get_settings()


class DatabaseManager:
    """Manages PostgreSQL connections and metadata operations."""

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool: Optional[asyncpg.Pool] = None

    async def initialize(self) -> None:
        """Initialize the database pool and create tables."""
        self.pool = await asyncpg.create_pool(
            self.db_url,
            min_size=5,
            max_size=20,
            command_timeout=60,
        )
        await self._create_tables()

    async def _create_tables(self) -> None:
        """Create required tables if they don't exist."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            # Documents table
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    doc_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    chapter TEXT,
                    lesson TEXT,
                    source_url TEXT,
                    file_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB
                );
                """
            )

            # Chunks table - stores text segments with embeddings metadata
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE CASCADE,
                    chunk_index INTEGER,
                    start_char INTEGER,
                    end_char INTEGER,
                    text TEXT NOT NULL,
                    tokens INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB
                );
                """
            )

            # Embeddings metadata table (vector operations done in Qdrant)
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS embedding_metadata (
                    chunk_id TEXT PRIMARY KEY REFERENCES chunks(chunk_id) ON DELETE CASCADE,
                    vector_id TEXT,
                    embedding_model TEXT,
                    embedding_dim INTEGER,
                    cosine_similarity FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # Query history for analytics
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS query_history (
                    query_id TEXT PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    user_id TEXT,
                    is_selection_mode BOOLEAN DEFAULT FALSE,
                    retrieved_chunk_ids TEXT[],
                    answer TEXT,
                    confidence_score FLOAT,
                    processing_time_ms FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # Create indexes for performance
            await conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_doc_chapter ON documents(chapter);"
            )
            await conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_chunk_doc ON chunks(doc_id);"
            )
            await conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_chunk_text ON chunks USING GIN(to_tsvector('english', text));"
            )
            await conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_query_created ON query_history(created_at);"
            )

    async def close(self) -> None:
        """Close the database pool."""
        if self.pool:
            await self.pool.close()

    async def save_document(
        self,
        doc_id: str,
        title: str,
        chapter: Optional[str] = None,
        lesson: Optional[str] = None,
        source_url: Optional[str] = None,
        file_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Save a document record."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO documents (doc_id, title, chapter, lesson, source_url, file_path, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (doc_id) DO UPDATE SET
                    title = $2,
                    chapter = $3,
                    lesson = $4,
                    source_url = $5,
                    file_path = $6,
                    metadata = $7,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                doc_id,
                title,
                chapter,
                lesson,
                source_url,
                file_path,
                json.dumps(metadata) if metadata else None,
            )

    async def save_chunk(
        self,
        chunk_id: str,
        doc_id: str,
        chunk_index: int,
        start_char: int,
        end_char: int,
        text: str,
        tokens: int,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Save a text chunk."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO chunks (chunk_id, doc_id, chunk_index, start_char, end_char, text, tokens, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (chunk_id) DO UPDATE SET
                    text = $6,
                    tokens = $7,
                    metadata = $8;
                """,
                chunk_id,
                doc_id,
                chunk_index,
                start_char,
                end_char,
                text,
                tokens,
                json.dumps(metadata) if metadata else None,
            )

    async def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a chunk by its ID."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT c.*, d.title, d.chapter, d.lesson, d.source_url
                FROM chunks c
                JOIN documents d ON c.doc_id = d.doc_id
                WHERE c.chunk_id = $1;
                """,
                chunk_id,
            )
            if row:
                return dict(row)
            return None

    async def get_chunks_by_doc_id(self, doc_id: str) -> List[Dict[str, Any]]:
        """Retrieve all chunks for a document."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM chunks WHERE doc_id = $1 ORDER BY chunk_index;
                """,
                doc_id,
            )
            return [dict(row) for row in rows]

    async def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by its ID."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM documents WHERE doc_id = $1;",
                doc_id,
            )
            if row:
                return dict(row)
            return None

    async def save_query_history(
        self,
        query_id: str,
        query_text: str,
        user_id: Optional[str] = None,
        is_selection_mode: bool = False,
        retrieved_chunk_ids: Optional[List[str]] = None,
        answer: Optional[str] = None,
        confidence_score: Optional[float] = None,
        processing_time_ms: Optional[float] = None,
    ) -> None:
        """Save query history for analytics."""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO query_history
                (query_id, query_text, user_id, is_selection_mode, retrieved_chunk_ids, answer, confidence_score, processing_time_ms)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
                """,
                query_id,
                query_text,
                user_id,
                is_selection_mode,
                retrieved_chunk_ids or [],
                answer,
                confidence_score,
                processing_time_ms,
            )

    async def health_check(self) -> bool:
        """Check database connectivity."""
        if not self.pool:
            return False
        try:
            async with self.pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1;")
                return result == 1
        except Exception:
            return False


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


async def get_db_manager() -> DatabaseManager:
    """Get or create the database manager singleton."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(settings.neon_db_url)
        await _db_manager.initialize()
    return _db_manager
