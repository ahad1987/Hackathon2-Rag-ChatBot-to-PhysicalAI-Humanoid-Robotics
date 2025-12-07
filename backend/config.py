"""Configuration management for RAG chatbot backend."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    embedding_model: str = "text-embedding-3-small"

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "book-embeddings"

    # Neon PostgreSQL Configuration
    neon_db_url: str

    # Backend Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    env: str = "development"

    # CORS Configuration
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    # RAG Configuration
    top_k_retrieval: int = 10
    reranker_top_k: int = 5
    max_tokens_per_query: int = 4000
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Security Configuration
    rate_limit_queries_per_minute: int = 60
    enable_selection_mode: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

    def validate_required_keys(self) -> None:
        """Validate that all required API keys are set."""
        required = [
            "openai_api_key",
            "qdrant_url",
            "qdrant_api_key",
            "neon_db_url",
        ]
        missing = [key for key in required if not getattr(self, key)]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Copy .env.example to .env and fill in all required values."
            )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings singleton."""
    settings = Settings()
    settings.validate_required_keys()
    return settings
