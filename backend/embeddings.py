"""Embeddings generation and retrieval using OpenAI."""

import asyncio
import tiktoken
from typing import List, Tuple
from openai import AsyncOpenAI
from config import get_settings

settings = get_settings()


class EmbeddingManager:
    """Manages text embeddings using OpenAI Embeddings API."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        response = await self.client.embeddings.create(
            input=text,
            model=self.model,
        )
        return response.data[0].embedding

    async def embed_texts_batch(
        self, texts: List[str], batch_size: int = 20
    ) -> List[List[float]]:
        """Generate embeddings for multiple texts with batching."""
        embeddings = []

        # Process in batches for efficiency
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = await self.client.embeddings.create(
                input=batch,
                model=self.model,
            )

            # Sort by index to maintain order
            batch_embeddings = sorted(
                response.data, key=lambda x: x.index
            )
            embeddings.extend([e.embedding for e in batch_embeddings])

        return embeddings

    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken."""
        try:
            tokens = self.encoding.encode(text)
            return len(tokens)
        except Exception:
            # Fallback: approximate 1 token per 4 characters
            return len(text) // 4

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings for this model."""
        # text-embedding-3-small: 1536 dimensions (default)
        # text-embedding-3-large: 3072 dimensions
        if "large" in self.model:
            return 3072
        else:
            # Default for all other models including text-embedding-3-small
            return 1536


# Global embedding manager instance
_embedding_manager: EmbeddingManager | None = None


def get_embedding_manager() -> EmbeddingManager:
    """Get or create the embedding manager singleton."""
    global _embedding_manager
    if _embedding_manager is None:
        _embedding_manager = EmbeddingManager()
    return _embedding_manager
