#!/usr/bin/env python3
"""
Ingest all book documents from docusaurus-book/docs into the RAG system.
"""

import os
import sys
import json
import re
from pathlib import Path
import requests

# Backend API endpoint
API_BASE_URL = os.getenv("RAG_API_URL", "http://localhost:8000")
DOCS_PATH = Path(__file__).parent.parent / "docusaurus-book" / "docs"

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2].lstrip()

            # Parse YAML frontmatter
            metadata = {}
            for line in frontmatter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"\'')

            return metadata, body

    return {}, content

def extract_chapter_info(file_path):
    """Extract chapter/lesson info from file path."""
    parts = file_path.relative_to(DOCS_PATH).parts

    module = None
    chapter = None
    lesson = None

    if len(parts) > 0:
        first_part = parts[0]
        if first_part.startswith("module"):
            module = first_part
        elif first_part in ["introduction", "foundations", "approach", "applications", "ethics"]:
            chapter = first_part

    if len(parts) > 1:
        file_name = parts[-1]
        if file_name != "index.md":
            lesson = file_name.replace(".md", "")

    return module, chapter, lesson

def ingest_document(file_path):
    """Ingest a single markdown document."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        metadata, body = extract_frontmatter(content)

        # Extract chapter info
        module, chapter, lesson = extract_chapter_info(file_path)

        # Get title from metadata or file name
        title = metadata.get("title", file_path.stem.replace("-", " ").title())

        # Create doc_id
        doc_id = file_path.relative_to(DOCS_PATH).as_posix().replace("/", ":").replace(".md", "")

        # Prepare request
        payload = {
            "doc_id": doc_id,
            "title": title,
            "content": body,
            "chapter": chapter or module,
            "lesson": lesson,
            "source_url": None,
            "file_path": str(file_path),
            "metadata": {
                "module": module,
                "chapter": chapter,
                "lesson": lesson,
                **metadata
            }
        }

        # Send to backend
        response = requests.post(
            f"{API_BASE_URL}/embed",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            print(f"[OK] {doc_id}: {result['chunks_created']} chunks, {result['vectors_upserted']} vectors")
            return True
        else:
            print(f"[ERR] {doc_id}: {response.status_code} - {response.text[:100]}")
            return False

    except Exception as e:
        print(f"[FAIL] {file_path}: {str(e)}")
        return False

def main():
    """Main ingestion loop."""
    print(f"Starting document ingestion from {DOCS_PATH}")
    print(f"Backend API: {API_BASE_URL}")
    print()

    # Find all markdown files
    md_files = sorted(DOCS_PATH.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")
    print()

    success_count = 0
    total_count = len(md_files)

    for i, file_path in enumerate(md_files, 1):
        print(f"[{i}/{total_count}] ", end="", flush=True)
        if ingest_document(file_path):
            success_count += 1

    print()
    print(f"Ingestion complete: {success_count}/{total_count} documents successfully ingested")
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
