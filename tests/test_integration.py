"""
Integration tests for the research agent system.
"""

from unittest.mock import Mock, patch

import pytest


# These integration tests can be marked to run separately from unit tests


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests for the complete agent system."""

    def test_basic_to_enhanced_agent_comparison(self, mock_api_keys):
        """Test running both agents on the same topic and comparing results."""

        # Mock the basic agent
        mock_basic_agent = Mock()
        mock_basic_agent.run.return_value = "# Basic Report\n\nBasic analysis complete."

        # Mock the enhanced agent
        mock_enhanced_agent = Mock()
        mock_enhanced_agent.run.return_value = (
            "# Enhanced Report\n\nComprehensive analysis complete."
        )

        with (
            patch("agent.SAGEAgent", return_value=mock_basic_agent),
            patch(
                "enhanced_sage_agent.EnhancedSAGEAgent",
                return_value=mock_enhanced_agent,
            ),
            patch("builtins.print"),
        ):
            from main import run_basic_agent, run_enhanced_agent

            topic = "Analyze the AI market trends"

            # Run both agents
            basic_result = run_basic_agent(topic)
            enhanced_result = run_enhanced_agent(topic)

            # Verify both produced results
            assert basic_result is not None
            assert enhanced_result is not None
            assert "Basic Report" in basic_result
            assert "Enhanced Report" in enhanced_result

            # Verify they were called with the same topic
            mock_basic_agent.run.assert_called_with(goal=topic)
            mock_enhanced_agent.run.assert_called_with(goal=topic, max_iterations=20)

    def test_database_persistence_flow(self, temp_db, mock_api_keys):
        """Test the complete database persistence flow."""
        from enhanced_sage_agent import ResearchDatabase

        # Initialize database
        db = ResearchDatabase(temp_db)

        # Test caching workflow
        query = "AI market research"
        results = '{"results": [{"title": "AI Market Report", "url": "example.com"}]}'

        # Cache a result
        db.cache_search_result(query, results, "tavily")

        # Retrieve cached result
        cached = db.get_cached_result(query)
        assert cached == results

        # Test that it doesn't return old results (mock recent time)
        old_cached = db.get_cached_result(query, max_age_hours=0)
        assert old_cached is None

    def test_research_context_lifecycle(self):
        """Test the complete research context lifecycle."""
        from datetime import datetime

        from enhanced_sage_agent import ResearchContext

        # Create new research context
        start_time = datetime.now()
        context = ResearchContext(
            goal="Test research goal",
            start_time=start_time,
            sources=[],
            findings=[],
            current_phase="planning",
            confidence_score=0.0,
            iteration_count=0,
        )

        # Simulate research progression
        context.current_phase = "searching"
        context.sources.append({"url": "example.com", "title": "Test Source"})
        context.iteration_count += 1

        context.current_phase = "analyzing"
        context.findings.append({"insight": "Key finding", "confidence": 0.8})
        context.confidence_score = 0.8
        context.iteration_count += 1

        context.current_phase = "reporting"
        context.confidence_score = 0.9
        context.iteration_count += 1

        # Verify final state
        assert context.current_phase == "reporting"
        assert len(context.sources) == 1
        assert len(context.findings) == 1
        assert context.confidence_score == 0.9
        assert context.iteration_count == 3

    def test_tool_error_handling_integration(self, mock_api_keys):
        """Test how the system handles tool errors in an integrated way."""
        # Import inside the test to ensure patching works
        with (
            patch("src.enhanced_sage_agent.tavily_client") as mock_tavily,
            patch("src.enhanced_sage_agent.ResearchDatabase") as mock_db_class,
        ):
            # Mock database to return no cached results
            mock_db = Mock()
            mock_db.get_cached_result.return_value = None
            mock_db_class.return_value = mock_db

            # Mock tavily to raise exception
            mock_tavily.search.side_effect = Exception("API Rate Limited")

            from src.enhanced_sage_agent import academic_search, news_search, web_search

            result = web_search("test query")
            assert "Error during search: API Rate Limited" in result

            # Test that other search tools handle errors similarly
            news_result = news_search("test news")
            assert "Error during news search: API Rate Limited" in news_result

            academic_result = academic_search("test academic")
            assert "Error during academic search: API Rate Limited" in academic_result

    def test_full_workflow_with_mocked_apis(
        self, mock_api_keys, mock_genai, mock_tavily
    ):
        """Test a complete workflow with all APIs mocked."""
        from src.enhanced_sage_agent import EnhancedSAGEAgent

        # Setup enhanced mocks for a complete conversation
        mock_model_instance = Mock()
        mock_chat = Mock()
        mock_model_instance.start_chat.return_value = mock_chat
        mock_genai["model"].return_value = mock_model_instance

        # Mock a complete conversation flow
        responses = []

        # First response - web search
        response1 = Mock()
        response1.candidates = [Mock()]
        response1.candidates[0].content.parts = [Mock()]
        function_call1 = Mock()
        function_call1.name = "web_search"
        function_call1.args = {"query": "AI market analysis"}
        response1.candidates[0].content.parts[0].function_call = function_call1
        responses.append(response1)

        # Second response - analyze data
        response2 = Mock()
        response2.candidates = [Mock()]
        response2.candidates[0].content.parts = [Mock()]
        function_call2 = Mock()
        function_call2.name = "analyze_data"
        function_call2.args = {"data_description": "Market data analysis"}
        response2.candidates[0].content.parts[0].function_call = function_call2
        responses.append(response2)

        # Final response - finish research
        response3 = Mock()
        response3.candidates = [Mock()]
        response3.candidates[0].content.parts = [Mock()]
        function_call3 = Mock()
        function_call3.name = "finish_research"
        function_call3.args = {
            "final_report_markdown": "# AI Market Analysis\n\nComprehensive report complete."
        }
        response3.candidates[0].content.parts[0].function_call = function_call3
        responses.append(response3)

        mock_chat.send_message.side_effect = responses

        # Mock database operations
        with patch("src.enhanced_sage_agent.ResearchDatabase"):
            agent = EnhancedSAGEAgent()

            # This would be a more complex test in a real scenario
            # For now, we're just testing that the agent can be instantiated
            # and has the expected tools
            assert len(agent.tools) == 8  # All enhanced tools
            assert "web_search" in agent.tools
            assert "finish_research" in agent.tools


@pytest.mark.slow
class TestPerformanceIntegration:
    """Performance-related integration tests."""

    def test_database_performance_with_multiple_queries(self, temp_db):
        """Test database performance with multiple cache operations."""
        from src.enhanced_sage_agent import ResearchDatabase

        db = ResearchDatabase(temp_db)

        # Simulate caching multiple search results
        queries = [f"query_{i}" for i in range(100)]

        # Cache all queries
        for i, query in enumerate(queries):
            result = f"result_{i}"
            db.cache_search_result(query, result, "test")

        # Retrieve all cached results
        for i, query in enumerate(queries):
            cached = db.get_cached_result(query)
            assert cached == f"result_{i}"

    def test_agent_tool_execution_sequence(self, mock_api_keys):
        """Test the sequence of tool executions in an agent run."""
        from src.enhanced_sage_agent import (
            analyze_data,
            create_outline,
            quality_check,
            web_search,
        )

        # Mock all external dependencies
        with (
            patch("src.enhanced_sage_agent.tavily_client") as mock_tavily,
            patch("src.enhanced_sage_agent.ResearchDatabase") as mock_db_class,
            patch("google.generativeai.GenerativeModel") as mock_model,
        ):
            # Mock database to return no cached results
            mock_db = Mock()
            mock_db.get_cached_result.return_value = None
            mock_db_class.return_value = mock_db

            # Setup mocks
            mock_tavily.search.return_value = {
                "results": [{"title": "Test", "content": "Test content"}]
            }

            mock_model_instance = Mock()
            mock_response = Mock()
            mock_response.text = "Test AI response"
            mock_model_instance.generate_content.return_value = mock_response
            mock_model.return_value = mock_model_instance

            # Execute tools in sequence (simulating agent workflow)
            search_result = web_search("AI market trends")
            assert "Test" in search_result

            analysis_result = analyze_data("Market data from search")
            assert "Test AI response" in analysis_result

            outline_result = create_outline("AI market analysis")
            assert "Test AI response" in outline_result

            quality_result = quality_check("Final research content")
            assert "Test AI response" in quality_result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
