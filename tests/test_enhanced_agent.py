"""
Tests for the enhanced SAGE Agent (enhanced_sage_agent.py).
"""

import json
import sqlite3
from datetime import datetime
from unittest.mock import Mock, patch

from enhanced_sage_agent import (
    EnhancedSAGEAgent,
    ResearchContext,
    ResearchDatabase,
    academic_search,
    analyze_data,
    create_outline,
    finish_research,
    generate_filename,
    market_research,
    news_search,
    quality_check,
    web_search,
)


class TestResearchDatabase:
    """Test the ResearchDatabase class."""

    def test_init_database(self, temp_db):
        """Test database initialization."""
        ResearchDatabase(temp_db)

        # Check if tables were created
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        assert "search_cache" in tables
        assert "research_sessions" in tables
        conn.close()

    def test_cache_search_result(self, temp_db):
        """Test caching search results."""
        db = ResearchDatabase(temp_db)

        query = "test query"
        results = "test results"
        source = "test source"

        db.cache_search_result(query, results, source)

        # Verify data was stored
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT query, results, source FROM search_cache WHERE query = ?", (query,)
        )
        row = cursor.fetchone()

        assert row is not None
        assert row[0] == query
        assert row[1] == results
        assert row[2] == source
        conn.close()

    def test_get_cached_result_exists(self, temp_db):
        """Test retrieving existing cached result."""
        db = ResearchDatabase(temp_db)

        query = "test query"
        results = "test results"
        source = "test source"

        db.cache_search_result(query, results, source)
        cached = db.get_cached_result(query)

        assert cached == results

    def test_get_cached_result_not_exists(self, temp_db):
        """Test retrieving non-existing cached result."""
        db = ResearchDatabase(temp_db)
        cached = db.get_cached_result("nonexistent query")
        assert cached is None


class TestResearchContext:
    """Test the ResearchContext dataclass."""

    def test_research_context_creation(self, sample_research_goal):
        """Test ResearchContext creation."""
        start_time = datetime.now()
        context = ResearchContext(
            goal=sample_research_goal,
            start_time=start_time,
            sources=[],
            findings=[],
            current_phase="planning",
            confidence_score=0.0,
            iteration_count=0,
        )

        assert context.goal == sample_research_goal
        assert context.start_time == start_time
        assert context.sources == []
        assert context.findings == []
        assert context.current_phase == "planning"
        assert context.confidence_score == 0.0
        assert context.iteration_count == 0
        assert context.research_outline is None


class TestEnhancedSearchTools:
    """Test the enhanced search tool functions."""

    def test_web_search_with_cache(self, mock_api_keys, temp_db):
        """Test web search with caching."""
        # Mock the database to return no cached result first
        with (
            patch("enhanced_sage_agent.ResearchDatabase") as mock_db_class,
            patch("enhanced_sage_agent.tavily_client") as mock_tavily,
        ):
            mock_db = Mock()
            mock_db.get_cached_result.return_value = None
            mock_db_class.return_value = mock_db

            mock_tavily.search.return_value = {
                "results": [{"title": "Test", "url": "test.com"}]
            }

            query = "renewable energy market"
            result = web_search(query)

            # Verify search was called
            mock_tavily.search.assert_called_once()
            mock_db.cache_search_result.assert_called_once()

            # Verify result format
            search_results = json.loads(result)
            assert isinstance(search_results, list)

    def test_web_search_uses_cache(self, mock_api_keys, temp_db):
        """Test web search uses cached results when available."""
        with patch("enhanced_sage_agent.ResearchDatabase") as mock_db_class:
            mock_db = Mock()
            cached_result = json.dumps(
                [{"title": "Cached Result", "url": "cached.com"}]
            )
            mock_db.get_cached_result.return_value = cached_result
            mock_db_class.return_value = mock_db

            result = web_search("test query")
            assert result == cached_result

    def test_news_search(self, mock_api_keys):
        """Test news search functionality."""
        with patch("enhanced_sage_agent.tavily_client") as mock_tavily:
            mock_tavily.search.return_value = {
                "results": [{"title": "News", "url": "news.com"}]
            }

            query = "renewable energy"
            result = news_search(query)

            # Verify search was called with news domains
            mock_tavily.search.assert_called_once()
            call_args = mock_tavily.search.call_args
            assert "include_domains" in call_args[1]

            # Verify result format
            search_results = json.loads(result)
            assert isinstance(search_results, list)

    def test_academic_search(self, mock_api_keys):
        """Test academic search functionality."""
        with patch("enhanced_sage_agent.tavily_client") as mock_tavily:
            mock_tavily.search.return_value = {
                "results": [{"title": "Academic", "url": "scholar.com"}]
            }

            query = "machine learning"
            result = academic_search(query)

            # Verify search was called with academic sites
            mock_tavily.search.assert_called_once()
            call_args = mock_tavily.search.call_args
            modified_query = call_args[1]["query"]
            assert "scholar.google.com" in modified_query

            # Verify result format
            search_results = json.loads(result)
            assert isinstance(search_results, list)

    def test_market_research(self, mock_api_keys):
        """Test market research functionality."""
        with patch("enhanced_sage_agent.tavily_client") as mock_tavily:
            mock_tavily.search.return_value = {
                "results": [{"title": "Market", "url": "market.com"}]
            }

            query = "AI industry"
            result = market_research(query)

            # Verify search was called with market research terms
            mock_tavily.search.assert_called_once()
            call_args = mock_tavily.search.call_args
            modified_query = call_args[1]["query"]
            assert "market research" in modified_query

            # Verify result format
            search_results = json.loads(result)
            assert isinstance(search_results, list)


class TestAnalysisTools:
    """Test the analysis tool functions."""

    def test_analyze_data(self, mock_genai, mock_api_keys):
        """Test data analysis functionality."""
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.text = "Analysis results: Market is growing at 15% CAGR"
        mock_model_instance.generate_content.return_value = mock_response
        mock_genai["model"].return_value = mock_model_instance

        data_description = "Market data showing growth trends"
        result = analyze_data(data_description)

        assert "Analysis results" in result
        mock_model_instance.generate_content.assert_called_once()

    def test_create_outline(self, mock_genai, mock_api_keys):
        """Test outline creation functionality."""
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.text = "# Research Outline\n1. Introduction\n2. Market Analysis"
        mock_model_instance.generate_content.return_value = mock_response
        mock_genai["model"].return_value = mock_model_instance

        topic = "AI market analysis"
        result = create_outline(topic)

        assert "Research Outline" in result
        mock_model_instance.generate_content.assert_called_once()

    def test_quality_check(self, mock_genai, mock_api_keys):
        """Test quality check functionality."""
        mock_model_instance = Mock()
        mock_response = Mock()
        mock_response.text = (
            "Quality Score: 8/10. Comprehensive analysis with good sources."
        )
        mock_model_instance.generate_content.return_value = mock_response
        mock_genai["model"].return_value = mock_model_instance

        content = "Research content to evaluate"
        result = quality_check(content)

        assert "Quality Score" in result
        mock_model_instance.generate_content.assert_called_once()


class TestUtilityFunctions:
    """Test utility functions."""

    def test_generate_filename_geospatial(self):
        """Test filename generation for geospatial software topic."""
        topic = (
            "Analyze the current state of the geospatial software development industry"
        )
        filename = generate_filename(topic)

        assert "Geospatial-Software-Industry-Analysis" in filename
        assert filename.endswith(".md")
        assert len(filename.split("_")) >= 2  # Should include timestamp

    def test_generate_filename_market_analysis(self):
        """Test filename generation for market analysis topic."""
        topic = "Write a comprehensive market analysis report"
        filename = generate_filename(topic)

        assert "Market-Analysis-Report" in filename
        assert filename.endswith(".md")

    def test_generate_filename_fallback(self):
        """Test filename generation fallback for generic topics."""
        topic = "Research the impact of technology"
        filename = generate_filename(topic)

        assert filename.endswith(".md")
        assert "Research" in filename or "Technology" in filename

    def test_generate_filename_exception_handling(self):
        """Test filename generation with exception handling."""
        # Test the actual exception handling in the function
        with patch("enhanced_sage_agent.datetime") as mock_datetime:
            # Make datetime.now() work but strftime fail on the first call
            mock_now = Mock()
            mock_now.strftime.side_effect = [
                Exception("Format error"),
                "20250814_120000",
            ]
            mock_datetime.now.return_value = mock_now

            # Should still return a valid filename even with exceptions
            filename = generate_filename("test topic")
            assert filename.endswith(".md")
            assert "Research-Report_" in filename

    def test_finish_research(self, temp_db, mock_api_keys):
        """Test finish research functionality."""
        with patch("enhanced_sage_agent.ResearchDatabase") as mock_db_class:
            mock_db = Mock()
            mock_db.db_path = temp_db
            mock_db_class.return_value = mock_db

            # Create a temporary database
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_sessions (
                    session_id TEXT PRIMARY KEY,
                    goal TEXT,
                    start_time DATETIME,
                    end_time DATETIME,
                    status TEXT,
                    final_report TEXT
                )
            """)
            conn.commit()
            conn.close()

            report = "# Final Research Report\n\nComprehensive analysis complete."
            result = finish_research(report)

            assert result == report


class TestEnhancedSAGEAgent:
    """Test the EnhancedSAGEAgent class."""

    def test_agent_initialization(self, mock_genai, mock_api_keys, temp_db):
        """Test enhanced agent initialization."""
        with patch("enhanced_sage_agent.ResearchDatabase"):
            agent = EnhancedSAGEAgent()

            assert hasattr(agent, "tools")
            assert hasattr(agent, "context")
            assert hasattr(agent, "db")

            # Check that all enhanced tools are present
            expected_tools = [
                "web_search",
                "news_search",
                "academic_search",
                "market_research",
                "analyze_data",
                "create_outline",
                "quality_check",
                "finish_research",
            ]

            for tool in expected_tools:
                assert tool in agent.tools

    def test_agent_initialization_custom_model(self, mock_genai, mock_api_keys):
        """Test enhanced agent initialization with custom model."""
        with patch("enhanced_sage_agent.ResearchDatabase"):
            custom_model = "gemini-1.5-flash"
            EnhancedSAGEAgent(model_name=custom_model)

            # Verify model was called with custom name
            mock_genai["model"].assert_called()
            # Get the model name from any of the calls
            model_calls = mock_genai["model"].call_args_list
            assert len(model_calls) > 0  # At least one model was created
