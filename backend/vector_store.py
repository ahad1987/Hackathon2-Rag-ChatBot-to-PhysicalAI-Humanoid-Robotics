"""Vector store operations using Qdrant."""

from typing import List, Dict, Any, Optional, Tuple
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    PointStruct,
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
)
from config import get_settings

settings = get_settings()


class QdrantManager:
    """Manages vector operations with Qdrant Cloud."""

    def __init__(self, url: str, api_key: str, collection_name: str):
        self.client = AsyncQdrantClient(url=url, api_key=api_key, check_compatibility=False)
        self.collection_name = collection_name
        self.vector_size = 1536  # text-embedding-3-small returns 1536 dimensions

    async def initialize(self) -> None:
        """Initialize the collection if it doesn't exist."""
        try:
            await self.client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )
            # Create payload indexes for filtering
            await self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="doc_id",
                field_schema="keyword",
            )
            await self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter",
                field_schema="keyword",
            )
            await self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="lesson",
                field_schema="keyword",
            )

    async def upsert_vectors(
        self,
        vectors: List[Dict[str, Any]],
    ) -> None:
        """Upsert vectors with metadata into Qdrant."""
        points = []

        for i, vector_data in enumerate(vectors):
            point = PointStruct(
                id=hash(vector_data["chunk_id"]) & 0x7FFFFFFF,  # Positive ID
                vector=vector_data["embedding"],
                payload={
                    "chunk_id": vector_data["chunk_id"],
                    "doc_id": vector_data["doc_id"],
                    "chapter": vector_data.get("chapter"),
                    "lesson": vector_data.get("lesson"),
                    "start_char": vector_data.get("start_char"),
                    "end_char": vector_data.get("end_char"),
                    "text": vector_data.get("text"),
                    "tokens": vector_data.get("tokens", 0),
                },
            )
            points.append(point)

        # Upsert in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i : i + batch_size]
            await self.client.upsert(
                collection_name=self.collection_name,
                points=batch,
            )

    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        doc_id_filter: Optional[str] = None,
        chapter_filter: Optional[str] = None,
        lesson_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        filter_conditions = []

        if doc_id_filter:
            filter_conditions.append(
                FieldCondition(
                    key="doc_id",
                    match=MatchValue(value=doc_id_filter),
                )
            )

        if chapter_filter:
            filter_conditions.append(
                FieldCondition(
                    key="chapter",
                    match=MatchValue(value=chapter_filter),
                )
            )

        if lesson_filter:
            filter_conditions.append(
                FieldCondition(
                    key="lesson",
                    match=MatchValue(value=lesson_filter),
                )
            )

        filter_obj = None
        if filter_conditions:
            if len(filter_conditions) == 1:
                filter_obj = Filter(must=filter_conditions)
            else:
                filter_obj = Filter(must=filter_conditions)

        results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            query_filter=filter_obj,
            limit=top_k,
            with_payload=True,
        )

        return [
            {
                "chunk_id": result.payload["chunk_id"],
                "doc_id": result.payload["doc_id"],
                "chapter": result.payload.get("chapter"),
                "lesson": result.payload.get("lesson"),
                "text": result.payload.get("text"),
                "start_char": result.payload.get("start_char"),
                "end_char": result.payload.get("end_char"),
                "score": result.score,
                "tokens": result.payload.get("tokens", 0),
            }
            for result in results
        ]

    async def delete_by_doc_id(self, doc_id: str) -> None:
        """Delete all vectors for a document."""
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="doc_id",
                        match=MatchValue(value=doc_id),
                    )
                ]
            ),
        )

    async def health_check(self) -> bool:
        """Check Qdrant connectivity."""
        try:
            await self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False


# Global Qdrant manager instance
_qdrant_manager: Optional[QdrantManager] = None


async def get_qdrant_manager() -> QdrantManager:
    """Get or create the Qdrant manager singleton."""
    global _qdrant_manager
    if _qdrant_manager is None:
        _qdrant_manager = QdrantManager(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            collection_name=settings.qdrant_collection_name,
        )
        await _qdrant_manager.initialize()
    return _qdrant_manager
