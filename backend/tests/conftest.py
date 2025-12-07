"""Pytest configuration and fixtures for RAG backend tests."""

import pytest
import asyncio
import os
from pathlib import Path

# Set test environment
os.environ["ENV"] = "test"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_data_dir():
    """Get path to test data directory."""
    return Path(__file__).parent / "data"
