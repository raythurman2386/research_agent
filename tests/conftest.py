"""
Test configuration and fixtures for the research agent tests.
"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def mock_api_keys():
    """Mock API keys for testing."""
    with patch.dict(
        os.environ,
        {
            "GOOGLE_API_KEY": "test-google-api-key",
            "TAVILY_API_KEY": "test-tavily-api-key",
        },
    ):
        yield


@pytest.fixture
def mock_genai():
    """Mock Google GenerativeAI for testing."""
    with (
        patch("google.generativeai.configure") as mock_config,
        patch("google.generativeai.GenerativeModel") as mock_model,
    ):
        yield {
            "configure": mock_config,
            "model": mock_model,
        }


@pytest.fixture
def mock_tavily():
    """Mock Tavily client for testing."""
    mock_client = Mock()
    mock_client.search.return_value = {
        "results": [
            {
                "title": "Test Article",
                "url": "https://example.com/test",
                "content": "Test content from search",
                "score": 0.9,
            }
        ]
    }

    with patch("tavily.TavilyClient", return_value=mock_client):
        yield mock_client


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        db_path = temp_file.name

    yield db_path

    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def sample_research_goal():
    """Sample research goal for testing."""
    return "Analyze the current state of renewable energy technology markets"


@pytest.fixture
def sample_search_results():
    """Sample search results for testing."""
    return [
        {
            "title": "Renewable Energy Market Report 2024",
            "url": "https://example.com/renewable-report",
            "content": "The renewable energy market is experiencing significant growth...",
            "score": 0.95,
        },
        {
            "title": "Solar Panel Technology Advances",
            "url": "https://example.com/solar-tech",
            "content": "Recent advances in solar panel technology have improved efficiency...",
            "score": 0.88,
        },
    ]
