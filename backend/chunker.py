"""Document chunking with overlap for RAG ingestion."""

from typing import List, Tuple, Dict, Any
from embeddings import get_embedding_manager


class DocumentChunker:
    """Chunks documents with configurable size and overlap."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize chunker.

        Args:
            chunk_size: Maximum tokens per chunk
            overlap: Number of overlapping tokens between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.embedding_manager = get_embedding_manager()

    def chunk_text(
        self, text: str, metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.

        Args:
            text: Full text to chunk
            metadata: Metadata to attach to each chunk (doc_id, chapter, lesson, etc.)

        Returns:
            List of chunk dictionaries with text, token count, and position info
        """
        # Split by sentences/paragraphs first
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        current_tokens = 0
        char_offset = 0

        for paragraph in paragraphs:
            paragraph_tokens = self.embedding_manager.count_tokens(paragraph)

            # Check if adding this paragraph would exceed chunk size
            if current_tokens + paragraph_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_data = {
                    "text": current_chunk.strip(),
                    "tokens": self.embedding_manager.count_tokens(
                        current_chunk
                    ),
                    "start_char": char_offset
                    - len(current_chunk),  # Approximate
                    "end_char": char_offset,
                    **metadata,
                }
                chunks.append(chunk_data)

                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(
                    current_chunk, self.overlap
                )
                current_chunk = overlap_text + paragraph
                current_tokens = self.embedding_manager.count_tokens(
                    current_chunk
                )
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
                current_tokens += paragraph_tokens

            char_offset += len(paragraph) + 2  # +2 for \n\n

        # Save final chunk
        if current_chunk:
            chunk_data = {
                "text": current_chunk.strip(),
                "tokens": self.embedding_manager.count_tokens(current_chunk),
                "start_char": char_offset - len(current_chunk),
                "end_char": char_offset,
                **metadata,
            }
            chunks.append(chunk_data)

        return chunks

    def _get_overlap_text(self, text: str, overlap_tokens: int) -> str:
        """Extract last N tokens from text for overlap."""
        sentences = text.split(". ")
        token_count = 0
        overlap_sentences = []

        for sentence in reversed(sentences):
            tokens = self.embedding_manager.count_tokens(sentence)
            if token_count + tokens <= overlap_tokens:
                overlap_sentences.insert(0, sentence)
                token_count += tokens
            else:
                break

        return ". ".join(overlap_sentences) + (". " if overlap_sentences else "")

    def chunk_multiple_documents(
        self, documents: List[Tuple[str, Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Chunk multiple documents.

        Args:
            documents: List of (text, metadata) tuples

        Returns:
            Flattened list of all chunks
        """
        all_chunks = []
        for text, metadata in documents:
            chunks = self.chunk_text(text, metadata)
            # Add chunk index
            for i, chunk in enumerate(chunks):
                chunk["chunk_index"] = i
            all_chunks.extend(chunks)
        return all_chunks
