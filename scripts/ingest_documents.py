#!/usr/bin/env python3
"""
Document ingestion script for RAG chatbot.

Reads Markdown files from Docusaurus book, chunks them, embeds them,
and upserts to Qdrant and PostgreSQL.
"""

import os
import sys
import asyncio
import json
from pathlib import Path
from typing import List, Tuple, Optional
import logging

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from config import get_settings
from database import get_db_manager
from vector_store import get_qdrant_manager
from embeddings import get_embedding_manager
from chunker import DocumentChunker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """Extract YAML frontmatter from markdown."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_str = parts[1]
    body = parts[2].strip()

    # Simple YAML parsing (for basic key: value pairs)
    frontmatter = {}
    for line in frontmatter_str.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"\'')

    return frontmatter, body


async def ingest_markdown_directory(
    directory: str,
    doc_id_prefix: str = "book",
) -> dict:
    """
    Ingest all markdown files from a directory.

    Args:
        directory: Path to directory containing .md files
        doc_id_prefix: Prefix for document IDs

    Returns:
        Ingestion statistics
    """
    db_manager = await get_db_manager()
    qdrant_manager = await get_qdrant_manager()
    embedding_manager = get_embedding_manager()
    chunker = DocumentChunker(
        chunk_size=settings.chunk_size,
        overlap=settings.chunk_overlap,
    )

    stats = {
        "files_processed": 0,
        "documents_saved": 0,
        "chunks_created": 0,
        "vectors_upserted": 0,
        "total_tokens": 0,
        "errors": [],
    }

    # Find all markdown files
    md_files = list(Path(directory).rglob("*.md"))
    logger.info(f"Found {len(md_files)} markdown files to ingest")

    for md_file in md_files:
        try:
            logger.info(f"Processing: {md_file}")

            # Read file
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse frontmatter
            frontmatter, body = parse_frontmatter(content)

            # Extract metadata
            title = frontmatter.get("title", md_file.stem)
            slug = frontmatter.get("slug", md_file.stem)
            doc_id = f"{doc_id_prefix}:{slug}"

            # Try to extract chapter and lesson from structure
            relative_path = md_file.relative_to(directory)
            path_parts = relative_path.parts

            chapter = None
            lesson = None

            # Simple heuristic: if file is in subdirectory, use as chapter/lesson
            if len(path_parts) > 1:
                chapter = path_parts[0].replace("-", " ").title()
                if len(path_parts) > 2:
                    lesson = path_parts[1].replace("-", " ").title()

            logger.info(
                f"  Title: {title}, Chapter: {chapter}, Lesson: {lesson}"
            )

            # Save document metadata
            await db_manager.save_document(
                doc_id=doc_id,
                title=title,
                chapter=chapter,
                lesson=lesson,
                file_path=str(md_file),
                metadata={
                    "slug": slug,
                    "relative_path": str(relative_path),
                },
            )

            # Chunk text
            chunks = chunker.chunk_text(
                body,
                {
                    "doc_id": doc_id,
                    "chapter": chapter,
                    "lesson": lesson,
                },
            )

            logger.info(f"  Created {len(chunks)} chunks")

            # Embed chunks
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = await embedding_manager.embed_texts_batch(
                chunk_texts
            )

            # Upsert to vector store
            vectors_to_upsert = []
            for i, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            ):
                chunk_id = f"{doc_id}:chunk:{i}"

                # Save to database
                await db_manager.save_chunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    chunk_index=i,
                    start_char=chunk["start_char"],
                    end_char=chunk["end_char"],
                    text=chunk["text"],
                    tokens=chunk["tokens"],
                    metadata={
                        "chapter": chapter,
                        "lesson": lesson,
                    },
                )

                vectors_to_upsert.append(
                    {
                        "chunk_id": chunk_id,
                        "doc_id": doc_id,
                        "chapter": chapter,
                        "lesson": lesson,
                        "text": chunk["text"],
                        "start_char": chunk["start_char"],
                        "end_char": chunk["end_char"],
                        "tokens": chunk["tokens"],
                        "embedding": embedding,
                    }
                )

                stats["total_tokens"] += chunk["tokens"]

            # Upsert vectors
            await qdrant_manager.upsert_vectors(vectors_to_upsert)

            stats["files_processed"] += 1
            stats["documents_saved"] += 1
            stats["chunks_created"] += len(chunks)
            stats["vectors_upserted"] += len(vectors_to_upsert)

            logger.info(
                f"  ✓ Ingested: {len(chunks)} chunks, "
                f"{len(vectors_to_upsert)} vectors"
            )

        except Exception as e:
            error_msg = f"Error processing {md_file}: {str(e)}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)

    await db_manager.close()
    return stats


async def ingest_sample_documents() -> dict:
    """
    Ingest sample test documents for verification.

    Returns:
        Ingestion statistics
    """
    db_manager = await get_db_manager()
    qdrant_manager = await get_qdrant_manager()
    embedding_manager = get_embedding_manager()
    chunker = DocumentChunker(
        chunk_size=settings.chunk_size,
        overlap=settings.chunk_overlap,
    )

    stats = {
        "files_processed": 0,
        "documents_saved": 0,
        "chunks_created": 0,
        "vectors_upserted": 0,
        "total_tokens": 0,
        "errors": [],
    }

    # Sample documents for testing
    sample_docs = [
        {
            "doc_id": "sample:intro",
            "title": "Introduction to Humanoid Robotics",
            "chapter": "Module 1",
            "lesson": "Fundamentals",
            "content": """
Humanoid robotics represents one of the most ambitious frontiers in artificial intelligence.
These systems aim to replicate human-like movement, perception, and decision-making.

The rise of humanoid robots has been driven by advances in:
- Machine learning and neural networks
- Sensor technology and computer vision
- Real-time processing capabilities
- Reinforcement learning algorithms

Humanoid robots are finding applications in:
1. Manufacturing and assembly
2. Healthcare and elderly care
3. Search and rescue operations
4. Research and education

The integration of large language models with robotics has opened new possibilities
for natural human-robot interaction and autonomous learning from experience.
            """.strip(),
        },
        {
            "doc_id": "sample:vision",
            "title": "Vision and Language in Robotics",
            "chapter": "Module 2",
            "lesson": "Perception Systems",
            "content": """
Vision-Language-Action (VLA) systems combine computer vision with language models
to enable robots to understand and act in complex environments.

Key components of VLA systems:
1. Vision Encoders: Process visual input from cameras
2. Language Models: Understand instructions and generate responses
3. Action Decoders: Convert decisions into robot commands

The transformer architecture has revolutionized how robots can:
- Understand spatial relationships
- Process natural language instructions
- Plan multi-step actions

Real-world examples include:
- Manipulation robots that can follow natural language instructions
- Autonomous systems that can explain their decisions
- Collaborative robots that adapt to human preferences

The safety implications are profound: robots must be able to explain their
reasoning and refuse unsafe actions even when instructed to perform them.
            """.strip(),
        },
    ]

    for doc in sample_docs:
        try:
            logger.info(f"Ingesting sample: {doc['title']}")

            # Save document
            await db_manager.save_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                chapter=doc["chapter"],
                lesson=doc["lesson"],
                metadata={"type": "sample"},
            )

            # Chunk
            chunks = chunker.chunk_text(
                doc["content"],
                {
                    "doc_id": doc["doc_id"],
                    "chapter": doc["chapter"],
                    "lesson": doc["lesson"],
                },
            )

            # Embed
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = await embedding_manager.embed_texts_batch(
                chunk_texts
            )

            # Upsert
            vectors_to_upsert = []
            for i, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            ):
                chunk_id = f"{doc['doc_id']}:chunk:{i}"

                await db_manager.save_chunk(
                    chunk_id=chunk_id,
                    doc_id=doc["doc_id"],
                    chunk_index=i,
                    start_char=chunk["start_char"],
                    end_char=chunk["end_char"],
                    text=chunk["text"],
                    tokens=chunk["tokens"],
                )

                vectors_to_upsert.append(
                    {
                        "chunk_id": chunk_id,
                        "doc_id": doc["doc_id"],
                        "chapter": doc["chapter"],
                        "lesson": doc["lesson"],
                        "text": chunk["text"],
                        "start_char": chunk["start_char"],
                        "end_char": chunk["end_char"],
                        "tokens": chunk["tokens"],
                        "embedding": embedding,
                    }
                )

                stats["total_tokens"] += chunk["tokens"]

            await qdrant_manager.upsert_vectors(vectors_to_upsert)

            stats["files_processed"] += 1
            stats["documents_saved"] += 1
            stats["chunks_created"] += len(chunks)
            stats["vectors_upserted"] += len(vectors_to_upsert)

            logger.info(f"✓ Ingested sample: {len(chunks)} chunks")

        except Exception as e:
            error_msg = f"Error ingesting sample {doc['doc_id']}: {str(e)}"
            logger.error(error_msg)
            stats["errors"].append(error_msg)

    await db_manager.close()
    return stats


async def main():
    """Main ingestion entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest documents for RAG chatbot"
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Path to markdown directory (default: docusaurus-book/docs)",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Ingest sample documents only",
    )

    args = parser.parse_args()

    try:
        if args.sample:
            logger.info("Ingesting sample documents...")
            stats = await ingest_sample_documents()
        else:
            # Default to docusaurus book docs
            path = args.path or "docusaurus-book/docs"
            if not os.path.exists(path):
                logger.error(f"Directory not found: {path}")
                sys.exit(1)

            logger.info(f"Ingesting documents from: {path}")
            stats = await ingest_markdown_directory(path)

        # Print results
        logger.info("\n" + "=" * 60)
        logger.info("INGESTION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Files processed: {stats['files_processed']}")
        logger.info(f"Documents saved: {stats['documents_saved']}")
        logger.info(f"Chunks created: {stats['chunks_created']}")
        logger.info(f"Vectors upserted: {stats['vectors_upserted']}")
        logger.info(f"Total tokens: {stats['total_tokens']}")

        if stats["errors"]:
            logger.warning(f"Errors encountered: {len(stats['errors'])}")
            for error in stats["errors"]:
                logger.warning(f"  - {error}")

        # Print stats as JSON for CI/CD
        print("\nJSON_STATS:")
        print(json.dumps(stats, indent=2))

        sys.exit(0 if not stats["errors"] else 1)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
